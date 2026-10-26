import pathlib
from typing import Annotated, Any, Dict, Literal, Optional, Tuple

from pydantic import ValidationError
from pydantic.fields import Field

from mztab_m_io import model
from mztab_m_io.model.mztabm import MzTabM
from mztab_m_io.model.serialization import SerializationContext
from mztab_m_io.model.validation import (
    Category,
    MessageType,
    MzTabMessage,
    ValidationContext,
)


class MzTabMLoadResult(ValidationContext):
    """Result object containing the loaded MzTabM data and validation information.

    This class extends ValidationContext to include the loading status and
    the parsed MzTabM object. It's used as the return type for loading and
    parsing operations to provide both the result and any validation messages
    or errors that occurred during the process.
    """

    success: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the loading operation was successful",
        ),
    ] = None

    mztabm: Annotated[
        Optional[MzTabM],
        Field(
            default=None,
            description="The loaded and validated MzTabM object, if successful",
        ),
    ] = None


def read(
    file_path: str,
    format: Literal["tsv", "json", "yaml"] = "tsv",
    auto_complete_ids: bool = False,
) -> MzTabMLoadResult:
    """Read and parse an mzTab-M file in TSV, JSON, or YAML format.

    This function reads an mzTab-M formatted file and attempts to parse
    it into an MzTabM object.
    The parsing includes validation of the content against the mzTab-M specification.

    Args:
        file_path: Path to the mzTab-M file to read.
        format: The format of the input file. One of:
            - "tsv": Tab-separated values (default)
            - "json": JSON format
            - "yaml": YAML format

    Returns:
        MzTabMLoadResult containing:
            - success: Boolean indicating if parsing was successful
            - mztabm: The parsed MzTabM object if successful, None otherwise
            - messages: List of validation messages or errors encountered

    Raises:
        ValueError: If file_path is empty or format is invalid
        FileNotFoundError: If the specified file does not exist

    Example:
        >>> result = read("example.mztab", format="tsv")
        >>> if result.success:
        ...     mztabm = result.mztabm
        ...     print(f"Loaded mzTab-M file with {len(result.messages)} messages")
        ... else:
        ...     print("Failed to load file")
        ...     for msg in result.messages:
        ...         print(f"{msg.message_type}: {msg.message}")
    """
    if not file_path:
        raise ValueError("Invalid file path")
    if not format:
        raise ValueError("Invalid file format.")

    input_path = pathlib.Path(file_path)
    if not input_path.exists():
        raise ValueError("Input file does not exist.")

    if format == "tsv":
        result = MzTabMLoadResult(
            success=False,
            messages=[],
            source_format="tsv",
            auto_complete_ids=auto_complete_ids,
        )
        try:
            mztabm, context = MzTabM.from_tsv_file(
                input_path,
                context=ValidationContext(
                    source_format="tsv", auto_complete_ids=auto_complete_ids
                ),
            )
            result.mztabm = mztabm
            if mztabm:
                result.success = True
            result.messages.extend(context.messages)
        except ValidationError as ex:
            result.messages.extend(
                [
                    MzTabMessage(
                        category=Category.FORMAT,
                        message_type=MessageType.ERROR,
                        message=repr(x),
                        source="",
                    )
                    for x in ex.errors()
                ]
            )
        return result
    elif format == "json" or format == "yaml":
        if format == "json":
            mztabm, context = MzTabM.from_json_file(input_path)
        else:
            mztabm, context = MzTabM.from_yaml_file(input_path)
        success = False
        errors = [x for x in context.messages if x.message_type == MessageType.ERROR]
        if not errors and mztabm:
            success = True
        return MzTabMLoadResult(
            success=success, mztabm=mztabm, messages=context.messages
        )
    else:
        raise ValueError(f"invalid format type: {format}")


