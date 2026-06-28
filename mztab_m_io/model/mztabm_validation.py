import re
from collections.abc import Sequence
from typing import Any, Dict, List, Mapping, Union

from pydantic import BaseModel

from mztab_m_io.model.serialization import (
    EnforcementLevel,
    IdentifiableModel,
)
from mztab_m_io.model.validation import (
    Category,
    MessageType,
    MzTabMessage,
)

MessageTypeMap: Dict[EnforcementLevel, MessageType] = {
    "optional": MessageType.INFO,
    "recommended": MessageType.WARNING,
    "required": MessageType.ERROR,
}


def to_jsonpath(reference: List[Union[str, int]]):
    if not reference:
        return "$"
    return "$." + ".".join([str(x) for x in reference])


def convert_full_path(full_path) -> str:
    path = str(full_path)
    path = path.replace(".[", "[")
    path = path.replace("(", "")
    path = path.replace(")", "")

    return f"$.{path}" if path else "$"


def is_non_string_container(value) -> bool:
    return isinstance(value, (Sequence, Mapping)) and not isinstance(
        value, (str, bytes, bytearray)
    )


def cross_check(model: BaseModel, messages: List[MzTabMessage]) -> List[MzTabMessage]:
    if messages is None:
        messages = []

    references = _get_reference_dict(model, messages)

    reference_hits = _check_referenced_items(model, references, messages)

    _check_unreferenced_items(reference_hits, messages)
    return messages


def _check_referenced_items(
    model: BaseModel,
    references: Dict[str, Dict[int, Any]],
    messages: List[MzTabMessage],
) -> Dict[str, Dict[int, int]]:
    reference_hits: Dict[str, Dict[int, int]] = {}
    for k, v in references.items():
        reference_hits[k] = dict.fromkeys(v.keys(), 0)

    for section, field, subfield, referenced_field in [
        ("metadata", "ms_run", "instrument_ref", "instrument"),
        ("metadata", "assay", "sample_ref", "sample"),
        ("metadata", "assay", "ms_run_refs", "ms_run"),
        ("metadata", "study_variable", "group_refs", "study_variable_group"),
        ("metadata", "study_variable", "assay_refs", "assay"),
        ("small_molecule_summary", None, "smf_id_refs", "small_molecule_feature"),
        ("small_molecule_feature", None, "sme_id_refs", "small_molecule_evidence"),
        ("small_molecule_evidence", "spectra_reference", "ms_run_ref", "ms_run"),
        ("small_molecule_summary", "opt", "identifier", "assay"),
        ("small_molecule_summary", "opt", "identifier", "ms_run"),
        ("small_molecule_summary", "opt", "identifier", "study_variable"),
        ("small_molecule_feature", "opt", "identifier", "assay"),
        ("small_molecule_feature", "opt", "identifier", "ms_run"),
        ("small_molecule_feature", "opt", "identifier", "study_variable"),
        ("small_molecule_evidence", "opt", "identifier", "assay"),
        ("small_molecule_evidence", "opt", "identifier", "ms_run"),
        ("small_molecule_evidence", "opt", "identifier", "study_variable"),
    ]:
        section_data = getattr(model, section, {})
        if not section_data:
            continue
        target = section_data
        field_ref = section
        targets = []
        if not isinstance(section_data, list):
            field_ref = field
            target = getattr(section_data, field, None)
            if not target:
                continue
            targets = [(None, target)]
        else:
            if field:
                targets = [
                    (idx, getattr(x, field)) for idx, x in enumerate(section_data)
                ]
            else:
                targets = [(idx, x) for idx, x in enumerate(section_data)]

        for target_idx, target in targets:
            if isinstance(target, list):
                for idx, list_item in enumerate(target):
                    if field == "opt":
                        field_ref_name = getattr(list_item, subfield)
                    else:
                        field_ref_name = (
                            f"{field_ref}[{idx}]"
                            if target_idx is None
                            else f"{field}[{target_idx}] {field_ref}[{idx}]"
                        )
                    _check_references(
                        references,
                        field_ref_name,
                        subfield,
                        referenced_field,
                        list_item,
                        reference_hits,
                        messages,
                    )
            elif target:
                field_ref_name = (
                    f"{field_ref}"
                    if field is None or target_idx is None
                    else f"{field}[{target_idx}] {field_ref}"
                )
                _check_references(
                    references,
                    field_ref_name,
                    subfield,
                    referenced_field,
                    target,
                    reference_hits,
                    messages,
                )
    # Reference in headers
    if "study_variable" in reference_hits:
        section_data = getattr(model, "small_molecule_summary", [])
        if section_data:
            for field in [
                "abundance_study_variable",
                "abundance_variation_study_variable",
            ]:
                length = len(getattr(section_data[0], field, []) or [])
                for idx in reference_hits["study_variable"]:
                    if idx is None:
                        continue
                    if idx <= length:
                        reference_hits["study_variable"][idx] += 1
    if "assay" in reference_hits:
        for section in ["small_molecule_summary", "small_molecule_feature"]:
            section_data = getattr(model, section, [])
            if section_data:
                length = len(getattr(section_data[0], "abundance_assay", []) or [])
                for idx in reference_hits["assay"]:
                    if idx is None:
                        continue
                    if idx <= length:
                        reference_hits["assay"][idx] += 1

    return reference_hits


