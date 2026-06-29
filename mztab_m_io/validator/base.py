import abc
import importlib
import logging
from typing import Any, Literal, Optional, Tuple

import jsonpath_ng

from mztab_m_io.model import MzTabBaseModel
from mztab_m_io.profile.base import JsonPath
from mztab_m_io.profile.constraints import (
    Constraint,
    CustomConstraint,
    DecimalConstraint,
    ValidationRuntimeConfiguration,
)
from mztab_m_io.profile.model import (
    MzTabMProfileConfiguration,
    ProfileValidatorDefinition,
)
from mztab_m_io.validator.opa_engine import OpaEngineFactory

logger = logging.getLogger(__name__)


class ConstraintValidationResult(MzTabBaseModel):
    is_valid: bool
    message: Optional[str] = None


class ProfileValidator(abc.ABC):
    def __init__(self, profile_validator_factory: "ProfileValidatorFactory"):
        self.profile_validator_factory = profile_validator_factory

    @abc.abstractmethod
    def get_id(self) -> str: ...

    @abc.abstractmethod
    def get_checker(self, constraint: Constraint) -> Optional["ConstraintChecker"]: ...

    @abc.abstractmethod
    def get_checker_by_name(
        self, constraint_type: str, constraint_name: Optional[str] = None
    ) -> Optional["ConstraintChecker"]: ...

    @abc.abstractmethod
    def register_checker(
        self,
        constraint_type: str,
        checker: "ConstraintChecker",
        constraint_name: Optional[str] = None,
    ) -> None: ...

    @staticmethod
    def get_registered_profile_checkers(
        validator_id: None | str = None,
    ) -> dict[tuple[str, str], type["ConstraintChecker"]]:
        return REGISTERED_PROFILE_CHECKER_CLASSES.get(validator_id or None) or {}


class DefaultProfileValidator(ProfileValidator):
    def __init__(self, profile_validator_factory: "ProfileValidatorFactory"):
        super().__init__(profile_validator_factory=profile_validator_factory)
        self._registry: dict[tuple[str, str], type[ConstraintChecker]] = {}
        self._checkers: dict[tuple[str, str], ConstraintChecker] = {}
        checkers = self.get_registered_profile_checkers(self.get_id())
        for (constraint_type, name), checker in checkers.items():
            self.register_checker(
                constraint_type=constraint_type, constraint_name=name, checker=checker
            )

    def get_id(self) -> str:
        return MZTABM_DEFAULT_VALIDATOR_ID

    def get_checker(self, constraint: Constraint) -> Optional["ConstraintChecker"]:
        return self.get_checker_by_name(
            constraint_type=constraint.type, constraint_name=constraint.name
        )

    def get_checker_by_name(
        self, constraint_type: str, constraint_name: Optional[str]
    ) -> Optional["ConstraintChecker"]:
        key = (constraint_type, constraint_name or None)
        checker_class = self._registry.get(key)
        if checker_class:
            checker = self._checkers.get(key)
            if not checker:
                checker = checker_class()
                checker.profile_validator_factory = self.profile_validator_factory
                checker.constraint_type = constraint_type
                checker.constraint_name = constraint_type
                checker.validator_id = self.get_id()
                self._checkers[key] = checker
            return checker
        else:
            raise ValueError(
                f"There is no checker class for '{constraint_type}, {constraint_name}'"
            )

    def register_checker(
        self,
        constraint_type: str,
        constraint_name: str,
        checker: type["ConstraintChecker"],
    ) -> None:
        # constraint_type = constraint_class.model_fields.get("type").default
        self._registry[(constraint_type, constraint_name)] = checker

    def unregister_checker(self, checker: "ConstraintChecker") -> None:
        matches = [k for k, v in self._registry if v == checker.__class__]
        for key in matches or []:
            del self._registry[key]
        matches = [k for k, v in self._checkers if v == checker]
        for key in matches or []:
            del self._checkers[key]


