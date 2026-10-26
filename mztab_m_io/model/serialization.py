import abc
import json
from typing import (
    Annotated,
    Any,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Set,
    Type,
    Union,
)

import yaml
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.functional_validators import ModelWrapValidatorHandler, model_validator
from pydantic_core.core_schema import ValidationInfo

from mztab_m_io.model.base import MzTabBaseModel
from mztab_m_io.model.field_utils import get_field_type_info
from mztab_m_io.model.validation import (
    Category,
    MessageType,
    MzTabMessage,
    ValidationContext,
)


class MetadataInfo(MzTabBaseModel):
    object_level_value_field: Optional[str] = None
    list_concatenation_str_dict: Dict[str, str] = {}
    referenced_field_names: Dict[str, str] = {}
    ignore_filed_names: Set[str] = set()
    non_indexed_list_values: Set[str] = set()
    field_type: Type[BaseModel]
    sub_field_types: Dict[str, Any] = {}
    subfield_lists: Set[str] = set()
    metadata_serializations: Dict[str, "MetadataSerialization"] = {}


ValueConstraint = Literal[
    "positive-integer",
    "non-negative-integer",
    "curie",
    "any-url",
    "datetime",
    "date",
    "email",
]

EnforcementLevel = Literal["recommended", "required"]


class ValidationPolicy(MzTabBaseModel):
    required: Optional[bool] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    pattern: Optional[str] = None
    value_constraint: Optional[ValueConstraint] = None
    enforcement_level: Optional[EnforcementLevel] = "required"


class ValidationProfile(MzTabBaseModel):
    validation_policy: Optional[Union[ValidationPolicy]] = ValidationPolicy()


class MetadataSerialization(ValidationProfile):
    ignore: bool = False
    object_level_value: bool = False
    list_concatenation_str: Optional[str] = None
    non_indexed_list_value: bool = False
    referenced_field_name: Optional[str] = None
    allow_multiple: bool = False
    mztab_example: Annotated[Optional[str], Field(alias="x-mztab-example")] = None


class TableSerialization(ValidationProfile):
    ignore: bool = False
    list_concatenation_str: Optional[str] = None
    multiple_columns: bool = False
    column_value_field: Optional[str] = None
    referenced_section: Optional[str] = None
    referenced_field_name: Optional[str] = None
    mztab_example: Annotated[Optional[str], Field(alias="x-mztab-example")] = None


class TableSectionInfo(MzTabBaseModel):
    list_concatenation_str_dict: Dict[str, str] = {}
    multi_column_fields: Dict[str, str] = {}
    column_value_fields: Dict[str, str] = {}
    data_types: Dict[str, Any] = {}
    list_fields: Dict[str, bool] = {}
    field_type: Type[BaseModel]
    table_serializations: Dict[str, "TableSerialization"] = {}


class SerializationContext(MzTabBaseModel):
    convert_to: Literal["tsv", "json", "yaml"] = "tsv"
    messages: List[MzTabMessage] = []
    success: bool = False