def _check_unreferenced_items(
    reference_hits: Dict[str, Dict[int, int]],
    messages: List[MzTabMessage],
):
    for k, v in reference_hits.items():
        for idx, hit in v.items():
            if hit < 1:
                messages.append(
                    MzTabMessage(
                        category=Category.CROSS_CHECK,
                        message_type=MessageType.WARNING,
                        message=f"{k}[{idx}] is not referenced in the file",
                        source=f"{k}[{idx}]",
                    )
                )


def _get_reference_dict(
    model: BaseModel, messages: List[MzTabMessage], metadata_field_name="metadata"
) -> Dict[str, Dict[int, Any]]:
    references: Dict[str, Dict[int, Any]] = {}
    metadata = getattr(model, metadata_field_name)
    if not metadata:
        messages.append(
            MzTabMessage(
                category=Category.CROSS_CHECK,
                message_type=MessageType.ERROR,
                message="metadata is not defined",
            )
        )
    if metadata:
        for indexed_field in [
            "assay",
            "instrument",
            "sample",
            "ms_run",
            "study_variable",
            "study_variable_group",
        ]:
            vals = getattr(metadata, indexed_field)
            if not vals:
                continue
            references[indexed_field] = {}
            for idx, item in enumerate(vals):
                if isinstance(item, IdentifiableModel):
                    references[indexed_field][item.id] = item
                else:
                    messages.append(
                        MzTabMessage(
                            category=Category.CROSS_CHECK,
                            message_type=MessageType.WARNING,
                            message=f"metadata {indexed_field} item at index {idx} "
                            f"is not valid {str(item)}",
                        )
                    )

    for section, indexed_field in [
        ("small_molecule_evidence", "sme_id"),
        ("small_molecule_feature", "smf_id"),
    ]:
        references[section] = {}
        items = getattr(model, section)
        if not items:
            continue

        for item in items:
            val = getattr(item, indexed_field)
            references[section][val] = item
    return references


def _check_references(
    references: Dict[str, Dict[int, Any]],
    field_ref: str,
    subfield: str,
    referenced_field: str,
    target: BaseModel,
    reference_hits: Dict[str, Dict[int, Any]],
    messages: List[MzTabMessage],
):
    subfield_vals = getattr(target, subfield)
    indexed_items = references.get(referenced_field, {})
    if isinstance(subfield_vals, list):
        for i, idx in enumerate(subfield_vals):
            if idx in indexed_items:
                reference_hits[referenced_field][idx] += 1
            else:
                messages.append(
                    MzTabMessage(
                        category=Category.CROSS_CHECK,
                        message_type=MessageType.WARNING,
                        message=f"{field_ref} -> {subfield}[{i}] value "
                        f"{referenced_field}[{idx}] is not defined.",
                    )
                )
    elif isinstance(subfield_vals, str) and subfield_vals.startswith(referenced_field):
        match = re.match(referenced_field + r"\[(\d+)\]", subfield_vals)
        if match:
            idx = int(match.group(1))
            if idx in indexed_items:
                reference_hits[referenced_field][idx] += 1
            else:
                messages.append(
                    MzTabMessage(
                        category=Category.CROSS_CHECK,
                        message_type=MessageType.WARNING,
                        message=f"{field_ref} -> {subfield} value "
                        f"{referenced_field}[{idx}] is not defined ",
                    )
                )
    elif isinstance(subfield_vals, int):
        idx = subfield_vals
        if idx in indexed_items:
            reference_hits[referenced_field][idx] += 1
        else:
            messages.append(
                MzTabMessage(
                    category=Category.CROSS_CHECK,
                    message_type=MessageType.WARNING,
                    message=f"{field_ref} -> {subfield} value "
                    f"{referenced_field}[{idx}] is not defined ",
                )
            )
