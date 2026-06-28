import datetime
import re
from decimal import Decimal
from typing import Any, Mapping, Optional, Tuple

import email_validator
import jsonpath_ng
from rfc3986 import urlparse
from rfc3986.validators import Validator as Rfc3986Validator

from mztab_m_io.model.base import MzTabBaseModel
from mztab_m_io.model.common import Parameter
from mztab_m_io.model.mztabm_validation import (
    convert_full_path,
    is_non_string_container,
)
from mztab_m_io.profile.base import JsonPath
from mztab_m_io.profile.constraints import (
    BaseParameter,
    BooleanConstraint,
    CollectionConstraint,
    ConstraintGroup,
    CVListConstraint,
    CVTermConstraint,
    CVTermEnumConstraint,
    CVTermValueConstraint,
    DateTimeConstraint,
    DecimalConstraint,
    EmailConstraint,
    IntegerConstraint,
    IntegerEnumConstraint,
    NonNegativeIntegerConstraint,
    NotNullConstraint,
    ParentCVTermConstraint,
    PositiveIntegerConstraint,
    RegexConstraint,
    StringConstraint,
    StringEnumConstraint,
    UriConstraint,
)
from mztab_m_io.profile.model import MzTabMProfileConfiguration
from mztab_m_io.validator.base import (
    ConstraintChecker,
    constraint_checker,
)


def extract_cv_info(value: Any) -> Parameter:
    """Extracts label, accession, name, and value from a Parameter or dict."""
    if isinstance(value, Parameter):
        return value
    elif isinstance(value, dict):
        return Parameter(
            cv_label=value.get("cv_label"),
            cv_accession=value.get("cv_accession"),
            name=value.get("name"),
            value=value.get("value"),
        )
    elif isinstance(value, str):
        cleaned = value.strip("[]")
        parts = cleaned.split(",", maxsplit=3)
        return Parameter(
            cv_label=parts[0].strip() if len(parts) > 0 else None,
            cv_accession=parts[1].strip() if len(parts) > 1 else None,
            name=parts[2].strip() if len(parts) > 2 else None,
            value=parts[3].strip() if len(parts) > 3 else None,
        )


