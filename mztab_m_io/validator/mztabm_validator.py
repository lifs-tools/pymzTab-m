import json
import logging
from collections.abc import Mapping
from importlib.resources import files
from pathlib import Path
from typing import Annotated, Any

from jsonpath_ng import parse
from pydantic import BaseModel, Field

import mztab_m_io
from mztab_m_io.model.mztabm_validation import convert_full_path
from mztab_m_io.profile.base import EnforcementLevel, JsonPath
from mztab_m_io.profile.constraints import Constraint
from mztab_m_io.profile.model import (
    FieldRequirement,
    FieldRequirementGroup,
    MzTabMProfile,
)
from mztab_m_io.validator.base import (
    ConstraintChecker,
    DefaultProfileValidatorFactory,
    ProfileValidator,
    ProfileValidatorFactory,
    ProfileValidatorLoader,
)

logger = logging.getLogger(__name__)


class MzTabMValidationMessage(BaseModel):
    code: None | str = None
    source: JsonPath
    name: str
    enforcement_level: EnforcementLevel
    message: str = ""


class MzTabMValidationResult(BaseModel):
    errors: dict[JsonPath, list[MzTabMValidationMessage]]
    recommendations: dict[JsonPath, list[MzTabMValidationMessage]]
    optionals: dict[JsonPath, list[MzTabMValidationMessage]]


