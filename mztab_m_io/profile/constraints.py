import abc
from collections.abc import Sequence
from decimal import Decimal
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import (
    Field,
    field_validator,
)

from mztab_m_io.model.base import MzTabBaseModel
from mztab_m_io.model.common import ExtendedParameter
from mztab_m_io.profile.base import JsonPath


class ValidationRuntimeConfiguration(MzTabBaseModel):
    offline_mode: Annotated[
        None | bool,
        Field(description="Skip online validations and checks."),
    ] = None

    skipped_requirements: Annotated[
        None | list[str],
        Field(description="Skip the listed requirements."),
    ] = None

    max_messages_for_each_requirement: Annotated[
        None | int,
        Field(description="Maximum message for each requirement."),
    ] = 10

    skip_decimal_validations: Annotated[
        None | bool,
        Field(description="Skip decimal value constraints."),
    ] = None


class BaseParameter(MzTabBaseModel):
    """A lightweight reference to a controlled vocabulary (CV) term.

    Used within constraint definitions to identify specific CV terms
    by their label, accession, or human-readable name.
    """

    cv_label: Annotated[
        Optional[str],
        Field(
            description="Short identifier of the controlled vocabulary "
            "(e.g. 'MS' for PSI-MS, 'UO' for Unit Ontology)."
        ),
    ] = ""
    cv_accession: Annotated[
        Optional[str],
        Field(description="Accession of the term in CURIE format (e.g. 'MS:1000073')."),
    ] = ""
    name: Annotated[
        Optional[str],
        Field(
            description="Human-readable name of the parameter term "
            "(e.g. 'electrospray ionization')."
        ),
    ] = ""

    def __str__(self):
        return f"[{self.cv_label or ''}, {self.cv_accession or ''}, {self.name or ''}]"


class Precondition(MzTabBaseModel):
    evaluations: Annotated[
        list["Evaluation"], Field(description="Evaluation constraints", min_length=1)
    ]
    join_operator: Annotated[
        Literal["and", "or"],
        Field(description="Operator to join the constraints."),
    ] = "and"
    min_valid: Annotated[
        Optional[int],
        Field(
            description="Minimum number of evaluation that must be true for evaluation."
        ),
    ] = None
    max_valid: Annotated[
        Optional[int],
        Field(description="Maximum number of evaluation that can be true."),
    ] = None


class Constraint(abc.ABC, MzTabBaseModel):
    """Base class for all validation constraints.

    Every constraint has a ``name`` that acts as its type discriminator
    when serialized to JSON/YAML profiles.
    """

    validator: Annotated[
        Optional[str],
        Field(
            description="Label of validator. "
            "If it is not defined, default validator will be used"
        ),
    ] = None
    type: Annotated[
        str,
        Field(description="Unique discriminator identifying the constraint type."),
    ]
    name: Annotated[Optional[str], Field(description="Name of constraint.")] = None
    precondition: Annotated[None | Precondition, Field(description="")] = None
    json_path: Annotated[
        Optional[JsonPath],
        Field(
            description="Jsonpath used as input to constraint. "
            "It is relative jsonpath of `value`. If it is not defined, "
            "`value` will be used."
        ),
    ] = None

    default_precondition_evaluation: Annotated[
        Optional[bool],
        Field(
            description="Defines evaluation value "
            "if there is a precondition failure. "
            "if it is not defined, evaluation value will be considered True"
        ),
    ] = None
    negated: Annotated[
        Optional[bool],
        Field(
            description="Whether the constraint should be negated. If set to true, "
            "the constraint is inverted."
        ),
    ] = None
    null_values: Annotated[
        Optional[list[Optional[str]]],
        Field(description="List of values that should be considered null."),
    ] = None
    exceptional_values: Annotated[
        Optional[list[Union[None, str]]],
        Field(
            description="List of values that are exceptions to the constraint. "
            "If a value is found in this list, "
            "the constraint will not be applied to it and return True."
        ),
    ] = None