class ProfileValidatorLoader:
    def __init__(
        self, validator_definitions: None | list[ProfileValidatorDefinition] = None
    ):
        self.loaded_validators: dict[str, ProfileValidator] = {}
        self.validator_definitions = validator_definitions
        for definition in self.validator_definitions or []:
            self.load_validator(definition)

    def load_validator(
        self, definition: ProfileValidatorDefinition
    ) -> ProfileValidator:
        parts = definition.profile_validator_class.split(".")
        class_name = parts[-1]
        module_name = parts[:-1]
        try:
            module_object = importlib.import_module(module_name)
            target_class = getattr(module_object, class_name)

        except Exception as ex:
            message = f"Error while loading {module_name}.{class_name}: {ex}"
            logger.error(message)
            raise ValueError(message)
        if not issubclass(target_class, ProfileValidator):
            message = f"Class {module_name}.{class_name} is not ProfileValidator class"
            logger.error(message)
            raise ValueError(message)
        instance = target_class()
        self.loaded_validators[definition.validator_id] = instance
        return instance


class ProfileValidatorFactory(abc.ABC):
    def __init__(
        self,
        custom_validator_definitions: Optional[list[ProfileValidatorDefinition]] = None,
        default_profile_validator_id: Optional[str] = None,
        opa_engine_factory: Optional[OpaEngineFactory] = None,
        **kwargs,
    ):
        self.custom_validator_definitions = custom_validator_definitions or []
        self.default_profile_validator_id = default_profile_validator_id
        self.opa_engine_factory = opa_engine_factory
        self.kwargs = kwargs

    @abc.abstractmethod
    def get_validator_by_label(self, label: str) -> Optional[ProfileValidator]: ...

    @abc.abstractmethod
    def get_validator_by_id(self, validator_id: str) -> Optional[ProfileValidator]: ...

    @abc.abstractmethod
    def get_checker(self, constraint: Constraint) -> Optional["ConstraintChecker"]: ...

    def get_checker_by_name(
        self,
        constraint_type: str,
        constraint_name: Optional[str] = None,
        validator_id: Optional[str] = None,
    ) -> Optional["ConstraintChecker"]: ...

    @abc.abstractmethod
    def register_profile_validator(
        self,
        definition: ProfileValidatorDefinition,
        default: bool = False,
    ) -> ProfileValidator: ...

    @abc.abstractmethod
    def unregister_profile_validator(self, validator_id: str) -> ProfileValidator: ...

    @staticmethod
    def get_profile_validator_factory(
        factory_class: str,
        custom_validator_definitions: Optional[list[ProfileValidatorDefinition]] = None,
        default_profile_validator_id: Optional[str] = None,
        **kwargs,
    ) -> "ProfileValidatorFactory":
        parts = factory_class.split(".")
        class_name = parts[-1]
        module_name = parts[:-1]
        try:
            module_object = importlib.import_module(module_name)
            target_class = getattr(module_object, class_name)

        except Exception as ex:
            message = f"Error while loading {module_name}.{class_name}: {ex}"
            logger.error(message)
            raise ValueError(message)
        if not issubclass(target_class, "ProfileValidatorFactory"):
            message = (
                f"Class {module_name}.{class_name} is not ProfileValidatorFactory class"
            )
            logger.error(message)
            raise ValueError(message)
        instance = target_class(
            custom_validator_definitions=custom_validator_definitions,
            default_profile_validator_id=default_profile_validator_id,
            **kwargs,
        )
        return instance


