import logging
import re
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    OrderedDict,
    Type,
    Union,
)

from pydantic import BaseModel, ValidationError

from mztab_m_io.model.base import MzTabBaseModel
from mztab_m_io.model.field_utils import split_joined_str
from mztab_m_io.model.mztabm_validation import to_jsonpath
from mztab_m_io.model.section.base_table_section import BaseTableSection
from mztab_m_io.model.section.mtd import Metadata
from mztab_m_io.model.section.sme import SmallMoleculeEvidence
from mztab_m_io.model.section.smf import SmallMoleculeFeature
from mztab_m_io.model.section.sml import SmallMoleculeSummary
from mztab_m_io.model.serialization import IdentifiableModel, SerializationContext
from mztab_m_io.model.validation import Category, MessageType, MzTabMessage

logger = logging.getLogger(__name__)


def update_ids(model: BaseModel, idx: Union[None, int] = None):
    if isinstance(model, IdentifiableModel):
        if idx is not None:
            model.id = idx
    for field in model.__class__.model_fields.keys():
        val = getattr(model, field)
        if isinstance(val, list):
            for id, item in enumerate(val, start=1):
                if isinstance(item, BaseModel):
                    update_ids(item, id)
        if isinstance(val, Mapping):
            for _, v in val.items():
                if isinstance(v, list):
                    for id, item in enumerate(v, start=1):
                        if isinstance(item, BaseModel):
                            update_ids(item, id)
        elif isinstance(val, BaseModel):
            update_ids(val, None)


def parse_table_section(
    lines: List[str], header_prefix: str, data_prefix: str
) -> List[Dict[str, str]]:
    """Parse a table section (SML, SMF, or SME) of mzTab-M file."""
    headers = None
    data = []
    for line in lines:
        if line.startswith(header_prefix):
            headers = [
                x.strip().strip('"')
                for x in split_joined_str(line, "\t")[1:]
                if x and x.strip()
            ]
        elif line.startswith("COM"):
            parts = line.split("\t", maxsplit=1)
            if len(parts) < 2:
                continue
            if parts[1].strip():
                data.append(
                    {
                        "prefix": parts[0].strip(),
                        "msg": parts[1].strip(),
                    }
                )
        elif line.startswith(data_prefix) and headers:
            values = [
                x.strip().strip('"')
                for x in split_joined_str(line, "\t")[1:]
                if x and x.strip()
            ]
            if len(values) == len(headers):
                row = dict(zip(headers, values))
                data.append(row)
            else:
                raise ValueError(
                    f"Invalid number of values for headers: {headers} {values}"
                )

    return data


def parse_table_header(header: str) -> Dict[str, Any]:
    if not header:
        return {}
    header = header or ""
    columns = header.strip().split("\t")
    column_map = {}
    for column in columns:
        if column.startswith("opt_"):
            optional_column_name = column.replace("opt_", "", 1).strip('"')
            column_map[column] = (
                "opt",
                optional_column_name,
            )
        else:
            match = re.match(r"^\s*(.+)\s*\[\s*(\d+)\s*\]\s*$", column)
            if match:
                column_name, index = match.groups()
                column_map[column] = (column_name.strip('"'), int(index))
            else:
                column_map[column] = (column.strip('"'), None)
    return column_map