class CollectionConstraint(Constraint):
    """Checks minimum and maximum number of occurrences of items."""

    type: Annotated[
        str,
        Field(description="Unique discriminator identifying the constraint type."),
    ] = "items-count"

    min_occurs: Annotated[
        Optional[int], Field(description="Minimum number of items.")
    ] = None
    max_occurs: Annotated[
        Optional[int],
        Field(Field(description="Maximum number of items.")),
    ] = None

    item_value_jsonpath_list: Annotated[
        Optional[list[str]],
        Field(
            description="relative jsonpath values "
            "to select item values for matching reference values. "
            "If it is not defined, serialized version of collection item will be used."
        ),
    ] = None
    match_reference_values: Annotated[
        Optional[list[bool] | list[int] | list[str] | list[BaseParameter]],
        Field(description="reference value list to compare collection item values."),
    ] = None
    min_match: Annotated[
        Optional[int],
        Field(Field(description="Minimum number of match in the collection.")),
    ] = None

    max_match: Annotated[
        Optional[int],
        Field(Field(description="Maximum number of match in the collection.")),
    ] = None

    min_referenced_value_match: Annotated[
        Optional[int],
        Field(
            Field(description="Minimum number of referenced values will match an item.")
        ),
    ] = None

    max_reference_value_match: Annotated[
        Optional[int],
        Field(
            Field(description="Maximum number of referenced values will match an item.")
        ),
    ] = None


class NotNullConstraint(Constraint):
    """Base class for constraints that can be null."""

    type: Annotated[
        str,
        Field(description="Unique discriminator identifying the constraint type."),
    ] = "not-null"

    case_sensitive: Annotated[
        Optional[bool],
        Field(description="Whether the comparison should be case-sensitive."),
    ] = None
    exceptional_values: Annotated[
        Optional[list[Union[None, str]]],
        Field(
            frozen=True,
            description="All values will be considered to evaluate value.",
        ),
    ] = None


class RegexConstraint(Constraint):
    """Validates a string value against a regular expression pattern.

    Use for structured identifiers or format patterns that can be
    expressed as a single regex (e.g. ORCID, adduct ion notation).
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = "regex"
    pattern: Annotated[
        str,
        Field(
            min_length=2,
            description="Regular expression pattern the value must match. "
            "Anchored implicitly (full-match semantics).",
        ),
    ]
    case_sensitive: Annotated[
        Optional[bool],
        Field(
            description="Whether the pattern match is case-sensitive. Defaults to True."
        ),
    ] = True


class StringConstraint(Constraint):
    """Validates that a string value's length falls within a range.

    At least one of ``minimum`` or ``maximum`` should be set.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "string-length"
    )
    minimum: Annotated[
        Optional[int],
        Field(
            description="Minimum number of characters (inclusive). "
            "None means no lower bound.",
            ge=0,
        ),
    ] = None
    maximum: Annotated[
        Optional[int],
        Field(
            description="Maximum number of characters (inclusive). "
            "None means no upper bound.",
            ge=0,
        ),
    ] = None


class StringEnumConstraint(Constraint):
    """Validates that a string value is one of a fixed set of allowed options.

    Each option maps a string key to a display value, integer code,
    or an ``ExtendedParameter`` with full CV term metadata.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "string-enum"
    )
    options: Annotated[
        list[str] | dict[str, Union[int, str, ExtendedParameter]],
        Field(
            description="Mapping of allowed string values to their "
            "display labels, integer codes, or CV term definitions."
        ),
    ]


class IntegerEnumConstraint(Constraint):
    """Validates that an integer value is one of a fixed set of allowed options.

    Each option maps an integer key to a display value, integer code,
    or an ``ExtendedParameter`` with full CV term metadata.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "integer-enum"
    )
    options: Annotated[
        dict[int, Union[int, str, ExtendedParameter]],
        Field(
            description="Mapping of allowed integer values to their "
            "display labels, integer codes, or CV term definitions."
        ),
    ]


