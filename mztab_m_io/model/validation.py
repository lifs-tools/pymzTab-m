import enum
from typing import List, Literal, Optional

from mztab_m_io.model.base import MzTabBaseModel


class Category(str, enum.Enum):
    FORMAT = "format"
    LOGICAL = "logical"
    CROSS_CHECK = "cross_check"
    PROFILE = "profile"


class MessageType(str, enum.Enum):
    ERROR = "error"
    WARNING = "warn"
    INFO = "info"


class MzTabMessage(MzTabBaseModel):
    code: str = ""
    category: Category
    message_type: Optional[MessageType] = MessageType.INFO
    message: str
    line_number: Optional[int] = None
    source: Optional[str] = None


class ValidationContext(MzTabBaseModel):
    messages: List[MzTabMessage] = []
    source_format: Literal["tsv", "json", "yaml"] = "tsv"
    auto_complete_ids: bool = False