@constraint_checker(NotNullConstraint)
class NotNullConstraintChecker(ConstraintChecker):
    """
    Regex constraint checker validates a string value
    against a regular expression pattern.
    """

    def validate(
        self,
        constraint: NotNullConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        messages = []
        if value is not None and constraint.null_values:
            str_val = str(value) if constraint.case_sensitive else str(value).lower()
            if str_val in constraint.null_values:
                messages.append("value is in null value list")
                value = None
        message = ""
        if value is not None:
            evaluation = True
            message = f"{value} is not null"
        message = ". ".join(messages)

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(RegexConstraint)
class RegexConstraintChecker(ConstraintChecker):
    """
    Regex constraint checker validates a string value
    against a regular expression pattern.
    """

    def validate(
        self,
        constraint: RegexConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        if value is not None and constraint.null_values:
            str_val = str(value) if constraint.case_sensitive else str(value).lower()
            if str_val in constraint.null_values:
                value = None
        message = ""
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is null"
        else:
            str_val = str(value) if constraint.case_sensitive else str(value).lower()
            if constraint.exceptional_values and (
                str_val in constraint.exceptional_values
                or value in constraint.exceptional_values
            ):
                evaluation = True
            else:
                if constraint.case_sensitive:
                    match = re.fullmatch(constraint.pattern, str_val)
                else:
                    match = re.fullmatch(constraint.pattern, str_val, re.IGNORECASE)
                if match:
                    message = (
                        f"value matches the pattern. input: '{str_val}' "
                        f"pattern: '{constraint.pattern}'"
                    )
                    evaluation = True
                else:
                    message = (
                        f"value does not match the pattern. input: '{str_val}' "
                        f"expected pattern: '{constraint.pattern}'"
                    )

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(StringConstraint)
class StringConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: StringConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        if value is not None and constraint.null_values:
            str_val = str(value)
            if str_val in constraint.null_values:
                value = None
        evaluation = False
        message = ""
        min_req = False
        max_req = False
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                min_req = True
                max_req = True
            elif not constraint.minimum:
                min_req = True
            message = "value is null"
        else:
            if not isinstance(value, str):
                message = f"Value type is {type(value)}"
            else:
                val = str(value)
                if constraint.exceptional_values and (
                    val in constraint.exceptional_values
                    or value in constraint.exceptional_values
                ):
                    min_req = True
                    max_req = True
                else:
                    messages = []
                    min_req = (
                        True
                        if constraint.minimum is None or len(val) >= constraint.minimum
                        else False
                    )
                    max_req = (
                        True
                        if constraint.maximum is None or len(val) <= constraint.maximum
                        else False
                    )
                    if not min_req:
                        messages.append("minimum length error")
                    if not max_req:
                        messages.append("maximum length error")
                    message = ". ".join(messages)
        evaluation = True if min_req and max_req else False
        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(CollectionConstraint)
class CollectionConstraintChecker(ConstraintChecker):

    def validate(
        self,
        constraint: CollectionConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        if value is not None and constraint.null_values:
            str_val = str(value)
            if str_val in constraint.null_values:
                value = None
        evaluation = False
        message = ""
        min_req = False
        max_req = False
        min_match_req = False
        max_match_req = False
        min_referenced_value_req = False
        max_referenced_value_req = False
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                min_req = True
                max_req = True
                min_match_req = True
                max_match_req = True
                min_referenced_value_req = True
                max_referenced_value_req = True
            elif not constraint.min_occurs:
                min_req = True
            message = "value is not defined"
        else:
            val = value
            if constraint.exceptional_values and (
                val in constraint.exceptional_values
                or value in constraint.exceptional_values
            ):
                min_req = True
                max_req = True
                min_match_req = True
                max_match_req = True
                min_referenced_value_req = True
                max_referenced_value_req = True
                message = "value is in exceptional list"
            else:
                messages = []
                min_req = (
                    True
                    if constraint.min_occurs is None
                    or len(val) >= constraint.min_occurs
                    else False
                )
                max_req = (
                    True
                    if constraint.max_occurs is None
                    or len(val) <= constraint.max_occurs
                    else False
                )
                if not min_req:
                    messages.append(
                        "minimum count error: "
                        f"current: {len(val)}, min: {constraint.min_occurs}"
                    )
                if not max_req:
                    messages.append(
                        "maximum count error: "
                        f"current: {len(val)}, max: {constraint.max_occurs}"
                    )
                if constraint.match_reference_values:
                    values: list[dict[str, Any]] = []
                    for json_path in constraint.item_value_jsonpath_list:
                        item_values = {}
                        json_expression = self._json_path_expressions.get(json_path)
                        if not json_expression:
                            json_expression = jsonpath_ng.parse(json_path)
                            self._json_path_expressions[json_path] = json_expression
                        # if json_path.startswith("@"):
                        matches = json_expression.find(value)
                        # else:
                        #     matches = json_expression.find(root)

                        for x in matches or []:
                            source = convert_full_path(x.full_path)
                            if (
                                constraint.null_values
                                and x.value in constraint.null_values
                            ):
                                item_values[source] = None
                            else:
                                item_values[source] = x.value
                        values.append(item_values)
                    keys = set().union(*(d.keys() for d in values))

                    zipped = {key: tuple(d.get(key) for d in values) for key in keys}
                    references = [
                        tuple(x) if is_non_string_container(x) else (x,)
                        for x in constraint.match_reference_values or []
                    ]
                    matched = []
                    matched_set = set()
                    for key, item in zipped.items():
                        if item in references:
                            matched.append(key)
                            matched_set.add(item)
                    matched_count = len(matched)
                    reference_value_matched_count = len(matched_set)

                    if constraint.min_match is not None:
                        if matched_count >= constraint.min_match:
                            min_match_req = True
                        else:
                            messages.append(
                                "Minimum items matched error. "
                                f"Matched count: {matched_count}, "
                                f"expected : {constraint.min_match}"
                            )
                    elif matched_count > 0:
                        min_match_req = True
                    if constraint.max_match is not None:
                        if matched_count <= constraint.max_match:
                            max_match_req = True
                        else:
                            messages.append(
                                "Maximum items matched error. "
                                f"Matched count: {matched_count}, "
                                f"expected : {constraint.max_match}"
                            )
                    else:
                        max_match_req = True

                    if constraint.min_referenced_value_match is not None:
                        if (
                            reference_value_matched_count
                            >= constraint.min_referenced_value_match
                        ):
                            min_referenced_value_req = True
                        else:
                            messages.append(
                                "Minimum matched item error. "
                                f"Matched count: {matched_count}, "
                                f"expected : {constraint.min_match}. "
                                "items are fetched with "
                                f"'{', '.join(constraint.item_value_jsonpath_list)}'"
                                " :, reference values: "
                                f"{', '.join(constraint.match_reference_values)}"
                            )
                    else:
                        min_referenced_value_req = True
                    if constraint.max_reference_value_match is not None:
                        if (
                            reference_value_matched_count
                            <= constraint.max_reference_value_match
                        ):
                            max_referenced_value_req = True
                        elif constraint.max_reference_value_match > matched_count:
                            messages.append(
                                "Maximum matched item error. "
                                f"Matched count: {matched_count}, "
                                f"expected : {constraint.max_match}. "
                                "items are fetched with "
                                f"'{', '.join(constraint.item_value_jsonpath_list)}'"
                                " :, reference values: "
                                f"{', '.join(constraint.match_reference_values)}"
                            )
                    else:
                        max_referenced_value_req = True
                else:
                    min_match_req = True
                    max_match_req = True
                    min_referenced_value_req = True
                    max_referenced_value_req = True
                message = ". ".join(messages)
        all_results = all(
            [
                min_req,
                max_req,
                min_match_req,
                max_match_req,
                min_referenced_value_req,
                max_referenced_value_req,
            ]
        )
        evaluation = True if all_results else False
        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(StringEnumConstraint)
class StringEnumConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: StringEnumConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        message = ""
        if value is not None and constraint.null_values:
            str_val = str(value)
            if str_val in constraint.null_values:
                value = None
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is null"
        else:
            val = str(value)
            if constraint.exceptional_values and (
                val in constraint.exceptional_values
                or value in constraint.exceptional_values
            ):
                evaluation = True
            else:
                if val in constraint.options:
                    evaluation = True
                    message = "value is in the enum list"
                else:
                    message = f"{val} value is not in the enum list"

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(IntegerEnumConstraint)
class IntegerEnumConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: IntegerEnumConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        message = ""
        if value is not None and constraint.null_values:
            str_val = str(value)
            if str_val in constraint.null_values:
                value = None
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is null"
        else:
            val = str(value)
            if constraint.exceptional_values and (
                val in constraint.exceptional_values
                or value in constraint.exceptional_values
            ):
                evaluation = True
            else:
                try:
                    int_val = int(val)
                except:  # noqa: E722
                    int_val = None
                if int_val is not None:
                    if int_val in constraint.options:
                        evaluation = True
                        message = "value is in the int enum list"
                    else:
                        message = "value is not in the int enum list"
                else:
                    message = f"value '{val}' is not numeric"

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(IntegerConstraint)
class IntegerConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: IntegerConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        message = ""
        if value is not None and constraint.null_values:
            str_val = str(value)
            if str_val in constraint.null_values:
                value = None
        min_req = False
        max_req = False
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                min_req = True
                max_req = True
            message = "value is null"
        else:
            val = str(value)
            if constraint.exceptional_values and (
                val in constraint.exceptional_values
                or value in constraint.exceptional_values
            ):
                min_req = True
                max_req = True
            else:
                try:
                    int_val = int(val)
                except:  # noqa: E722
                    int_val = None
                if int_val is not None:
                    min_req = (
                        True
                        if constraint.minimum is None or int_val >= constraint.minimum
                        else False
                    )
                    max_req = (
                        True
                        if constraint.maximum is None or int_val <= constraint.maximum
                        else False
                    )
                    messages = []
                    if constraint.minimum is not None and not min_req:
                        messages.append(
                            f"minimum value error. "
                            f"current: {int_val}, min: {constraint.minimum}"
                        )
                    if constraint.maximum is not None and not max_req:
                        messages.append(
                            "maximum value error. "
                            f"current: {int_val}, min: {constraint.maximum}"
                        )

                    message = ". ".join(messages)
                else:
                    message = f"value '{val}' is not numeric"
        evaluation = True if min_req and max_req else False
        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(NonNegativeIntegerConstraint)
class NonNegativeIntegerConstraintChecker(IntegerConstraintChecker): ...


@constraint_checker(PositiveIntegerConstraint)
class PositiveIntegerConstraintChecker(IntegerConstraintChecker): ...


@constraint_checker(BooleanConstraint)
class BooleanConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: BooleanConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        message = ""
        if value is not None and constraint.null_values:
            str_val = str(value)
            if str_val in constraint.null_values:
                value = None
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is null"
        else:
            val = str(value)
            if constraint.exceptional_values and (
                val in constraint.exceptional_values
                or value in constraint.exceptional_values
            ):
                evaluation = True
            else:
                try:
                    if val.lower() in constraint.exceptional_false_values or []:
                        boolean_value = False
                    elif val.lower() in constraint.exceptional_true_values or []:
                        boolean_value = True
                    else:
                        boolean_value = bool(val)
                except:  # noqa: E722
                    boolean_value = None

                if boolean_value is not None:
                    f"value '{val}' evaluated as {boolean_value}"
                else:
                    message = f"value '{val}' is not boolean"

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(DecimalConstraint)
class DecimalConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: DecimalConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        message = ""
        min_req = False
        max_req = False
        min_scale_req = False
        max_scale_req = False
        if value is not None and constraint.null_values:
            str_val = str(value).lower()
            if str_val in constraint.null_values:
                value = None
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                min_req = True
                max_req = True
                min_scale_req = True
                max_scale_req = True
            message = "value is null"
        else:
            val = str(value)
            if constraint.exceptional_values and (
                val in constraint.exceptional_values
                or value in constraint.exceptional_values
            ):
                min_req = True
                max_req = True
                min_scale_req = True
                max_scale_req = True
            else:
                decimal_val: None | Decimal = None
                try:
                    decimal_val = Decimal(val)
                except:  # noqa: E722
                    pass
                if decimal_val is not None:
                    if decimal_val.is_finite():
                        if (
                            not constraint.allow_scientific_notation
                            and "e" in val.lower()
                        ):
                            message = "scientific notation is not allowed"
                        else:
                            scale = -decimal_val.as_tuple().exponent
                            min_scale_req = (
                                True
                                if constraint.min_scale is None
                                or scale >= constraint.min_scale
                                else False
                            )
                            max_scale_req = (
                                True
                                if constraint.max_scale is None
                                or scale <= constraint.max_scale
                                else False
                            )
                            min_req = (
                                True
                                if constraint.minimum is None
                                or decimal_val >= constraint.minimum
                                else False
                            )
                            max_req = (
                                True
                                if constraint.maximum is None
                                or decimal_val <= constraint.maximum
                                else False
                            )
                            messages = []

                            if constraint.minimum is not None and not min_req:
                                messages.append("minimum value error")
                            if constraint.maximum is not None and not max_req:
                                messages.append("maximum value error")
                            if constraint.min_scale is not None and not min_scale_req:
                                messages.append("minimum scale error")
                            if constraint.max_scale is not None and not max_scale_req:
                                messages.append("max scale error")
                            message = ". ".join(messages)
                    else:
                        message = f"Value is {decimal_val}"
                        if constraint.allow_non_finite_values:
                            min_req = True
                            max_req = True
                            min_scale_req = True
                            max_scale_req = True

                else:
                    message = f"value '{val}' is not numeric"
        evaluation = (
            True if min_req and max_req and max_scale_req and min_scale_req else False
        )
        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(DateTimeConstraint)
class DateTimeConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: DateTimeConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        message = ""

        if value is not None and constraint.null_values:
            str_val = str(value).lower()
            if str_val in constraint.null_values:
                value = None

        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is null"
        else:
            val = str(value)
            if constraint.exceptional_values and (
                val in constraint.exceptional_values
                or value in constraint.exceptional_values
            ):
                evaluation = True
            else:
                try:
                    if constraint.format:
                        datetime.datetime.strptime(val, constraint.format)
                    else:
                        datetime.datetime.fromisoformat(val)
                    evaluation = True
                    message = "value is valid datetime"
                except:  # noqa: E722
                    message = "value is is not valid datetime"

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(EmailConstraint)
class EmailConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: EmailConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        message = ""
        if value is not None and constraint.null_values:
            str_val = str(value).lower()
            if str_val in constraint.null_values:
                value = None
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is null"
        else:
            val = str(value)
            if constraint.exceptional_values and (
                val in constraint.exceptional_values
                or value in constraint.exceptional_values
            ):
                evaluation = True
            else:
                try:
                    email_validator.validate_email(value)
                    evaluation = True
                    message = "value is valid email"
                except email_validator.EmailNotValidError:
                    message = "value is not valid email"

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(UriConstraint)
class UriConstraintChecker(ConstraintChecker):
    def __init__(self):
        super().__init__()
        self.validator = Rfc3986Validator()

    def validate(
        self,
        constraint: UriConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        message = ""
        if value is not None and constraint.null_values:
            str_val = str(value).lower()
            if str_val in constraint.null_values:
                value = None
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is null"
        else:
            val = str(value)
            if constraint.exceptional_values and (
                val in constraint.exceptional_values
                or value in constraint.exceptional_values
            ):
                evaluation = True
            else:
                try:
                    ref = urlparse(val)
                    self.validator.validate(ref)

                    if constraint.allowed_schemes:
                        if ref.scheme in constraint.allowed_schemes:
                            evaluation = True
                            message = "value is valid url with allowed scheme"
                    else:
                        evaluation = True
                        message = "value is valid url"
                except Exception:  # noqa: E722
                    message = "value is not valid url"

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(CVTermConstraint)
class CVTermConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: CVTermConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        param = None
        if value is not None and constraint.null_values:
            param = extract_cv_info(value)
            if str(param) in constraint.null_values:
                value = None
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is not defined"
        else:
            if not param:
                param = extract_cv_info(value)
            name_req = False
            value_req = False
            if not param.cv_label and not param.cv_accession and not param.name:
                message = f"Value '{value}' could not be parsed as a CV term."
            else:
                is_user_defined = (
                    not param.cv_label
                    and not param.cv_accession
                    and param.name
                    and len(param.name) > 0
                )
                if is_user_defined:
                    if constraint.allow_user_defined_terms:
                        name_req = True
                        message = "User-defined terms is allowed."
                    else:
                        message = "User-defined terms is not allowed."
                else:
                    if param.name:
                        if not param.cv_label or not param.cv_accession:
                            message = f"invalid cv term label or accession. {param}"
                        else:
                            name_req = True
                            message = "term is valid."
                    else:
                        message = f"invalid cv term name: {param}"

                messages = [message] if message else []

                if constraint.is_cv_term_value_required:
                    if param.value:
                        value_req = True
                        messages.append("Value of CV term is defined.")
                    else:
                        messages.append("Value slot for CV term is required.")
                else:
                    value_req = True
                message = ". ".join(messages)
            evaluation = value_req and name_req

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(CVListConstraint)
class CVListConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: CVListConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        if value is not None and constraint.null_values:
            param = extract_cv_info(value)
            if str(param) in constraint.null_values:
                value = None
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is null"
        else:
            param = extract_cv_info(value)
            name_req = False
            value_req = False
            if not param.cv_label and not param.cv_accession and not param.name:
                message = f"Value '{value}' could not be parsed as a CV term."
            else:
                message = ""
                is_user_defined = (
                    not param.cv_label and not param.cv_accession and param.name
                )
                if is_user_defined:
                    if constraint.allow_user_defined_terms:
                        name_req = True
                        message = "User-defined terms is allowed."
                    else:
                        message = "User-defined terms is not allowed."
                else:
                    if param.name:
                        if not param.cv_label or not param.cv_accession:
                            message = f" '{param}' invalid cv term label or accession."
                        else:
                            if constraint.exceptional_values:
                                base_param = BaseParameter.model_validate(
                                    param, from_attributes=True
                                )
                                if base_param in constraint.exceptional_values:
                                    name_req = True
                                    message = (
                                        f"'{param}' term is in exception cv term list."
                                    )
                            if not name_req:
                                if constraint.allowed_cv_list:
                                    if (
                                        param.cv_label.upper()
                                        in constraint.allowed_cv_list
                                    ):
                                        name_req = True
                                    else:
                                        message = (
                                            f"'{param}' not in the selected cv list: "
                                            f"{', '.join(constraint.allowed_cv_list)}"
                                        )
                                else:
                                    name_req = True
                                    message = "term in cv list."
                    else:
                        message = "invalid cv term name."

                messages = [message] if message else []

                if constraint.is_cv_term_value_required:
                    if param.value:
                        value_req = True
                        messages.append("Value of CV term is defined.")
                    else:
                        messages.append("Value slot for CV term is required.")
                else:
                    value_req = True
                message = ". ".join(messages)
            evaluation = value_req and name_req

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(CVTermEnumConstraint)
class CVTermEnumConstraintChecker(ConstraintChecker):
    def validate(
        self,
        constraint: CVTermEnumConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        if value is not None and constraint.null_values:
            param = extract_cv_info(value)
            if str(param) in constraint.null_values:
                value = None
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is null"
        else:
            param = extract_cv_info(value)
            name_req = False
            value_req = False
            if not param.cv_label and not param.cv_accession and not param.name:
                message = f"Value '{value}' could not be parsed as a CV term."
            else:
                is_user_defined = (
                    not param.cv_label and not param.cv_accession and param.name
                )
                if is_user_defined:
                    if constraint.allow_user_defined_terms:
                        name_req = True
                        message = "User-defined terms is allowed."
                    else:
                        message = "User-defined terms is not allowed."
                else:
                    if param.name:
                        if not param.cv_label or not param.cv_accession:
                            message = "invalid cv term label or accession."
                        else:
                            if constraint.exceptional_cv_list:
                                if param.cv_label in constraint.exceptional_cv_list:
                                    name_req = True
                                    message = (
                                        f"term '{param.cv_label}' is "
                                        "in exception cv list."
                                    )
                            if not name_req:
                                if constraint.allowed_cv_terms:
                                    input_val = BaseParameter.model_validate(
                                        param, from_attributes=True
                                    )

                                    if input_val in constraint.allowed_cv_terms:
                                        name_req = True
                                        message = f"'{input_val}' is in cv term list"
                                    else:
                                        message = (
                                            f"'{input_val}' is not in cv term list"
                                        )
                                else:
                                    name_req = True
                                    message = "term in cv term list"
                    else:
                        message = "invalid cv term name"

                messages = [message] if message else []

                if constraint.is_cv_term_value_required:
                    if param.value:
                        value_req = True
                        messages.append("Value of CV term is defined.")
                    else:
                        messages.append("Value slot for CV term is required.")
                else:
                    value_req = True
                message = ". ".join(messages)
            evaluation = value_req and name_req

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(ParentCVTermConstraint)
class ParentCVTermConstraintChecker(ConstraintChecker):
    # TODO: implement it later
    def validate(
        self,
        constraint: ParentCVTermConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        evaluation = False
        if value is not None and constraint.null_values:
            param = extract_cv_info(value)
            if str(param) in constraint.null_values:
                value = None
        if value is None:
            if constraint.exceptional_values and value in constraint.exceptional_values:
                evaluation = True
            message = "value is null"
        else:
            param = extract_cv_info(value)
            name_req = False
            value_req = False
            if not param.cv_label and not param.cv_accession and not param.name:
                message = f"Value '{value}' could not be parsed as a CV term."
            else:
                is_user_defined = (
                    not param.cv_label and not param.cv_accession and param.name
                )
                if is_user_defined:
                    if constraint.allow_user_defined_terms:
                        name_req = True
                        message = "User-defined terms is allowed."
                    else:
                        message = "User-defined terms is not allowed."
                else:
                    if param.name:
                        if not param.cv_label or not param.cv_accession:
                            message = "invalid cv term label or accession."
                        else:
                            if constraint.parent_cv_terms:
                                if param.cv_label in constraint.exceptional_cv_list:
                                    name_req = True
                                    message = "term is in exception cv list."
                            if not name_req:
                                if constraint.parent_cv_terms:
                                    input_val = BaseParameter.model_validate(
                                        param, from_attributes=True
                                    )
                                    if input_val in constraint.allowed_cv_terms:
                                        name_req = True
                                    else:
                                        message = "not in cv term list."
                                else:
                                    name_req = True
                                    message = "term in cv term list."
                    else:
                        message = "invalid cv term name."

                messages = [message] if message else []

                if constraint.is_cv_term_value_required:
                    if param.value:
                        value_req = True
                        messages.append("Value of CV term is defined.")
                    else:
                        messages.append("Value slot for CV term is required.")
                else:
                    value_req = True
                message = ". ".join(messages)
            evaluation = value_req and name_req

        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message


@constraint_checker(CVTermValueConstraint)
class CVTermValueConstraintChecker(ConstraintChecker):
    # TODO: implement it later
    def validate(
        self,
        constraint: CVTermValueConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        checker = CVTermConstraintChecker()
        is_valid, msg = checker.validate(constraint, value)
        if not is_valid:
            return is_valid, msg

        if value is None:
            return True, None

        param = extract_cv_info(value)

        if constraint.key_cv_term:
            key_matches = False
            if (
                constraint.key_cv_term.cv_accession
                and constraint.key_cv_term.cv_accession == param.cv_accession
            ):
                key_matches = True
            elif (
                not constraint.key_cv_term.cv_accession
                and constraint.key_cv_term.name == param.name
            ):
                key_matches = True

            if key_matches and constraint.value_constraint:
                checker = (
                    self.constraint_checker_manager.get_checker_by_constraint_type(
                        constraint.value_constraint
                    )
                )
                res = checker.validate_constraint(
                    constraint.value_constraint, param.value, root=root
                )
                return res.is_valid, res.message

        return True, None


@constraint_checker(ConstraintGroup)
class ConstraintGroupChecker(ConstraintChecker):
    def validate(
        self,
        constraint: ConstraintGroup,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        if not constraint.constraints:
            return True, None
        evaluation = False
        if value is not None and constraint.null_values:
            param = extract_cv_info(value)
            if str(param) in constraint.null_values:
                value = None
        is_and = constraint.join_operator == "and"
        messages = []
        valid_constraints = []
        for sub_constraint in constraint.constraints:
            res = self.validate_constraint(sub_constraint, value, root=root)
            if not res.is_valid and res.message:
                messages.append(res.message)

            if res.is_valid:
                valid_constraints.append(sub_constraint)

        valid_count = len(valid_constraints)
        min_valid = constraint.min_valid
        max_valid = constraint.max_valid
        if is_and:
            if valid_count == len(constraint.constraints):
                messages.append("All conditions are valid")
                evaluation = True
        else:
            min_valid = min_valid if min_valid is not None else 1
            if valid_count >= min_valid:
                evaluation = True
                messages.append(f"Min {min_valid} conditions are valid")
            else:
                messages.append(f"Min {min_valid} conditions are not valid")
            max_valid = (
                max_valid if max_valid is not None else len(constraint.constraints)
            )
            if valid_count <= max_valid:
                evaluation = True
                messages.append(f"Max {max_valid} conditions are valid")
            else:
                messages.append(f"Max {max_valid} conditions are not valid")
        message = ". ".join(messages)
        if constraint.negated:
            evaluation = not evaluation
        return evaluation, message
