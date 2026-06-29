import json
import logging
import math
import os
import re
import shutil
import tarfile
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.request import urlopen

from opa_wasmtime import OPAPolicy

logger = logging.getLogger(__name__)
try:
    import jsonschema
except ImportError:
    jsonschema = None


def _sanitize_json_value(value):
    """Return a JSON-compatible value for OPA WASM evaluation."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, list):
        return [_sanitize_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _sanitize_json_value(item) for key, item in value.items()}
    return value


def _builtin_time_format(*args):
    """OPA time.format: format nanoseconds into a time string.

    Accepts:
      - (ns) -> RFC3339 string
      - ([ns, layout]) -> formatted with layout
      - ([ns, layout, tz]) -> formatted with layout and timezone
    """
    if not args:
        return ""
    value = args[0]
    if isinstance(value, list):
        ns = value[0]
        layout = value[1] if len(value) > 1 else None
        # tz name is value[2] if present (ignored for simplicity)
    else:
        ns = value
        layout = None

    dt = datetime.fromtimestamp(ns / 1e9, tz=timezone.utc)
    if layout is None:
        return dt.isoformat()
    # Map common Go time layout tokens to Python strftime directives
    fmt = layout
    fmt = fmt.replace("2006", "%Y")
    fmt = fmt.replace("01", "%m")
    fmt = fmt.replace("02", "%d")
    fmt = fmt.replace("15", "%H")
    fmt = fmt.replace("04", "%M")
    fmt = fmt.replace("05", "%S")
    return dt.strftime(fmt)


def _builtin_regex_find_n(*args):
    """OPA regex.find_n(pattern, value, number).

    Returns at most `number` matches of `pattern` in `value`.
    If number < 0, returns all matches.
    """
    if len(args) < 3:
        return []
    pattern, value, number = args[0], args[1], args[2]
    matches = re.findall(pattern, str(value))
    if number < 0:
        return matches
    return matches[:number]


def _builtin_time_now_ns(*args):
    """OPA time.now_ns: current time in nanoseconds."""
    return int(time.time() * 1e9)


def _builtin_sprintf(*args):
    """OPA sprintf(format, values).

    OPA uses Go-style format verbs. This translates common verbs
    (%s, %d, %v, %f, %g, %e) to Python equivalents.
    """
    if len(args) < 2:
        return ""
    fmt_str, values = args[0], args[1]
    # Replace Go's %v (default format) with %s for Python compatibility
    py_fmt = fmt_str.replace("%v", "%s")
    try:
        return py_fmt % tuple(values)
    except (TypeError, ValueError):
        return fmt_str


def _builtin_json_match_schema(*args):
    """OPA json.match_schema(document, schema).

    Returns [valid: bool, errors: list[str]].
    Uses jsonschema library if available, otherwise returns valid.
    """
    if len(args) < 2:
        return [True, []]
    document, schema = args[0], args[1]
    # OPA accepts either objects or JSON strings
    if isinstance(document, str):
        try:
            document = json.loads(document)
        except json.JSONDecodeError:
            return [False, ["invalid JSON document"]]
    if isinstance(schema, str):
        try:
            schema = json.loads(schema)
        except json.JSONDecodeError:
            return [False, ["invalid JSON schema"]]
    if jsonschema is None:
        return [True, []]
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(document), key=lambda e: list(e.path))
    if not errors:
        return [True, []]
    return [False, [e.message for e in errors]]


def _builtin_regex_replace(*args):
    """OPA regex.replace(s, pattern, value).

    Replaces all occurrences of `pattern` in `s` with `value`.
    """
    if len(args) < 3:
        return ""
    s, pattern, value = args[0], args[1], args[2]
    return re.sub(pattern, value, str(s))


def _builtin_time_parse_ns(*args):
    """OPA time.parse_ns(layout, value).

    Parses a time string according to layout and returns nanoseconds.
    Falls back to ISO 8601 parsing if Go-layout translation fails.
    """
    if len(args) < 2:
        return 0
    layout, value = args[0], args[1]
    # Translate common Go reference-time tokens to strptime directives
    fmt = layout
    fmt = fmt.replace("2006", "%Y")
    fmt = fmt.replace("01", "%m")
    fmt = fmt.replace("02", "%d")
    fmt = fmt.replace("15", "%H")
    fmt = fmt.replace("04", "%M")
    fmt = fmt.replace("05", "%S")
    try:
        dt = datetime.strptime(value, fmt)
        dt = dt.replace(tzinfo=timezone.utc)
    except ValueError:
        try:
            dt = datetime.fromisoformat(value)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return 0
    return int(dt.timestamp() * 1e9)


class OpaEngine:
    def __init__(self, wasm_path: str):
        try:
            if tarfile.is_tarfile(wasm_path):
                with tarfile.open(wasm_path, "r:*") as tar:
                    wasm_members = [
                        m for m in tar.getmembers() if m.name.endswith(".wasm")
                    ]
                    if not wasm_members:
                        raise ValueError(f"No .wasm file found in {wasm_path}")
                    f = tar.extractfile(wasm_members[0])
                    if f is not None:
                        wasm_bytes = f.read()
                    else:
                        raise ValueError(f"Could not extract {wasm_members[0].name}")
            else:
                wasm_bytes = Path(wasm_path).read_bytes()

            fd, temp_path = tempfile.mkstemp(suffix=".wasm")
            os.write(fd, wasm_bytes)
            os.close(fd)
            self._temp_path = temp_path

            builtins_map = {
                "time.format": _builtin_time_format,
                "regex.find_n": _builtin_regex_find_n,
                "time.now_ns": _builtin_time_now_ns,
                "sprintf": _builtin_sprintf,
                "json.match_schema": _builtin_json_match_schema,
                "regex.replace": _builtin_regex_replace,
                "time.parse_ns": _builtin_time_parse_ns,
            }

            self.policy = OPAPolicy(
                self._temp_path,
                builtins=builtins_map,
                min_memory=5120,
                max_memory=16384,
            )
            logger.info("WASM module %s is loaded successfully.", wasm_path)

            # Load data.json from the bundle to provide rule configurations
            # (ontology lists, controlled vocabularies, etc.) to the WASM policy.
            # Without this, many validation rules evaluate to empty/undefined.
            self._load_bundle_data(wasm_path)
        except Exception as ex:
            logger.info("Failed to load WASM module %s.", ex)
            raise ex

    def _load_bundle_data(self, wasm_path: str) -> None:
        """Extract and load data.json from an OPA bundle into the policy.

        The `opa eval --data bundle.tar.gz` command automatically loads both
        the Rego rules and data.json. When using the WASM engine, the compiled
        policy already contains the rules, but data.json must be loaded
        separately via `set_data()`.
        """
        data_names = {"/data.json", "data.json"}
        try:
            with tarfile.open(wasm_path, "r:*") as tar:
                for member in tar.getmembers():
                    if member.name in data_names:
                        f = tar.extractfile(member)
                        if f is not None:
                            data = json.load(f)
                            self.policy.set_data(data)
                            logger.info(
                                "Bundle data loaded from %s/%s", wasm_path, member.name
                            )

                            return
            logger.warning("Warning: No data.json found in bundle: %s ", wasm_path)
        except Exception as e:
            logger.warning(
                "Warning: Failed to load bundle data from: %s %s ", wasm_path, e
            )

    def __del__(self):
        if hasattr(self, "_temp_path") and Path(self._temp_path).exists():
            try:
                temp_path = Path(self._temp_path)
                if temp_path.is_dir():
                    shutil.rmtree(temp_path)
                else:
                    temp_path.unlink()
            except OSError:
                pass

    def evaluate(self, input_data: dict, entrypoint: None | str | int) -> dict:
        """
        Evaluate physical input data against the loaded OPA WASM rules.
        """
        input_data = _sanitize_json_value(input_data)
        result = self.policy.evaluate(input_data, entrypoint=entrypoint)
        # Return the raw OPA evaluation result so callers can inspect
        # the returned list of evaluation records
        return result[0].get("result") if result and result[0] else []


class OpaEngineFactory:
    def __init__(self):
        self.engines: dict[Path, OpaEngine] = {}

    def load_from_url(self, url: str, file_path: str) -> None:
        """Download a file from a URL and save it to the given file path.

        Args:
            url: The URL to download from.
            file_path: The local path to save the downloaded file.

        Raises:
            URLError: If the URL cannot be reached.
            OSError: If the file cannot be written.
        """

        target_path = Path(file_path)
        target_path.parent.mkdir(exist_ok=True, parents=True)
        logger.info("Downloading %s to %s", url, file_path)

        with urlopen(url) as response, target_path.open("wb") as out_file:  # noqa: S310
            while chunk := response.read(8192):
                out_file.write(chunk)

        logger.info("Saved %s (%d bytes)", file_path, target_path.stat().st_size)

    def get_opa_engine(
        self,
        wasm_file_path: str,
        wasm_download_url: Optional[str] = None,
    ):
        if not wasm_file_path:
            raise ValueError("Invalid WASM file path")
        wasm_path = Path(wasm_file_path)
        if wasm_path in self.engines:
            return self.engines[wasm_path]

        if not wasm_path.exists() and not wasm_download_url:
            raise ValueError(
                "Invalid WASM file does not exists and URL is not defined. "
                "Select a valid file path or a valid URL to download WASM file"
            )

        if not wasm_path.exists():
            self.load_from_url(wasm_download_url, wasm_file_path)

        engine = OpaEngine(wasm_path=wasm_file_path)
        self.engines[wasm_path] = engine
        return engine

    # def evaluate_opa_policy(
    #     self,
    #     wasm_file_path: str,
    #     entrypoint: str,
    #     input_json: dict,
    #     wasm_download_url: Optional[str] = None,
    # ) -> dict:
    #     if not entrypoint:
    #         raise ValueError("WASM entrypoint is not defined")
    #     if not input_json:
    #         raise ValueError("input json is not defined")

    #     engine: OpaEngine = self.get_opa_engine(wasm_file_path, wasm_download_url)
    #     return engine.evaluate(input_json, entrypoint)