class MzTabMValidator:
    def __init__(
        self,
        profile: Annotated[
            None | str | Path | dict | MzTabMProfile,
            Field(
                description="MzTabM profile file path or dictionary."
                " If it is not defined, default profile will be used."
            ),
        ] = None,
    ):
        self.json_path_expressions: dict[JsonPath, Any] = {}
        self.profiles: dict[str, MzTabMProfile] = {}

        self.mztabm_profile = None
        if isinstance(profile, str):
            profile = Path(profile)
        if profile is None or isinstance(profile, Path):
            if profile and not profile.exists():
                raise ValueError("MzTab-M profile file does not exist.")
            self.mztabm_profile = self.get_profile(profile)
        elif isinstance(profile, dict):
            self.mztabm_profile = MzTabMProfile.model_validate(profile, by_alias=True)
        if isinstance(profile, MzTabMProfile):
            self.mztabm_profile = profile
        if not isinstance(self.mztabm_profile, MzTabMProfile):
            raise ValueError("Profile is not valid")

        custom_validator_definitions = None
        self.default_profile_validator_id = None
        if self.mztabm_profile.configuration:
            config = self.mztabm_profile.configuration
            custom_validator_definitions = config.custom_validator_definitions or []
            labels = {x.label: x for x in custom_validator_definitions}
            default_label = config.default_validator_label
            default_validator_definition = labels.get(default_label)
            self.default_profile_validator_id = (
                default_validator_definition.validator_id
                if default_validator_definition
                else None
            )

        if (
            not self.mztabm_profile.configuration
            or not self.mztabm_profile.configuration.profile_validator_factory_class
        ):
            profile_validator_factory = DefaultProfileValidatorFactory(
                custom_validator_definitions=custom_validator_definitions,
                default_profile_validator_id=self.default_profile_validator_id,
            )
        else:
            config = self.mztabm_profile.configuration
            kwargs = config.profile_validator_factory_class_arguments or {}
            profile_validator_factory = (
                ProfileValidatorFactory.get_profile_validator_factory(
                    config.profile_validator_factory_class,
                    custom_validator_definitions=custom_validator_definitions,
                    default_profile_validator_id=self.default_profile_validator_id,
                    **kwargs,
                )
            )
        self.profile_validator_factory = profile_validator_factory

    def append_message(
        self,
        messages: dict[JsonPath, list[MzTabMValidationMessage]],
        json_path: JsonPath,
        message: MzTabMValidationMessage,
    ):
        if json_path not in messages:
            messages[json_path] = []
        messages.get(json_path).append(message)

    def validate_mztabm_file(
        self,
        mztabm_file_path: str | Path,
    ) -> MzTabMValidationResult:
        if isinstance(mztabm_file_path, str):
            mztabm_file_path = Path(mztabm_file_path)

        if not mztabm_file_path.exists():
            raise ValueError("MzTab-M file does not exist.")

        input_json = json.loads(mztabm_file_path.read_text())

        return self.validate_mztabm_json(input_json)

    def get_profile(self, profile_file_path: None | Path = None):
        if profile_file_path in self.profiles:
            logger.info("Profile is found for %s", profile_file_path)
            return self.profiles[profile_file_path]
        mztabm_version = "2.1.0-M"
        logger.info("Default profile will be loaded.")
        with (
            files(mztab_m_io.__name__)
            .joinpath(
                f"resources/profiles/mztabm-default-profile-{mztabm_version}.json"
            )
            .open("r") as f
        ):
            default_profile_json = json.loads(f.read())
            default_profile = MzTabMProfile.model_validate(default_profile_json)
        input_profile = None
        if profile_file_path:
            profile_json = json.loads(profile_file_path.read_text())
            input_profile = MzTabMProfile.model_validate(profile_json)
            # merge with default profile.
            # Override keys if they exist in default
            # Delete keys if there is no value

            new_requirements = input_profile.requirements
            input_profile.requirements = default_profile.requirements
            for key, value in new_requirements.items():
                new_codes = self.get_codes(value)
                if key in input_profile.requirements:
                    old_codes = self.get_codes(input_profile.requirements[key])
                    if value is None:
                        del input_profile.requirements[key]
                        logger.info(
                            "Deleted: Dropped profile requirement(s) for '%s': %s",
                            key,
                            old_codes,
                        )
                    else:
                        logger.info(
                            "Overridden: "
                            "Requirement updates for '%s'. old codes: %s, new: %s",
                            key,
                            old_codes,
                            new_codes,
                        )

                else:
                    logger.info(
                        "Added: New profile requirement(s) for '%s': %s ",
                        key,
                        new_codes,
                    )
                input_profile.requirements[key] = value
        profile = input_profile or default_profile
        self.profiles[profile_file_path or ""] = profile
        return profile

    def validate_mztabm_json(self, input_json: dict):
        result = self.validate_mztabm_json_with_profile(input_json=input_json)

        return self.process_messages(result)

    def get_codes(self, value: FieldRequirement | FieldRequirementGroup):
        requirement_codes = []
        if value:
            if isinstance(value, FieldRequirement):
                requirement_codes = [value.code] if value.code else ""
            else:
                requirement_codes = [x.code for x in value.requirements if x.code]
        requirement_codes_str = ", ".join(requirement_codes)
        return requirement_codes_str

    def validate_mztabm_json_with_profile(
        self,
        input_json: dict,
    ) -> dict[JsonPath, list[MzTabMValidationMessage]]:
        messages: dict[JsonPath, list[MzTabMValidationMessage]] = {}
        for (
            json_path,
            requirement_definition,
        ) in self.mztabm_profile.requirements.items():
            if not requirement_definition:
                logger.info(
                    "Skipping key. Field requirement is not defined for '%s'", json_path
                )
                continue
            requirement_group = None
            if isinstance(requirement_definition, FieldRequirement):
                requirement_group = FieldRequirementGroup(
                    requirements=[requirement_definition]
                )
            elif isinstance(requirement_definition, FieldRequirementGroup):
                requirement_group = requirement_definition
            else:
                raise ValueError(
                    f"Invalid requirement type: {type(requirement_definition)}"
                )
            if not json_path:
                logger.info("Field key is not defined. $ will be used.")
                json_path = "$"
            for field_requirement in requirement_group.requirements:
                self.validate_requirement(
                    field_requirement=field_requirement,
                    json_path=json_path,
                    input_json=input_json,
                    messages=messages,
                )
        return messages

    def validate_requirement(
        self,
        field_requirement: FieldRequirement,
        json_path: JsonPath,
        input_json: dict,
        messages: dict[JsonPath, list[MzTabMValidationMessage]],
    ):
        jsonpath_expr = self.json_path_expressions.get(json_path)
        if not jsonpath_expr:
            jsonpath_expr = parse(json_path)
            self.json_path_expressions[json_path] = jsonpath_expr

        matches = jsonpath_expr.find(input_json)
        if not matches:
            if field_requirement.match_is_required:
                self.append_message(
                    messages=messages,
                    json_path=json_path,
                    message=MzTabMValidationMessage(
                        code=field_requirement.code,
                        source=json_path,
                        name=field_requirement.value_constraint.type,
                        enforcement_level=field_requirement.enforcement_level,
                        message=f"There is no value with json path '{json_path}'",
                    ),
                )
        else:
            for x in matches or []:
                source = convert_full_path(x.full_path)
                if (
                    field_requirement.required_properties
                    or field_requirement.recommended_properties
                ) and not isinstance(x.value, Mapping):
                    self.append_message(
                        messages=messages,
                        json_path=source,
                        message=MzTabMValidationMessage(
                            code=field_requirement.code,
                            source=source,
                            name="Property check failed",
                            enforcement_level=EnforcementLevel.REQUIRED,
                            message=f"Property check failed. '{source}' is not object.",
                        ),
                    )
                else:
                    for field in field_requirement.required_properties or []:
                        if field not in x.value:
                            self.append_message(
                                messages=messages,
                                json_path=source,
                                message=MzTabMValidationMessage(
                                    code=field_requirement.code,
                                    source=source,
                                    name="Required property does not exist",
                                    enforcement_level=EnforcementLevel.REQUIRED,
                                    message=f"{field} is not in object '{source}'",
                                ),
                            )
                    for field in field_requirement.recommended_properties or []:
                        if field not in x.value:
                            self.append_message(
                                messages=messages,
                                json_path=source,
                                message=MzTabMValidationMessage(
                                    code=field_requirement.code,
                                    source=source,
                                    name="Recommended property does not exist",
                                    enforcement_level=EnforcementLevel.RECOMMENDED,
                                    message=f"{field} is not in object '{source}'",
                                ),
                            )

                if field_requirement.value_constraint:
                    constraint = field_requirement.value_constraint
                    checker = self.profile_validator_factory.get_checker(constraint)
                    sub_jsonpath = field_requirement.value_constraint.json_path
                    sub_input_value = x.value
                    if sub_jsonpath:
                        if not sub_jsonpath.startswith("$"):
                            sub_jsonpath = f"${sub_jsonpath}"
                        sub_jsonpath_expr = self.json_path_expressions.get(sub_jsonpath)
                        if not sub_jsonpath_expr:
                            sub_jsonpath_expr = parse(sub_jsonpath)
                            self.json_path_expressions[sub_jsonpath] = sub_jsonpath_expr

                        sub_input_value = [
                            a.value for a in sub_jsonpath_expr.find(x.value)
                        ]
                        if len(sub_input_value) == 1:
                            sub_input_value = sub_input_value[0]
                        elif len(sub_input_value) == 0:
                            sub_input_value = None

                    res = checker.validate_constraint(
                        constraint=field_requirement.value_constraint,
                        value=sub_input_value,
                        root=input_json,
                        config=self.mztabm_profile.configuration,
                    )
                    if not res.is_valid:
                        self.append_message(
                            messages=messages,
                            json_path=source,
                            message=MzTabMValidationMessage(
                                code=field_requirement.code,
                                source=source,
                                name=field_requirement.value_constraint.type,
                                enforcement_level=field_requirement.enforcement_level,
                                message=res.message,
                            ),
                        )

    def process_messages(self, messages: dict[JsonPath, list[MzTabMValidationMessage]]):
        errors = {}
        recommendations = {}
        optionals = {}
        for k, v in messages.items():
            for x in v:
                for level, items in [
                    (EnforcementLevel.REQUIRED, errors),
                    (EnforcementLevel.RECOMMENDED, recommendations),
                    (EnforcementLevel.OPTIONAL, optionals),
                ]:
                    if level == x.enforcement_level:
                        if k not in items:
                            items[k] = []
                        items[k].append(x)

        # for k, v in errors.items():
        #     for x in v:
        #         logger.error(
        #             "%s\t%s\t%s\t%s", x.enforcement_level.value, k, x.name, x.message
        #         )
        return MzTabMValidationResult(
            errors=errors, recommendations=recommendations, optionals=optionals
        )
