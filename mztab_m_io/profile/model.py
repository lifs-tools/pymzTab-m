from collections.abc import Mapping
import json
from pathlib import Path
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field, field_validator

from mztab_m_io.model.base import MzTabBaseModel
from mztab_m_io.profile.base import EnforcementLevel, JsonPath
from mztab_m_io.profile.constraints import (
    DEFAULT_CONSTRAINTS_MAP,
    Constraint,
    ConstraintGroup,
    DefaultConstraintType,
)


def populate_constraint_from_name(value):
    if value is None or isinstance(value, Constraint):
        return value
    if not isinstance(value, dict):
        return value

    constraint_type = value.get("type")
    if not constraint_type:
        return value

    constraint_class = DEFAULT_CONSTRAINTS_MAP.get(constraint_type)
    if not constraint_class:
        raise ValueError(f"Unknown value constraint type: {constraint_type}")

    constraint_data = dict(value)
    precondition = constraint_data.get("precondition")
    if precondition and isinstance(precondition, Mapping):
        evaluations = precondition.get("evaluations")
        if evaluations and isinstance(evaluations, list):
            for evaluation in precondition.get("evaluations", []):
                if isinstance(evaluation, Mapping) and evaluation.get("constraint"):
                    constraint = evaluation["constraint"]
                    evaluation["constraint"] = populate_constraint_from_name(constraint)

    if constraint_class == ConstraintGroup:
        constraint_data["constraints"] = [
            populate_constraint_from_name(constraint)
            for constraint in constraint_data.get("constraints", [])
        ]

    return constraint_class.model_validate(constraint_data)


class EnforcedRequirement(MzTabBaseModel):
    code: Annotated[
        Optional[str],
        Field(
            description="Requirement id. "
            "It is highly recommended to use unique code for each requirement"
        ),
    ] = None
    description: Annotated[
        Optional[str],
        Field(description="Description of requirement."),
    ] = None
    enforcement_level: Optional[EnforcementLevel] = EnforcementLevel.REQUIRED


class FieldRequirement(EnforcedRequirement):
    value_constraint: Optional[DefaultConstraintType] = None
    match_is_required: Optional[Optional[bool]] = None
    required_properties: Optional[list[str]] = None
    recommended_properties: Optional[list[str]] = None
    custom_constraints: Optional[list[str]] = None

    @field_validator("value_constraint", mode="before")
    @classmethod
    def populate_value_constraint(cls, value):
        return populate_constraint_from_name(value)


class FieldRequirementGroup(EnforcedRequirement):
    requirements: Annotated[
        list[Union[FieldRequirement, "FieldRequirementGroup"]],
        Field(min_length=1, description="List of constraints."),
    ]
    min_valid: Annotated[
        Optional[int],
        Field(
            description="Minimum number of constraints that must be true "
            "for the group to be true.",
            min=1,
        ),
    ] = None
    max_valid: Annotated[
        Optional[int],
        Field(
            description="Maximum number of constraints that can be true "
            "for the group to be true."
        ),
    ] = None


class ProfileValidatorDefinition(MzTabBaseModel):
    label: Annotated[
        str,
        Field(
            description="Label of the profile validator "
            "used to reference it in the profile."
        ),
    ]
    validator_id: Annotated[str, Field(description="Unique Id of profile validator.")]
    profile_validator_class: Annotated[
        str, Field(description="Full class name of profile validator.")
    ]
    description: Annotated[
        Optional[str],
        Field(
            description="Description of the custom validator.",
        ),
    ] = None


class MzTabMProfileConfiguration(MzTabBaseModel):
    supported_cv_lists: Annotated[
        Optional[list[str]],
        Field(description="Supported CV lists."),
    ] = None
    supported_cv_list_enforcement_level: Optional[EnforcementLevel] = None

    custom_validator_definitions: Annotated[
        Optional[list[ProfileValidatorDefinition]],
        Field(description="Supported custom validators."),
    ] = None
    default_validator_label: Annotated[
        Optional[str],
        Field(
            description="Label of validator used as default validator. "
            "If it is not defined, MzTabM default validator will be used."
        ),
    ] = None

    profile_validator_factory_class: Annotated[
        Optional[str],
        Field(
            description="Profile validator factory class. "
            "If it is not defined, default will be used."
        ),
    ] = None
    profile_validator_factory_class_arguments: Annotated[
        Optional[dict[str, Any]],
        Field(description="Key value arguments for profile factory class"),
    ] = None


class MzTabMProfile(MzTabBaseModel):
    id: Annotated[str, Field(description="Profile id.")]
    version: Annotated[str, Field(description="Profile version.")]
    name: Annotated[str, Field(description="Profile name.")]
    description: Annotated[
        Optional[str],
        Field(description="Profile description."),
    ] = None
    configuration: Annotated[
        Optional[MzTabMProfileConfiguration],
        Field(description="Profile configuration."),
    ] = None
    requirements: Annotated[
        Optional[dict[JsonPath, None | FieldRequirementGroup | FieldRequirement]],
        Field(description="Field requirements."),
    ] = None

    # value_constraints: Annotated[
    #     Optional[dict[JsonPath, ConstraintType | ConstraintGroup]],
    #     Field(description="Value constraints."),
    # ] = None
    @field_validator("requirements", mode="before")
    @classmethod
    def validate_requirements(cls, value):
        if value is None or not isinstance(value, dict):
            return value

        return {k: cls.create_requirement(v) for k, v in value.items()}

    def create_requirement(value: Any) -> FieldRequirementGroup | FieldRequirement:
        if (
            value is None
            or isinstance(value, FieldRequirement)
            or isinstance(value, FieldRequirementGroup)
            or not isinstance(value, dict)
        ):
            return value

        if "requirements" in value:
            return FieldRequirementGroup.model_validate(value, by_alias=True)
        else:
            return FieldRequirement.model_validate(value, by_alias=True)


if __name__ == "__main__":
    with Path("schema.json").open("w", encoding="utf-8") as f:
        json.dump(MzTabMProfile.model_json_schema(), f, indent=4)
