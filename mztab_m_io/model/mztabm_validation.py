import datetime
import re
from typing import Any, Dict, List, Union

import email_validator
from pydantic import AnyUrl, BaseModel

from mztab_m_io.model.serialization import (
    EnforcementLevel,
    IdentifiableModel,
    MetadataSerialization,
    ValidationPolicy,
    ValueConstraint,
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


def check_validation_policies(
    reference: List[Union[str, int]],
    model: BaseModel,
    messages: List[MzTabMessage],
) -> List[MzTabMessage]:
    if isinstance(model, str):
        pass
    for field, field_info in model.__class__.model_fields.items():
        val = getattr(model, field)
        # label = field_info.validation_alias or field
        new_ref = reference.copy()
        new_ref.append(field)
        extra = field_info.json_schema_extra or {}
        json_extra = MetadataSerialization.model_validate(extra, by_alias=True)
        policies = []
        if isinstance(json_extra.validation_policy, list):
            policies = json_extra.validation_policy
        elif isinstance(json_extra.validation_policy, ValidationPolicy):
            policies = [json_extra.validation_policy]
        for policy in policies:
            message_type = MessageTypeMap.get(policy.enforcement_level, "required")
            enforcement = policy.enforcement_level or "required"
            if policy.required and not val:
                item_ref = new_ref.copy()
                messages.append(
                    MzTabMessage(
                        code="",
                        category=Category.CROSS_CHECK,
                        message_type=message_type,
                        message=f"'{to_jsonpath(item_ref)}' is {enforcement}.",
                        source=to_jsonpath(item_ref),
                    )
                )
            if policy.value_constraint and val is not None:
                if isinstance(val, list):
                    for idx, item in enumerate(val):
                        match = _check_value_constraint(policy.value_constraint, item)
                        if not match:
                            list_ref = new_ref.copy()
                            list_ref.append(idx)
                            messages.append(
                                MzTabMessage(
                                    code="",
                                    category=Category.CROSS_CHECK,
                                    message_type=message_type,
                                    message=f"'{to_jsonpath(list_ref)}' value "
                                    f"constraint violation. "
                                    f"Expected value format {policy.value_constraint}. "
                                    f"Current value: {item}",
                                    source=to_jsonpath(list_ref),
                                )
                            )
                elif isinstance(val, str):
                    match = _check_value_constraint(policy.value_constraint, val)
                    if not match:
                        item_ref = new_ref.copy()
                        messages.append(
                            MzTabMessage(
                                code="",
                                category=Category.CROSS_CHECK,
                                message_type=message_type,
                                message=f"'{to_jsonpath(item_ref)}' value "
                                f"constraint violation. "
                                f"Expected value format {policy.value_constraint}. "
                                f"Current value: {val}",
                                source=to_jsonpath(item_ref),
                            )
                        )
            if policy.pattern and val is not None:
                if isinstance(val, list):
                    for idx, item in enumerate(val):
                        match = re.match(policy.pattern, item)
                        if not match:
                            list_ref = new_ref.copy()
                            list_ref.append(idx)
                            messages.append(
                                MzTabMessage(
                                    code="",
                                    category=Category.CROSS_CHECK,
                                    message_type=message_type,
                                    message=f"'{to_jsonpath(list_ref)}' pattern "
                                    f"match violation. "
                                    f"Expected pattern {policy.pattern}",
                                    source=to_jsonpath(list_ref),
                                )
                            )
                elif isinstance(val, str):
                    match = re.match(policy.pattern, val)
                    if not match:
                        item_ref = new_ref.copy()
                        messages.append(
                            MzTabMessage(
                                code="",
                                category=Category.CROSS_CHECK,
                                message_type=message_type,
                                message=f"'{to_jsonpath(item_ref)}' pattern "
                                f"match violation."
                                f"Expected pattern is {policy.pattern}",
                                source=to_jsonpath(item_ref),
                            )
                        )
            minimum_violation = False
            if policy.minimum and val is not None:
                if isinstance(val, (str, list)):
                    if val and len(val) < policy.minimum:
                        minimum_violation = True
                elif isinstance(val, int):
                    if val < policy.minimum:
                        minimum_violation = True
            if minimum_violation:
                item_ref = new_ref.copy()
                messages.append(
                    MzTabMessage(
                        code="",
                        category=Category.CROSS_CHECK,
                        message_type=message_type,
                        message=f"'{to_jsonpath(item_ref)}' min length violation. "
                        f"Expected minimum length is {policy.minimum}",
                        source=to_jsonpath(item_ref),
                    )
                )
            maximum_violation = False
            if policy.maximum and val is not None:
                if isinstance(val, (str, list)):
                    if val and len(val) > policy.maximum:
                        maximum_violation = True
                elif isinstance(val, int):
                    if val > policy.maximum:
                        maximum_violation = True
            if maximum_violation:
                item_ref = new_ref.copy()
                messages.append(
                    MzTabMessage(
                        code="",
                        category=Category.CROSS_CHECK,
                        message_type=message_type,
                        message=f"'{to_jsonpath(item_ref)}' max length violation. "
                        f"Expected minimum length is {policy.max}",
                        source=to_jsonpath(item_ref),
                    )
                )

        if isinstance(val, BaseModel):
            check_validation_policies(new_ref.copy(), val, messages)
        elif isinstance(val, list):
            for idx, item in enumerate(val):
                if isinstance(item, BaseModel):
                    list_ref = new_ref.copy()
                    list_ref.append(idx)
                    check_validation_policies(list_ref.copy(), item, messages)


def cross_check(model: BaseModel, messages: List[MzTabMessage]) -> List[MzTabMessage]:
    if messages is None:
        messages = []

    references = _get_reference_dict(model, messages)

    reference_hits = _check_referenced_items(model, references, messages)

    _check_unreferenced_items(reference_hits, messages)
    return messages


def _check_value_constraint(constraint: ValueConstraint, value: Union[str, int, float]):
    if value is None or (isinstance(value, str) and not value):
        return True
    if constraint == "any-url":
        try:
            AnyUrl(value)
            return True
        except Exception:
            return False

    if constraint == "positive-integer":
        if isinstance(value, int) and value > 0:
            return True
        return False
    if constraint == "non-negative-integer":
        if isinstance(value, int) and value >= 0:
            return True
        return False

    if constraint == "curie":
        if isinstance(value, str) and len(value.split(":")) == 2:
            return True
        return False

    if constraint == "datetime":
        try:
            datetime.datetime.fromisoformat(value)
            return True
        except Exception:
            return False

    if constraint == "date":
        try:
            datetime.datetime.strptime(value, "YYYY-MM-DD")
            return True
        except Exception:
            return False

    if constraint == "email":
        try:
            email_validator.validate_email(value)
            return True
        except email_validator.EmailNotValidError:
            return False


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
        ("small_molecule_evidence", "spectra_references", "ms_run_ref", "ms_run"),
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
