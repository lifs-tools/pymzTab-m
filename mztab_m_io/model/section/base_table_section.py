from typing import Annotated, Any, List, Optional, OrderedDict, Union

from pydantic import (
    Field,
)

from mztab_m_io.model.base import MzTabBaseModel
from mztab_m_io.model.common import Comment
from mztab_m_io.model.field_utils import get_field_type_info, sanitize_str
from mztab_m_io.model.serialization import (
    CustomSerializer,
    SerializationContext,
    TableSectionInfo,
    TableSerialization,
)


class BaseTableSection(MzTabBaseModel, CustomSerializer):
    """
    Base class contains common fields for all table sections.
    """

    # It is used to store table info for each section
    __table_section_info_dict__: Union[None, dict[str, TableSectionInfo]] = None
    __mztab_example__: Annotated[Optional[str], Field(alias="x-mztab-example")] = None

    prefix: Annotated[
        Optional[str],
        Field(
            description="The table row prefix. SMF, SME or SML MUST be used for rows "
            "of the table.",
            json_schema_extra=TableSerialization(ignore=True).model_dump(),
        ),
    ] = None

    header_prefix: Annotated[
        Optional[str],
        Field(
            description="The table header prefix. SFH, SEH or SMH MUST be used for "
            "the table header line (the column labels).",
            json_schema_extra=TableSerialization(ignore=True).model_dump(),
        ),
    ] = None

    comment: Annotated[
        Optional[List[Comment]],
        Field(
            description="",
            json_schema_extra=TableSerialization(
                ignore=True,
            ).model_dump(),
        ),
    ] = []

    def to_tsv(self, context: SerializationContext) -> str:
        row: list[str] = []
        for field, field_info in self.__class__.model_fields.items():
            field_name = field_info.validation_alias or field

            json_extra = self.get_table_section_info().table_serializations.get(
                field_name
            )
            if not json_extra or json_extra.ignore:
                continue
            if json_extra.multiple_columns and not json_extra.column_value_field:
                vals = self._serialize_value(getattr(self, field), context)
                if isinstance(vals, list):
                    row.extend(vals)
                else:
                    row.append(vals)

            elif json_extra.column_value_field:
                custom = OrderedDict()
                item = self
                if getattr(item, field):
                    for cust_item in getattr(item, field):
                        header = cust_item.get_header()
                        custom[header] = getattr(
                            cust_item, json_extra.column_value_field
                        )
                vals = list(custom.values())
                if vals:
                    row.extend(self._serialize_value(vals, context))
            else:
                val = getattr(self, field)
                if json_extra.list_concatenation_str:
                    if isinstance(val, list):
                        val = json_extra.list_concatenation_str.join(
                            self._serialize_value(val, context)
                        )
                        row.append(val)
                    else:
                        row.append(self._serialize_value(val, context))
                else:
                    if isinstance(val, list):
                        row.extend(self._serialize_value(val, context))
                    else:
                        row.append(self._serialize_value(val, context))
        row_data = [self.prefix]
        row_data.extend(row)
        data = "\t".join([sanitize_str(str(x)) for x in row_data])
        if self.comment:
            data += "\n" + "\n".join(
                [comment.to_tsv(context) for comment in self.comment]
            )
        return data

    @classmethod
    def get_table_section_info(cls):
        """
        Returns the table section info for the given class.
        """
        prefix = cls.model_fields.get("prefix").default
        if not cls.__table_section_info_dict__:
            cls.__table_section_info_dict__ = {}
        table_section_info = cls.__table_section_info_dict__.get(prefix)
        if table_section_info:
            return table_section_info
        table_section_info = TableSectionInfo(field_type=cls)
        for field, field_info in cls.model_fields.items():
            extra = field_info.json_schema_extra or {}
            field_name = field_info.validation_alias or field
            json_extra = TableSerialization.model_validate(extra, by_alias=True)
            table_section_info.field_type = cls
            table_section_info.table_serializations[field_name] = json_extra

            is_list, item_type = get_field_type_info(cls, field)
            if is_list:
                table_section_info.list_fields[field_name] = True
            table_section_info.data_types[field_name] = item_type
            if json_extra.list_concatenation_str:
                table_section_info.list_concatenation_str_dict[field_name] = (
                    json_extra.list_concatenation_str
                )
            if json_extra.multiple_columns:
                table_section_info.multi_column_fields[field_name] = (
                    json_extra.multiple_columns
                )
            if json_extra.column_value_field:
                table_section_info.column_value_fields[field_name] = (
                    json_extra.column_value_field
                )
        cls.__table_section_info_dict__[prefix] = table_section_info
        return table_section_info

    @classmethod
    def get_table_header(cls, data: List["BaseTableSection"]):
        """
        Returns the table header for the given table rows.
        """
        columns = OrderedDict()
        for field, field_info in cls.model_fields.items():
            field_name = field_info.validation_alias or field

            json_extra = cls.get_table_section_info().table_serializations.get(
                field_name
            )
            if not json_extra or json_extra.ignore:
                continue
            if json_extra.multiple_columns and not json_extra.column_value_field:
                if data and data[0]:
                    example = data[0]
                    if hasattr(example, field):
                        val = getattr(example, field)
                        if isinstance(val, list):
                            for idx, _ in enumerate(val, start=1):
                                header = f"{field_name}[{idx}]"
                                columns[header] = field_name
                else:
                    header = f"{field_name}[1]"
                    columns[header] = field_name
            elif json_extra.column_value_field:
                custom = OrderedDict()
                if data and data[0]:
                    item = data[0]
                    if getattr(item, field_name):
                        for cust_item in getattr(item, field_name):
                            custom_header = cust_item.get_header()
                            custom[custom_header] = field_name
                for item, val in custom.items():
                    columns[item] = val
            else:
                columns[field_name] = field_name
        header_prefix = cls.model_fields["header_prefix"].get_default()
        headers = [header_prefix]
        headers.extend(columns)
        return "\t".join(headers)

    @classmethod
    def _serialize_value(cls, val: Any, context: SerializationContext):
        if val is None:
            return "null"
        val_str = str(val).strip()
        if not val_str or val_str.lower() == "null":
            return "null"
        if isinstance(val, list) and not val:
            return ["null"]
        if val_str.lower() == "nan":
            return "NaN"
        if isinstance(val, float) and val != val:  # isnan check
            return "NaN"
        if isinstance(val, CustomSerializer):
            return val.to_tsv(context)
        if isinstance(val, float):
            if val.is_integer():
                return f"{int(val)}"
            return f"{val:1.11E}"
        if isinstance(val, list):
            return [cls._serialize_value(x, context) for x in val]
        # TODO: handle other types
        return str(val)