class IntegerConstraint(Constraint):
    """Validates that a value is a valid integer within an optional range.

    Use ``PositiveIntegerConstraint`` or ``NonNegativeIntegerConstraint``
    for common presets.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "integer"
    )
    minimum: Annotated[
        Optional[int],
        Field(
            description="Minimum allowed value (inclusive). None means no lower bound."
        ),
    ] = None
    maximum: Annotated[
        Optional[int],
        Field(
            description="Maximum allowed value (inclusive). None means no upper bound."
        ),
    ] = None


class PositiveIntegerConstraint(IntegerConstraint):
    """Validates that a value is a positive integer (≥ 1).

    Convenience subclass of ``IntegerConstraint`` with ``minimum=1``.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "positive-integer"
    )
    minimum: Annotated[
        Optional[int],
        Field(description="Minimum allowed value (inclusive). Defaults to 1."),
    ] = 1


class NonNegativeIntegerConstraint(IntegerConstraint):
    """Validates that a value is a non-negative integer (≥ 0).

    Convenience subclass of ``IntegerConstraint`` with ``minimum=0``.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "non-negative-integer"
    )
    minimum: Annotated[
        Optional[int],
        Field(description="Minimum allowed value (inclusive). Defaults to 0."),
    ] = 0


class BooleanConstraint(Constraint):
    """Validates that a value is boolean."""

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "boolean"
    )

    exceptional_false_values: Annotated[
        Optional[list[Optional[str]]],
        Field(
            description="Exceptional values counted as false. e.g., '0', 'no'. "
            " List all as lower case"
        ),
    ] = None
    exceptional_true_values: Annotated[
        Optional[list[Optional[str]]],
        Field(
            description="Exceptional true value list. e.g., '1', 'yeah'. "
            " List all as lower case"
        ),
    ] = None


class DecimalConstraint(Constraint):
    """Validates that a value is a valid floating-point number.

    Supports optional range bounds, scientific notation control,
    and decimal precision limits.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "decimal"
    )
    minimum: Annotated[
        Optional[Decimal],
        Field(
            description="Minimum allowed value (inclusive). None means no lower bound."
        ),
    ] = None
    maximum: Annotated[
        Optional[Decimal],
        Field(
            description="Maximum allowed value (inclusive). None means no upper bound."
        ),
    ] = None
    allow_scientific_notation: Annotated[
        Optional[bool],
        Field(
            description="Whether scientific notation (e.g. '1.23e4') is "
            "accepted. None means no restriction."
        ),
    ] = None
    min_scale: Annotated[
        Optional[int],
        Field(
            description="Minimum number of digits after the decimal point. "
            "None means no minimum scale requirement.",
            ge=0,
        ),
    ] = None
    max_scale: Annotated[
        Optional[int],
        Field(
            description="Maximum number of digits after the decimal point. "
            "None means no maximum scale limit.",
            ge=0,
        ),
    ] = None
    allow_non_finite_values: Annotated[
        Optional[bool],
        Field(description="Allow NaN, and -/+ Infinity values"),
    ] = None


class DateTimeConstraint(Constraint):
    """Validates that a string value represents a valid date, time,
    or datetime.

    When ``format`` is provided, the value must match that specific
    pattern (e.g. ISO-8601). When omitted, ISO-8601 is accepted.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = "time"
    format: Annotated[
        Optional[str],
        Field(
            description="Expected time/date format string "
            "(e.g. '%Y-%m-%d', '%Y-%m-%dT%H:%M:%SZ', '%H:%M:%S'). "
            "None means Date and time in UTC format is accepted."
        ),
    ] = None


class EmailConstraint(Constraint):
    """Validates that a string value is a well-formed email address."""

    type: Annotated[str, Field(description="Constraint type discriminator.")] = "email"


class UriConstraint(Constraint):
    """Validates that a string value is a well-formed URI.

    Optionally restricts accepted URI schemes (e.g. only ``https``,
    ``ftp``).
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = "uri"
    allowed_schemes: Annotated[
        Optional[list[str]],
        Field(
            description="List of accepted URI schemes "
            "(e.g. ['http', 'https', 'ftp']). "
            "None means any scheme is accepted."
        ),
    ] = None


class BaseCvTermConstraint(Constraint):
    """Base class for all validation constraints.

    Every constraint has a ``name`` that acts as its type discriminator
    when serialized to JSON/YAML profiles.
    """

    type: Annotated[
        str,
        Field(description="Unique discriminator identifying the constraint type."),
    ]
    exceptional_values: Annotated[
        Optional[list[Union[None, BaseParameter]]],
        Field(description="Allowed exceptional CV terms."),
    ] = None

    null_values: Annotated[
        Optional[list[Optional[str]]],
        Field(description="List of values that should be considered null."),
    ] = None