class DefaultProfileValidatorFactory(ProfileValidatorFactory):
    def __init__(
        self,
        custom_validator_definitions: Optional[list[ProfileValidatorDefinition]] = None,
        default_profile_validator_id: Optional[str] = None,
        validator_loader: None | ProfileValidatorLoader = None,
        opa_engine_factory: Optional[OpaEngineFactory] = None,
        **kwargs,
    ):
        super().__init__(
            custom_validator_definitions=custom_validator_definitions,
            default_profile_validator_id=default_profile_validator_id,
            opa_engine_factory=opa_engine_factory,
            **kwargs,
        )
        if not validator_loader:
            validator_loader = ProfileValidatorLoader(
                validator_definitions=custom_validator_definitions
            )
        self._validator_definitions = {
            x.validator_id: x for x in custom_validator_definitions or []
        }
        self._profile_validators: dict[str, ProfileValidator] = {}
        self._validator_labels = {}
        self._validator_ids_by_label = {}

        self.validator_loader = validator_loader
        base = DefaultProfileValidator(profile_validator_factory=self)
        self._profile_validators[base.get_id()] = base
        base_label = ""
        self._validator_definitions[self.default_profile_validator_id] = (
            ProfileValidatorDefinition(
                label=base_label,
                validator_id=base.get_id(),
                profile_validator_class=DefaultProfileValidator.__module__
                + "."
                + DefaultProfileValidator.__name__,
            )
        )
        self._validator_labels[self.default_profile_validator_id] = base_label
        self._validator_ids_by_label[base_label] = self.default_profile_validator_id
        if not default_profile_validator_id:
            self.default_profile_validator_id = base.get_id()

        for definition in self.custom_validator_definitions:
            default = self.default_profile_validator_id == definition.validator_id
            self.register_profile_validator(definition=definition, default=default)

        # for validator_id, checkers in self.initial_checker_classes.items():

    def get_validator_by_label(self, label: None | str) -> None | ProfileValidator:
        if not label:
            validator_id = self.default_profile_validator_id
        else:
            validator_id = self._validator_ids_by_label.get(label)
        profile_validator = self._profile_validators.get(validator_id)
        if not profile_validator:
            definition = self._validator_definitions.get(validator_id)
            if definition:
                validator = self.validator_loader.load_validator(definition)
                self._profile_validators[definition.validator_id] = validator
                self._validator_labels[definition.validator_id] = definition.label
                self._validator_ids_by_label[definition.label] = definition.validator_id

                profile_validator = validator
        return profile_validator

    def get_validator_by_id(self, validator_id: str) -> None | ProfileValidator:
        if not validator_id:
            validator_id = self.default_profile_validator_id

        profile_validator = self._profile_validators.get(validator_id)
        if not profile_validator:
            definition = self._validator_definitions.get(validator_id)
            if definition:
                validator = self.validator_loader.load_validator(definition)
                self._profile_validators[definition.validator_id] = validator
                self._validator_labels[definition.validator_id] = definition.label
                self._validator_ids_by_label[definition.label] = definition.validator_id

                profile_validator = validator
        return profile_validator

    def get_checker(self, constraint: Constraint) -> Optional["ConstraintChecker"]:
        validator = self.get_validator_by_id(validator_id=constraint.validator)
        if not validator:
            raise ValueError(f"Validator is not found for {constraint.validator}")
        return validator.get_checker(constraint=constraint)

    def get_checker_by_name(
        self,
        constraint_type: str,
        constraint_name: Optional[str] = None,
        validator_id: Optional[str] = None,
    ) -> Optional["ConstraintChecker"]:
        validator = self.get_validator_by_id(validator_id=validator_id)
        if not validator:
            raise ValueError(f"Validator is not found for {validator_id}")
        return validator.get_checker_by_name(
            constraint_type=constraint_type, constraint_name=constraint_name
        )

    def register_profile_validator(
        self,
        definition: ProfileValidatorDefinition,
        default: bool = False,
    ) -> ProfileValidator:
        profile_validator = self.validator_loader.load_validator(definition)
        self._profile_validators[definition.validator_id] = profile_validator
        self._validator_labels[definition.validator_id] = definition.label
        self._validator_ids_by_label[definition.label] = definition.validator_id
        logger.info(
            "%s name: %s class: %s is registered",
            definition.label,
            definition.validator_id,
            definition.profile_validator_class,
        )
        if default:
            self.default_profile_validator_id = definition.validator_id

        return profile_validator

    def unregister_profile_validator(self, validator_id: str) -> ProfileValidator:
        definition = self._validator_definitions.get(validator_id)
        if validator_id in self._profile_validators:
            del self._profile_validators[validator_id]
        if validator_id in self._validator_labels:
            del self._validator_labels[validator_id]
        if definition and definition.label in self._validator_ids_by_label:
            del self._validator_ids_by_label[definition.label]


