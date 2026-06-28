import logging
import re
from typing import Any, Optional, Tuple

import httpx2
from cachetools import TTLCache, cached

from mztab_m_io.profile.constraints import CustomConstraint
from mztab_m_io.profile.model import MzTabMProfileConfiguration
from mztab_m_io.validator.base import (
    CustomConstraintChecker,
    constraint_checker,
)

logger = logging.getLogger(__name__)


@constraint_checker(CustomConstraint, constraint_name="orcid", is_active=True)
class OrcidValidator(CustomConstraintChecker):
    """
    OrcidValidator checks if a given string value strictly conforms to the ORCID format.

    The expected ORCID format is XXXX-XXXX-XXXX-XXXX, where X is a digit from 0-9,
    and the final character can be a digit or the letter 'X'.
    """

    pattern = r"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[X0-9]$"

    def validate(
        self,
        constraint: CustomConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        """
        Validates the provided value against the ORCID regular expression pattern.

        Args:
            constraint (CustomConstraint): The custom constraint definition.
            value (Any): The value to be validated, expected to be a string.
            **kwargs: Additional keyword arguments.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating if the value is valid,
            along with an optional error message if it is not.
        """
        if not isinstance(value, str):
            return False, "Value must be a string"
        if not re.match(self.pattern, value):
            return (
                False,
                f"Value '{value}' is not in ORCID format: XXXX-XXXX-XXXX-XXXX",
            )
        return True, None


@constraint_checker(CustomConstraint, constraint_name="accessible-url")
class AccessibleUrlChecker(CustomConstraintChecker):
    """
    AccessibleUrlChecker checks if a given string value is an accessible URL.
    """

    @cached(cache=TTLCache(maxsize=2048, ttl=600))
    def check_http_url(self, url: str) -> Tuple[bool, Optional[str]]:
        try:
            result = httpx2.get(url, timeout=10, follow_redirects=True)
        except Exception as e:
            return False, f"URL '{url}' is not accessible: {e}"
        if result.status_code not in (200, 201):
            return False, f"URL '{url}' is not accessible: {result.status_code}"
        return True, None

    def validate(
        self,
        constraint: CustomConstraint,
        value: Any,
        root: None | dict[str, Any] = None,
        config: None | MzTabMProfileConfiguration = None,
    ) -> Tuple[bool, Optional[str]]:
        if not isinstance(value, str):
            return False, "Value must be a string"
        return self.check_http_url(value)