class CVTermConstraint(BaseCvTermConstraint):
    """Base constraint for values that must be controlled vocabulary terms.

    Subclasses refine which CV terms are acceptable (by list, by parent
    term, or by CV namespace). This class captures the common options
    shared across all CV term constraints.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "cv-term"
    )
    allow_user_defined_terms: Annotated[
        Optional[bool],
        Field(
            description="Whether user-defined terms (empty cv_label and cv_accession) "
            "are accepted alongside CV terms."
        ),
    ] = None
    is_cv_term_value_required: Annotated[
        Optional[bool],
        Field(
            description="Whether the CV term's value slot must be populated. "
            "When True, value MUST not be empty or null."
        ),
    ] = None


class CVListConstraint(CVTermConstraint):
    """Restricts CV terms to those from specific controlled vocabularies.

    The ``cv_list`` field specifies which CV namespace labels are
    allowed (e.g. ``['MS', 'UO']``).
    """

    type: Annotated[
        str,
        Field(description="Constraint type discriminator."),
    ] = "allowed-cv-list"
    allowed_cv_list: Annotated[
        Optional[list[str]],
        Field(
            min=1,
            description="List of allowed CV namespace labels "
            "(e.g. ['MS', 'UO', 'PRIDE']). Use only uppercase letters."
            "None means any CV namespace is accepted.",
        ),
    ] = None
    allow_user_defined_terms: Annotated[
        Optional[bool],
        Field(
            description="Whether user-defined terms (empty cv_label and cv_accession) "
            "are accepted alongside CV terms."
        ),
    ] = False

    @field_validator("allowed_cv_list", check_fields=False)
    @classmethod
    def cv_list_validation(cls, value):
        if not value:
            return None
        if isinstance(value, str):
            return [value.upper()]
        if isinstance(value, Sequence):
            return [str(x).upper() for x in value]
        return value


class CVTermEnumConstraint(CVTermConstraint):
    """Restricts the value to a specific set of CV terms.

    Unlike ``CVListConstraint`` which filters by CV namespace, this
    constraint enumerates the exact terms that are acceptable.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "cv-term-enum"
    )
    allowed_cv_terms: Annotated[
        list[BaseParameter],
        Field(
            min=1,
            description="Explicit list of allowed CV terms. "
            "Each entry identifies a term by label, accession, or name.",
        ),
    ]

    exceptional_cv_list: Annotated[
        Optional[list[str]],
        Field(description="Allowed exceptional CV terms."),
    ] = None


class ParentCVTermConstraint(CVTermConstraint):
    """Restricts the value to CV terms that are descendants of
    specified parent terms in the ontology hierarchy.

    Supports exclusion of specific terms or name patterns to
    filter out unwanted branches of the ontology tree.
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "parent-cv-term"
    )
    parent_cv_terms: Annotated[
        Optional[list[BaseParameter]],
        Field(
            min=1,
            description="List of parent CV terms. Valid values must be "
            "descendants of at least one of these terms.",
        ),
    ] = None
    excluded_cv_terms: Annotated[
        Optional[list[BaseParameter]],
        Field(
            description="CV terms to exclude even if they are descendants "
            "of a parent term."
        ),
    ] = None


class CVTermValueConstraint(Constraint):
    """Validates the value slot of a specific CV term.

    When a field contains a CV term matching ``key_cv_term``, its
    value is validated against the nested ``value_constraint``.
    This enables context-dependent validation (e.g. a numeric range
    that only applies when a specific CV term is used).
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "cv-term-value"
    )
    key_cv_term: Annotated[
        Optional[BaseParameter],
        Field(
            description="The CV term whose value slot should be validated. "
            "When the field contains this term, the value_constraint is applied."
        ),
    ] = None
    value_constraint: Annotated[
        Optional["DefaultConstraintType"],
        Field(
            description="Constraint applied to the value slot of the "
            "matched CV term. Determines the expected type and format."
        ),
    ] = None