def write(
    mztabm: MzTabM, file_path: str, format: Literal["tsv", "json", "yaml"] = "tsv"
) -> SerializationContext:
    """Write an MzTabM object to a file in TSV, JSON, or YAML format.

    This function serializes an MzTabM object to the specified format
    and writes it to a file.
    The target directory will be created if it doesn't exist.

    Args:
        mztabm: The MzTabM object to serialize
        file_path: Path where the file should be written
        format: The desired output format. One of:
            - "tsv": Tab-separated values (default)
            - "json": JSON format
            - "yaml": YAML format

    Returns:
        context: The serialization context containing the result
            and any validation messages

    Raises:
        ValueError: If mztabm is None, file_path is empty, or format is invalid

    Example:
        >>> mztabm = read("example.mztab")
        >>> context = write(mztabm, "output.mztab")
        >>> if context.success:
        ...     print("File written successfully")
        ... else:
        ...     print("Failed to write file")
    """
    if not mztabm:
        raise ValueError("Invalid mzTab-M input")
    if not file_path:
        raise ValueError("Invalid file path")
    if not format:
        raise ValueError("Invalid file format.")
    target_path = pathlib.Path(file_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    return mztabm.save(file_path, format)


def load_from_dict(data: Dict[str, Any]) -> MzTabMLoadResult:
    """Load and validate an MzTabM object from a dictionary.

    This function takes a dictionary representation of an mzTab-M file and attempts to
    validate and convert it into an MzTabM object. The dictionary should follow the
    mzTab-M structure with proper field names and data types.

    Args:
        data: A dictionary containing mzTab-M data. The structure should match
             the mzTab-M specification with proper field names and nested objects.

    Returns:
        MzTabMLoadResult containing:
            - success: Boolean indicating if loading was successful
            - mztabm: The loaded MzTabM object if successful, None otherwise
            - messages: List of validation messages or errors encountered

    Example:
        >>> result = load_from_dict(data)
        >>> if result.success:
        ...     mztabm = result.mztabm
        ...     print("Data loaded successfully")
        ... else:
        ...     print("Validation failed:")
        ...     for msg in result.messages:
        ...         print(f"{msg.message_type}: {msg.message}")
    """
    result = MzTabMLoadResult(success=False, messages=[], source_format="json")
    try:
        mztabm = MzTabM.from_dict(data, context=result)
        result.mztabm = mztabm
        result.success = True
    except ValidationError as ex:
        result.messages.extend(
            [
                MzTabMessage(
                    category=Category.FORMAT,
                    message_type=MessageType.ERROR,
                    message=repr(x),
                )
                for x in ex.errors()
            ]
        )
    except Exception as ex:
        result.messages.append(
            MzTabMessage(
                category=Category.FORMAT,
                message_type=MessageType.ERROR,
                message=str(ex),
            )
        )
    return result


def convert_to_dict(
    mztabm: MzTabM, context: Optional[SerializationContext] = None
) -> Tuple[Dict[str, Any], SerializationContext]:
    """Convert an MzTabM object to a dictionary representation.

    This function converts an MzTabM object into a dictionary format suitable for
    serialization to JSON or other formats. The conversion uses field aliases and
    excludes None values to create a clean representation.

    Args:
        mztabm: The MzTabM object to convert
        context: Optional serialization context

    Returns:
        Tuple[Dict[str, Any], SerializationContext]: Dictionary representation of
        the MzTabM object and the serialization context

    Raises:
        ValueError: If mztabm is None

    Example:
        >>> mztabm = read("example.mztab")
        >>> dict_data, context = convert_to_dict(mztabm)
        >>> if context.success:
        ...     print(f"Converted object with {len(dict_data)} top-level keys")
        ... else:
        ...     print("Failed to convert object")
    """
    if not mztabm:
        raise ValueError("Invalid mzTab-M input")
    if not context:
        context = SerializationContext()
    return mztabm.to_dict(context), context


__all__ = [
    "MzTabMLoadResult",
    "model",
    "read",
    "write",
    "load_from_dict",
    "convert_to_dict",
]
