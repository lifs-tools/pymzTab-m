import datetime
from enum import Enum
from typing import Annotated, Literal, Union

import email_validator
from pydantic import AnyUrl, Field

JsonPath = Annotated[str, Field(description="JSONPath expression")]


class EnforcementLevel(str, Enum):
    NOT_DEFINED = "not-defined"
    OPTIONAL = "optional"
    RECOMMENDED = "recommended"
    REQUIRED = "required"


ValueConstraint = Literal[
    "positive-integer",
    "non-negative-integer",
    "decimal",
    "curie",
    "any-url",
    "datetime",
    "date",
    "email",
]


def check_value_constraint(
    constraint: ValueConstraint, value: Union[str, int, float, bool]
) -> bool:
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