class OpaPolicyConstraint(Constraint):
    """Evaluates policy and returns messages.
    If there is no message, it will return empty list
    """

    type: Annotated[str, Field(description="Constraint type discriminator.")] = (
        "opa-policy"
    )
    opa_policy_file: Annotated[
        Optional[str],
        Field(
            description="OPA policy file key defined in profile configuration. "
            "If it is not defined, default policy file will be used."
        ),
    ] = None
    entrypoint: Annotated[str, Field(description="Entrypoint for evaluation")]


class CustomConstraint(Constraint):
    type: Annotated[str, Field(description="Constraint type discriminator.")] = "custom"

    name: Annotated[str, Field(description="Name of custom constraint.")]

    default_arguments: Annotated[
        Optional[dict[str, Any]],
        Field(description="The default arguments for the constraints."),
    ] = None
    value_jsonpath_arguments: Annotated[
        Optional[dict[str, str]],
        Field(
            description="The jsonpath arguments for the constraints. "
            "value is jsonpath string to fetch data from value or root object"
        ),
    ] = None
    root_jsonpath_arguments: Annotated[
        Optional[dict[str, str]],
        Field(
            description="The jsonpath arguments for the constraints. "
            "value is jsonpath string to fetch data from value or root object"
        ),
    ] = None


DefaultConstraintType = Annotated[
    Union[
        NotNullConstraint,
        IntegerConstraint,
        PositiveIntegerConstraint,
        NonNegativeIntegerConstraint,
        BooleanConstraint,
        DecimalConstraint,
        DateTimeConstraint,
        EmailConstraint,
        CollectionConstraint,
        UriConstraint,
        RegexConstraint,
        StringConstraint,
        StringEnumConstraint,
        IntegerEnumConstraint,
        CVTermConstraint,
        ParentCVTermConstraint,
        CVListConstraint,
        CVTermEnumConstraint,
        CustomConstraint,
        OpaPolicyConstraint,
        "ConstraintGroup",
    ],
    Field(description="A constraint type for a field."),
]


class Evaluation(MzTabBaseModel):
    root_value_evaluation: Annotated[
        Optional[bool], Field(description="Whether value is root or not.")
    ] = None
    json_path: Annotated[
        Optional[JsonPath],
        Field(
            description="Json path to find value for constraint evaluation. "
            "root or value will be used if it is not defined "
            "based on root_value_evaluation field"
        ),
    ] = None
    constraint: Annotated[
        DefaultConstraintType,
        Field(description="Constraint for evaluation"),
    ]
    default_evaluation: Annotated[
        Optional[bool],
        Field(
            description="Defines evaluation value "
            "if there is no result with jsonpath query. "
            "if it is not defined, evaluation value will be considered True"
        ),
    ] = None
    join_operator: Annotated[
        Literal["and", "or"],
        Field(description="Operator to join the constraints."),
    ] = "and"
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


class ConstraintGroup(Constraint):
    type: Annotated[str, Field(description="Constraint type discriminator.")] = "group"
    constraints: Annotated[
        list[DefaultConstraintType],
        Field(min=1, description="List of constraints."),
    ]
    join_operator: Annotated[
        Literal["and", "or"],
        Field(description="Operator to join the constraints."),
    ] = "and"
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


DEFAULT_CONSTRAINTS: list[type[Constraint]] = [
    NotNullConstraint,
    IntegerConstraint,
    PositiveIntegerConstraint,
    NonNegativeIntegerConstraint,
    BooleanConstraint,
    DecimalConstraint,
    DateTimeConstraint,
    EmailConstraint,
    CollectionConstraint,
    UriConstraint,
    RegexConstraint,
    StringConstraint,
    StringEnumConstraint,
    IntegerEnumConstraint,
    CVTermConstraint,
    ParentCVTermConstraint,
    CVListConstraint,
    CVTermEnumConstraint,
    CustomConstraint,
    OpaPolicyConstraint,
    ConstraintGroup,
]
DEFAULT_CONSTRAINTS_MAP: dict[str, Constraint] = {
    x.model_fields.get("type").default: x for x in DEFAULT_CONSTRAINTS
}