class MzTabSerializableModel(MzTabBaseModel):
    __metadata_info__: Union[None, MetadataInfo] = None
    __default_serialization__: Annotated[MetadataSerialization, Field(frozen=True)] = (
        MetadataSerialization()
    )
    __mztab_example__: Annotated[Optional[str], Field(alias="x-mztab-example")] = None

    def to_dict(self, context: SerializationContext, **kwargs) -> Dict[str, Any]:
        try:
            content = self.model_dump(**self._update_kwargs(**kwargs))
            context.success = True
            return content
        except Exception as e:
            context.success = False
            context.messages.append(
                MzTabMessage(
                    message_type=MessageType.ERROR,
                    category=Category.FORMAT,
                    source="input object",
                    message=str(e),
                )
            )
            return {}

    def to_json(self, context: SerializationContext, **kwargs) -> str:
        try:
            content = self.model_dump_json(**self._update_kwargs(**kwargs))
            context.success = True
            return content
        except Exception as e:
            context.success = False
            context.messages.append(
                MzTabMessage(
                    message_type=MessageType.ERROR,
                    category=Category.FORMAT,
                    source="output file",
                    message=str(e),
                )
            )
            return ""

    def to_yaml(self, context: SerializationContext, **kwargs) -> str:
        try:
            json_obj = json.loads(self.model_dump_json(**self._update_kwargs(**kwargs)))
            content = yaml.safe_dump(json_obj, sort_keys=False)
            context.success = True
            return content
        except Exception as e:
            context.success = False
            context.messages.append(
                MzTabMessage(
                    message_type=MessageType.ERROR,
                    category=Category.FORMAT,
                    source="output file",
                    message=str(e),
                )
            )
            return ""

    @classmethod
    def _update_kwargs(cls, **kwargs) -> dict:
        """
        Update kwargs for model_dump and model_dump_json
        with default arguments
        """
        if "by_alias" not in kwargs:
            kwargs["by_alias"] = True
        if "exclude_none" not in kwargs:
            kwargs["exclude_none"] = True
        return kwargs

    @classmethod
    def get_metadata_info(cls) -> MetadataInfo:
        if cls.__metadata_info__:
            return cls.__metadata_info__

        metadata_info = MetadataInfo(field_type=cls)

        for field, field_info in cls.model_fields.items():
            extra = field_info.json_schema_extra or {}
            is_list, field_type = get_field_type_info(cls, field)
            json_extra = MetadataSerialization.model_validate(extra, by_alias=True)
            field_name = field_info.validation_alias or field
            if is_list:
                metadata_info.subfield_lists.add(field_name)
            metadata_info.sub_field_types[field_name] = field_type

            metadata_info.metadata_serializations[field] = json_extra
            if json_extra.object_level_value:
                metadata_info.object_level_value_field = field_name
            if json_extra.list_concatenation_str:
                metadata_info.list_concatenation_str_dict[field_name] = (
                    json_extra.list_concatenation_str
                )
            if json_extra.referenced_field_name:
                metadata_info.referenced_field_names[field_name] = (
                    json_extra.referenced_field_name
                )
            if json_extra.ignore:
                metadata_info.ignore_filed_names.add(field_name)
            if json_extra.non_indexed_list_value:
                metadata_info.non_indexed_list_values.add(field_name)
        cls.__metadata_info__ = metadata_info
        return metadata_info

    @model_validator(mode="wrap")
    @classmethod
    def validate_model(
        cls,
        data: Any,
        handler: ModelWrapValidatorHandler["MzTabBaseModel"],
        info: ValidationInfo,
    ) -> "MzTabBaseModel":
        val = handler(data)
        if info and info.context and isinstance(info.context, ValidationContext):
            if isinstance(val, Mapping):
                for item, value in val.items():
                    item = cls.get_field_alias(item)
                    if info.context.messages is None:
                        info.context.messages = []
                    info.context.messages.append(
                        MzTabMessage(
                            category=Category.WARNING,
                            message_type=MessageType.WARNING,
                            message=f"Unknown field: {item}",
                        )
                    )
        return val

    __fields_alias_map__ = {}

    @classmethod
    def get_field_alias(cls, alias: str) -> str:
        if not cls.__fields_alias_map__:
            cls.__fields_alias_map__ = {}
            for field, field_info in cls.model_fields.items():
                name = field_info.validation_alias or field
                cls.__fields_alias_map__[name] = field

        return cls.__fields_alias_map__.get(alias)


class IdentifiableModel(MzTabSerializableModel):
    id: Annotated[
        Optional[int],
        Field(
            ge=1,
            json_schema_extra=MetadataSerialization(ignore=True).model_dump(),
        ),
    ] = None

    def get_id(self):
        return self.id


class CustomSerializer(abc.ABC):
    """
    An abstract base class to show that a model is a custom string serializer.
    """

    @abc.abstractmethod
    def to_tsv(self, context: SerializationContext) -> str:
        raise NotImplementedError


class CompactObjectModel(MzTabBaseModel, CustomSerializer):
    """
    A compact object model to serialize to
    a an object or a list of objects in a single line
    """

    pass