def split_file_sections(
    lines: List[str], context: Optional[SerializationContext] = None
) -> Dict[str, List[str]]:
    all_section_headers = {"SEH", "SME", "SFH", "SMF", "SMH", "SML", "MTD", "COM"}
    section_order: Dict[str, List[str]] = [
        ("MTD", [None, ("MTD", "COM"), ("SMH")]),
        ("SML", ["SMH", ("SMH", "SML", "COM"), ("SFH")]),
        ("SMF", ["SFH", ("SFH", "SMF", "COM"), ("SEH")]),
        ("SME", ["SEH", ("SEH", "SME", "COM"), None]),
    ]
    sections: Dict[str, List[str]] = {"MTD": [], "SML": [], "SMF": [], "SME": []}
    current_section = 0
    for idx, line in enumerate(lines, start=1):
        sanitized = line.strip()
        if not sanitized:
            continue
        if len(sanitized) < 4:
            if context:
                context.messages.append(
                    MzTabMessage(
                        category=Category.FORMAT,
                        type=MessageType.ERROR,
                        message=f"line error at {idx}: '{line}'",
                    )
                )
            continue
        line_header = sanitized[:3]
        if line_header not in all_section_headers:
            if context:
                context.messages.append(
                    MzTabMessage(
                        category=Category.FORMAT,
                        type=MessageType.ERROR,
                        message=f"line error at {idx}: '{line}'",
                    )
                )
            continue
        section, config = section_order[current_section]
        _, includes, terminators = config

        if terminators and line_header in terminators:
            current_section += 1
            section, config = section_order[current_section]
            _, includes, terminators = config

        if line_header in includes:
            sections[section].append(line)
    return sections


def update_table_dict(
    field_type: Type[BaseTableSection],
    summary_headers,
    rows: List[OrderedDict[str, Any]],
):
    new_table = []
    table_section_info = field_type.get_table_section_info()
    latest_row = None
    for row in rows:
        if row.get("prefix") == "COM" and latest_row:
            if "comment" not in latest_row:
                latest_row["comment"] = []
            latest_row["comment"].append(row)
            continue

        new_row = OrderedDict()
        for item, val in row.items():
            header, idx = summary_headers.get(item)
            item_type = table_section_info.data_types.get(header, None)
            is_list = table_section_info.list_fields.get(header, None)
            join_op = table_section_info.list_concatenation_str_dict.get(header, None)
            new_cell_data = None
            if is_list:
                if join_op:
                    new_cell_data = val if val and val != "null" else None
                    if new_cell_data:
                        new_cell_data = [
                            x if x and x != "null" else None
                            for x in split_joined_str(val, join_op)
                        ]

                        if isinstance(item_type, type) and issubclass(item_type, int):
                            new_cell_data = [
                                int(x) if x else None for x in new_cell_data
                            ]
                        elif isinstance(item_type, type) and issubclass(
                            item_type, float
                        ):
                            new_cell_data = [
                                float(x) if x else None for x in new_cell_data
                            ]
                else:
                    if isinstance(item_type, type) and issubclass(
                        item_type, MzTabBaseModel
                    ):
                        new_cell_data = None
                        if val and val != "null":
                            new_cell_data = val

                    elif isinstance(item_type, type) and issubclass(item_type, int):
                        new_cell_data = [int(val) if val and val != "null" else None]
                    elif isinstance(item_type, type) and issubclass(item_type, float):
                        try:
                            new_cell_data = (
                                [float(val)] if val and val != "null" else None
                            )
                        except ValueError:
                            logger.exception("Error parsing float value: %s", val)
                            new_cell_data = None
                    else:
                        new_cell_data = [val]
            else:
                if isinstance(item_type, type) and issubclass(
                    item_type, MzTabBaseModel
                ):
                    new_cell_data = None
                    if val and val != "null":
                        new_cell_data = val

                elif isinstance(item_type, type) and issubclass(item_type, int):
                    new_cell_data = (
                        int(val) if val is not None and val != "null" else None
                    )
                elif isinstance(item_type, type) and issubclass(item_type, float):
                    new_cell_data = None
                    if val and val.lower() != "null":
                        new_cell_data = (
                            float(val) if val.lower() != "nan" else float("nan")
                        )
                else:
                    if val and val.lower() != "null":
                        new_cell_data = val
                    else:
                        new_cell_data = None

            new_header, index = summary_headers[item]

            if index is None:
                new_row[new_header] = new_cell_data
            elif isinstance(index, int):
                if new_header not in new_row:
                    new_row[new_header] = []
                i = len(new_row[new_header])
                if i < index:
                    while i < index:
                        i += 1
                        new_row[new_header].append(None)
                if not new_cell_data:
                    new_row[new_header][index - 1] = None
                if isinstance(new_cell_data, list):
                    new_row[new_header][index - 1] = new_cell_data[0]
                else:
                    new_row[new_header][index - 1] = new_cell_data
            else:
                if new_header not in new_row:
                    new_row[new_header] = []
                match = re.match(
                    r"^(global|ms_run\[\d+\]|assay\[\d+\]|study_variable\[\d+\])_(.+)",
                    index,
                )
                if match:
                    identifier_parts = [match.group(1), match.group(2)]
                    new_identifier = identifier_parts[0]
                    accession = ""
                    cv_label = ""
                    term = ""
                    if identifier_parts[1].startswith("cv_"):
                        param_parts = identifier_parts[1].split("_", maxsplit=2)
                        cv_label = (
                            param_parts[1].split(":")[0]
                            if ":" in param_parts[1]
                            else ""
                        )
                        if len(param_parts) > 2:
                            accession = param_parts[1]
                            term = param_parts[2]
                        else:
                            accession = param_parts[1]
                            term = ""
                    else:
                        cv_label = ""
                        accession = ""
                        term = identifier_parts[1]
                    val = {}
                    val["param"] = {
                        "cv_label": cv_label,
                        "cv_accession": accession,
                        "name": term,
                    }
                    val["identifier"] = new_identifier
                    val["value"] = new_cell_data

                    new_row[new_header].append(val)
        latest_row = new_row
        new_table.append(new_row)
    return new_table