class ConstraintChecker(abc.ABC):
    validator_id: str | None = None
    name: str | None = None

    is_active: bool = True

    def __init__(self):
        self.constraint_type = None
        self.profile_validator_factory: ProfileValidatorFactory = None
        self.constraint_name = None
        self._json_path_expressions: dict[JsonPath, Any] = {}

    @abc.abstractmethod
    def validate(
        self,
        constraint: Constraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
        runtime_config: None | ValidationRuntimeConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        raise NotImplementedError

    def evaluate_precondition(
        self,
        constraint: Constraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
        runtime_config: None | ValidationRuntimeConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        if not constraint.precondition or not constraint.precondition.evaluations:
            return True, "There in no precondition"
        valid_conditions = []
        for evaluation in constraint.precondition.evaluations:
            json_path = evaluation.json_path or "$"

            if not json_path.startswith("$"):
                json_path = f"${json_path}"
            json_input = root if evaluation.root_value_evaluation else value
            checker = self.profile_validator_factory.get_checker(evaluation.constraint)

            json_expression = self._json_path_expressions.get(json_path)
            if not json_expression:
                json_expression = jsonpath_ng.parse(json_path)
                self._json_path_expressions[json_path] = json_expression

            matches = [x.value for x in json_expression.find(json_input)]
            if len(matches) == 1:
                matches = matches[0]
            elif len(matches) == 0:
                matches = None
            skip = False
            if runtime_config and runtime_config.skip_decimal_validations:
                if isinstance(constraint, DecimalConstraint):
                    skip = True

            if not skip:
                res = checker.validate_constraint(
                    evaluation.constraint, matches, root=root
                )
                if res.is_valid:
                    valid_conditions.append(evaluation)
            # elif res.message:
            #     logger.info("%s", res.message)

        return self.evaluate_results(
            valid_items_count=len(valid_conditions),
            all_items_count=len(constraint.precondition.evaluations),
            default_evaluation=evaluation.default_evaluation,
            join_operator=evaluation.join_operator,
            min_valid=evaluation.min_valid,
            max_valid=evaluation.max_valid,
        )

    def evaluate_results(
        self,
        # condition: Constraint | Evaluation,
        valid_items_count: int,
        all_items_count: int,
        join_operator: Literal["and", "or"] = "and",
        min_valid: None | int = None,
        max_valid: None | int = None,
        default_evaluation: None | bool = None,
    ):
        if all_items_count == 0:
            success = default_evaluation if default_evaluation is not None else True
            return success, "No item found for evaluation"

        if join_operator == "and":
            message = "some conditions are not satisfied"
            if valid_items_count == all_items_count:
                return True, "all conditions are satisfied"
        else:
            message = "some conditions are satisfied"
            min_valid = min_valid if min_valid is not None else 1
            max_valid_constraints = (
                max_valid if max_valid is not None else all_items_count
            )
            min_valid_req = False
            max_valid_req = False
            messages = []
            if valid_items_count >= min_valid:
                min_valid_req = True
            else:
                messages.append("min valid conditions is not satisfied")
            if valid_items_count <= max_valid_constraints:
                max_valid_req = True
            else:
                messages.append("min valid conditions is not satisfied")
            if min_valid_req and max_valid_req:
                message = "all conditions are satisfied"
                return True, message
            message = ". ".join(messages)
        return False, message

    def validate_constraint(
        self,
        constraint: Constraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
        runtime_config: None | ValidationRuntimeConfiguration = None,
    ) -> ConstraintValidationResult:
        """Dispatcher to route validation to the specific constraint validator."""
        checker = self.profile_validator_factory.get_checker(constraint)

        if checker:
            success, message = checker.evaluate_precondition(
                constraint, value, root=root
            )

            sub_value = self.get_json_path_value(constraint, value)
            if success:
                is_valid, message = checker.validate(
                    constraint,
                    sub_value,
                    root=root,
                    config=config,
                    runtime_config=runtime_config,
                )
            else:
                is_valid = True
                message = f"Precondition does not meet: {message}"
            return ConstraintValidationResult(
                is_valid=is_valid,
                message=message,
                constraint_name=getattr(constraint, "name", "unknown"),
            )

        return ConstraintValidationResult(
            is_valid=False,
            message=f"Unknown constraint type: {type(constraint)}",
            constraint_name=getattr(constraint, "name", "unknown"),
        )

    def get_json_path_value(self, constraint: Constraint, value: Any):
        sub_input_value = value

        if constraint.json_path:
            sub_jsonpath = constraint.json_path
            if not sub_jsonpath.startswith("$"):
                if sub_jsonpath.startswith("[") or sub_jsonpath.startswith("."):
                    sub_jsonpath = f"${sub_jsonpath}"
                elif not sub_jsonpath.startswith("."):
                    sub_jsonpath = f"$.{sub_jsonpath}"
            sub_jsonpath_expr = self._json_path_expressions.get(sub_jsonpath)
            if not sub_jsonpath_expr:
                sub_jsonpath_expr = jsonpath_ng.parse(sub_jsonpath)
                self._json_path_expressions[sub_jsonpath] = sub_jsonpath_expr

            sub_input_value = [a.value for a in sub_jsonpath_expr.find(value)]
            if len(sub_input_value) == 1:
                sub_input_value = sub_input_value[0]
            elif len(sub_input_value) == 0:
                sub_input_value = None
        return sub_input_value


MZTABM_DEFAULT_VALIDATOR_ID = (
    "https://github.com/HUPO-PSI/mzTab-M/profile-validators/default"
)
REGISTERED_PROFILE_CHECKER_CLASSES: dict[
    str, dict[tuple[str, str], type[ConstraintChecker]]
] = {}


def constraint_checker(
    constraint_class: type[Constraint],
    constraint_name: Optional[str] = None,
    validator_id: Optional[str] = None,
    is_active: bool = True,
):
    global REGISTERED_PROFILE_CHECKER_CLASSES
    if not validator_id:
        validator_id = MZTABM_DEFAULT_VALIDATOR_ID
    if validator_id not in REGISTERED_PROFILE_CHECKER_CLASSES:
        REGISTERED_PROFILE_CHECKER_CLASSES[validator_id] = {}

    def decorator(checker_class: type[ConstraintChecker]):
        if not issubclass(checker_class, ConstraintChecker):
            raise ValueError("Must be a subclass of ConstraintChecker")
        if not issubclass(constraint_class, Constraint):
            raise ValueError("Must be a subclass of Constraint")

        if not is_active:
            logger.debug(
                "Constraint checker '%s' is not active. Skipping...",
                constraint_class.__name__,
            )
            return
        checkers = REGISTERED_PROFILE_CHECKER_CLASSES[validator_id]
        constraint_type = constraint_class.model_fields.get("type").default
        if constraint_type == "custom" and not constraint_name:
            ValueError("constraint_name is required for a custom constraint")
        key = (constraint_type, constraint_name or None)
        if key in checkers:
            raise ValueError(
                f"{constraint_type} {constraint_name} checker is already in registry"
            )
        checkers[key] = checker_class
        logger.info(
            "Registering constraint checker '%s' %s %s",
            constraint_class.__name__,
            constraint_name,
            constraint_class.__name__,
        )

        # checker = checker_class(
        #     constraint_type=constraint_class, profile_validator=profile_validator
        # )
        # checker.is_active = is_active

        # profile_validator.register_checker(
        #     constraint_type=constraint_class,
        #     constraint_name=constraint_name,
        #     checker=constraint_class,
        # )
        return checker_class

    return decorator


class CustomConstraintChecker(ConstraintChecker, abc.ABC):
    @abc.abstractmethod
    def validate(
        self,
        constraint: CustomConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
        runtime_config: None | ValidationRuntimeConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        ...
        # if not constraint.validator:
        #     return False, "CustomConstraint is missing validator_id."

        # checker = self.profile_validator_factory.get_checker(constraint)
        # if not checker:
        #     return (
        #         False,
        #         f"Custom checker '{constraint.validator}' not found in registry.",
        #     )

        # try:
        #     is_valid, message = checker.validate(
        #         constraint, value, root=root, config=config
        #     )
        # except Exception as e:
        #     return False, str(e)
        # return is_valid, message


# def custom_constraint_checker(name: str, is_active: bool = True):
#     def decorator(checker_class: type[CustomConstraintChecker]):
#         if not issubclass(checker_class, CustomConstraintChecker):
#             raise ValueError("Must be a subclass of CustomConstraintChecker")
#         return default_constraint_checker(name, CustomConstraint, is_active)(
#             checker_class
#         )

#     return decorator
