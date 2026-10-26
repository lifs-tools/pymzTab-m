import re
from typing import (
    Annotated,
    Any,
    List,
    Literal,
    Optional,
    OrderedDict,
    Type,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel

try:
    import types

    types.UnionType
    TYPES_ENABLED = True
except Exception:
    TYPES_ENABLED = False


def sanitize_str(val: Optional[str], separators: Optional[list[str]] = None) -> str:
    if not val:
        return ""
    sanitized = val if isinstance(val, str) else str(val)
    # Replace common whitespace control chars with space
    sanitized = sanitized.strip().strip('"').strip()
    sanitized = re.sub(r"[\t\n\r]", " ", sanitized)
    # Remove remaining control characters (U+0000–U+001F, U+007F)
    sanitized = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", sanitized)
    sanitized = re.sub(r" +", " ", sanitized)

    # sanitized = sanitized.replace('"', '\\"')
    separators_set = {",", "|", '"'}
    if separators:
        separators_set.update(separators)
    if any(c in sanitized for c in separators_set):
        return f'"{sanitized}"'
    return sanitized


def split_joined_str(val: str, separator: str) -> list[str]:
    """Split a joined string by *separator*, respecting quoted items.

    Items that were quoted by ``sanitize_str`` (because they contained the
    separator) are surrounded by ``"`` and have internal ``"`` and ``\\``
    escaped with a leading backslash.  This function reverses that process:

    1. Split on *separator* only when outside quoted regions.
    2. Strip surrounding quotes from each item.
    3. Unescape ``\\\\"`` → ``"`` and ``\\\\\\\\`` → ``\\\\`` inside each item.

    For unquoted items that contain ``\\`` (i.e. they were escaped by
    ``sanitize_str`` but did not need quoting), the backslash sequences
    are also unescaped.

    Args:
        val: The raw joined string (e.g. from a TSV cell).
        separator: The join operator (e.g. ``"|"``).

    Returns:
        A list of unescaped item strings.
    """
    if not val:
        return []

    items: list[str] = []
    current: list[str] = []
    in_quotes = False
    i = 0

    while i < len(val):
        ch = val[i]

        if ch == '"' and not in_quotes:
            # Opening quote
            in_quotes = True
            i += 1
            continue

        if in_quotes:
            if ch == "\\" and i + 1 < len(val):
                # Escaped character — take the next char literally
                current.append(val[i + 1])
                i += 2
                continue
            if ch == '"':
                # Closing quote
                in_quotes = False
                i += 1
                continue
            current.append(ch)
            i += 1
            continue

        # Outside quotes: check for separator
        sep_len = len(separator)
        if val[i : i + sep_len] == separator:
            item = "".join(current)
            items.append(item)
            current = []
            i += sep_len
            continue

        current.append(ch)
        i += 1

    item = "".join(current)
    items.append(item)
    return items


def _is_union(t):
    """True for typing.Union[...] or PEP 604 T | U."""
    origin = get_origin(t)
    if TYPES_ENABLED:
        return origin is Union or origin is types.UnionType
    return origin is Union


def _unwrap_annotated(t):
    while get_origin(t) is Annotated:
        t = get_args(t)[0]
    return t


def _is_none(t):
    return t is type(None)


def _choose_union(members):
    """Prefer int, else first concrete non-None, else Any."""
    for m in members:
        if isinstance(m, type) and issubclass(m, int):
            return int
    for m in members:
        if isinstance(m, type):
            return m
    return Any


def _resolve(annotation):
    annotation = _unwrap_annotated(annotation)

    # ---- Literal[...] → str ----
    if get_origin(annotation) is Literal:
        return False, str

    # ---- Union / Optional ----
    if _is_union(annotation):
        args = get_args(annotation)
        non_none = [a for a in args if not _is_none(a)]

        if not non_none:
            return False, Any

        if len(non_none) == 1:
            return _resolve(non_none[0])

        return False, _choose_union(non_none)

    # ---- List[T] ----
    origin = get_origin(annotation)
    if origin in (list, List):
        args = get_args(annotation)
        if not args:
            return True, Any
        (item,) = args

        item = _unwrap_annotated(item)

        # item is a union?
        if _is_union(item):
            item_args = get_args(item)
            non_none = [a for a in item_args if not _is_none(a)]

            if not non_none:
                return True, Any
            if len(non_none) == 1:
                inner = non_none[0]
                return True, inner if isinstance(inner, type) else Any

            return True, _choose_union(non_none)

        return True, item if isinstance(item, type) else Any

    # ---- Concrete type ----
    return False, annotation if isinstance(annotation, type) else Any


def get_field_type_info(model: Type[BaseModel], field_name: str):
    field = model.model_fields[field_name]
    return _resolve(field.annotation)


def to_plain_dict(obj):
    """
    Recursively convert OrderedDict → dict.
    Works for nested structures (dicts, lists, tuples, sets).
    Other types are returned unchanged.
    """
    if isinstance(obj, OrderedDict):
        obj = dict(obj)

    if isinstance(obj, dict):
        return {k: to_plain_dict(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [to_plain_dict(v) for v in obj]

    elif isinstance(obj, tuple):
        return tuple(to_plain_dict(v) for v in obj)

    elif isinstance(obj, set):
        return {to_plain_dict(v) for v in obj}

    return obj