def check_ids(
    model: BaseModel,
    source: List[str | int],
    messages: List[MzTabMessage],
    in_list: bool = False,
):
    if isinstance(model, IdentifiableModel) and in_list:
        if model.id is None:
            reference = source.copy()
            reference.append("id")
            jsonpath = to_jsonpath(reference)
            messages.append(
                MzTabMessage(
                    message=f"{jsonpath} is missing",
                    category=Category.CROSS_CHECK,
                    message_type=MessageType.ERROR,
                    source=jsonpath,
                )
            )
            return

    for field in model.__class__.model_fields.keys():
        reference = source.copy()
        reference.append(field)
        val = getattr(model, field)
        if isinstance(val, list):
            for idx, item in enumerate(val):
                sub_reference = reference.copy()
                sub_reference.append(idx)
                if isinstance(item, IdentifiableModel):
                    check_ids(item, sub_reference, messages, True)
        elif isinstance(val, BaseModel):
            check_ids(val, reference, messages, False)


def parse_tsv_file(
    model_class: Type[BaseModel],
    data: Union[str, List[str]],
    context: SerializationContext,
) -> OrderedDict[str, Any]:
    lines = data
    if isinstance(data, str):
        lines = data.split("\n")
    if not lines:
        raise ValidationError("input content is empty")
    if not isinstance(lines, list):
        raise ValidationError("input format is not valid")
    if not isinstance(lines[0], str):
        raise ValidationError(f"input data is not valid: {data[0].__class__}")
    sections = split_file_sections(lines, context)
    mztabm = OrderedDict()
    mztabm["metadata"] = Metadata.parse_metadata(sections["MTD"], context)
    mztabm["comment"] = mztabm["metadata"].get("comment", None)
    section_inputs = [
        (SmallMoleculeSummary, "small_molecule_summary", "SMH", "SML"),
        (SmallMoleculeFeature, "small_molecule_feature", "SFH", "SMF"),
        (SmallMoleculeEvidence, "small_molecule_evidence", "SEH", "SME"),
    ]
    for section_class, section, header_prefix, data_prefix in section_inputs:
        if sections[data_prefix]:
            summary_map = parse_table_header(sections[data_prefix][0])
            summary_dict = parse_table_section(
                sections[data_prefix], header_prefix, data_prefix
            )

            field_info = model_class.model_fields.get(section)
            field_name = field_info.validation_alias or section

            mztabm[field_name] = update_table_dict(
                section_class, summary_map, summary_dict
            )

    return mztabm
