from typing_extensions import Annotated, Any, List, Optional, OrderedDict, Union, Dict

from pydantic import (
    Field,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    model_serializer,
)

from mztab_m_io.model import CustomSerializer, MzTabBaseModel
from mztab_m_io.model.field_utils import get_field_type_info
from mztab_m_io.model.serialization import (
    TableInfo,
    TableSerialization,
    ValidationPolicy,
)


class BaseTableSection(MzTabBaseModel, CustomSerializer):
    prefix: Annotated[
        Optional[str],
        Field(
            description="The table row prefix. SMF, SME or SML MUST be used for rows "
            "of the table.",
            json_schema_extra=TableSerialization(
                ignore=True,
                validation_policy=ValidationPolicy(
                    required=True, pattern=r"SMF|SME|SML"
                ),
            ).model_dump(),
        ),
    ] = None
    header_prefix: Annotated[
        Optional[str],
        Field(
            description="The table header prefix. SFH, SEH or SMH MUST be used for "
            "the table header line (the column labels).",
            json_schema_extra=TableSerialization(
                ignore=True,
                validation_policy=ValidationPolicy(
                    required=True, pattern=r"SFH|SEH|SMH"
                ),
            ).model_dump(),
        ),
    ] = None

    @classmethod
    def serialize_value(cls, val: Any):
        if val is None or not str(val) or str(val).lower() == "null":
            return "null"
        if isinstance(val, list) and not val:
            return ["null"]
        if str(val).lower() == "nan" or val == float("nan"):
            return "NaN"
        if isinstance(val, MzTabBaseModel):
            return val.model_dump(by_alias=True)
        if isinstance(val, float):
            if val.is_integer():
                return f"{int(val)}"
            return f"{val:1.11E}"
        if isinstance(val, list):
            return [cls.serialize_value(x) for x in val]
        return str(val)

    @model_serializer(mode="wrap")
    def serialize_model(
        self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Union[str, Dict[str, Any]]:
        default_success, result = self.serialize_to_json(handler, info)
        if default_success:
            return result
        row = []
        for field, field_info in self.__class__.model_fields.items():
            extra = field_info.json_schema_extra or {}
            field_name = field_info.validation_alias or field

            json_extra = TableSerialization.model_validate(extra, by_alias=True)
            if json_extra.ignore:
                continue
            if json_extra.multiple_columns and not json_extra.column_name_field:
                vals = self.serialize_value(getattr(self, field))
                if isinstance(vals, list):
                    row.extend(vals)
                else:
                    row.append(vals)

            elif json_extra.column_name_field:
                custom = OrderedDict()
                item = self
                if getattr(item, field):
                    for cust_item in getattr(item, field):
                        if hasattr(cust_item, json_extra.column_name_field):
                            col = getattr(cust_item, json_extra.column_name_field)
                            custom_header = f"{field_name}_{col}"
                            custom[custom_header] = getattr(
                                cust_item, json_extra.column_value_field
                            )
                vals = list(custom.values())
                if vals:
                    row.extend(self.serialize_value(vals))
            else:
                val = getattr(self, field)
                if json_extra.list_concatenation_str:
                    if isinstance(val, list):
                        val = json_extra.list_concatenation_str.join(
                            self.serialize_value(val)
                        )
                        row.append(val)
                    else:
                        val = self.serialize_value(val)
                        row.append(val)
                else:
                    if isinstance(val, list):
                        row.extend(self.serialize_value(val))
                    else:
                        row.append(self.serialize_value(val))
        row_data = [self.prefix]
        row_data.extend([x for x in row])
        return "\t".join(row_data)

    @classmethod
    def get_table_info(cls):
        table_info = TableInfo()
        for field, field_info in cls.model_fields.items():
            extra = field_info.json_schema_extra or {}
            field_name = field_info.validation_alias or field
            json_extra = TableSerialization.model_validate(extra, by_alias=True)
            if json_extra.ignore:
                continue
            is_list, item_type = get_field_type_info(cls, field)
            if is_list:
                table_info.list_fields[field_name] = True
            table_info.data_types[field_name] = item_type
            if json_extra.list_concatenation_str:
                table_info.list_concatenation_str_dict[field_name] = (
                    json_extra.list_concatenation_str
                )
            if json_extra.multiple_columns:
                table_info.multi_column_fields[field_name] = json_extra.multiple_columns
            if json_extra.column_name_field:
                table_info.column_name_fields[field_name] = json_extra.column_name_field
            if json_extra.column_value_field:
                table_info.column_value_fields[field_name] = (
                    json_extra.column_value_field
                )

        return table_info

    @classmethod
    def get_table_header(cls, data: List["BaseTableSection"]):
        columns = OrderedDict()
        for field, field_info in cls.model_fields.items():
            extra = field_info.json_schema_extra or {}
            field_name = field_info.validation_alias or field

            json_extra = TableSerialization.model_validate(extra, by_alias=True)
            if json_extra.ignore:
                continue
            if json_extra.multiple_columns and not json_extra.column_name_field:
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
            elif json_extra.column_name_field:
                custom = OrderedDict()
                if data and data[0]:
                    item = data[0]
                    if getattr(item, field_name):
                        for cust_item in getattr(item, field_name):
                            if hasattr(cust_item, json_extra.column_name_field):
                                col = getattr(cust_item, json_extra.column_name_field)
                                custom_header = f"{field_name}_{col}"
                                custom[custom_header] = col
                for item, val in custom.items():
                    columns[item] = val
            else:
                columns[field_name] = field_name
        header_prefix = cls.model_fields["header_prefix"].get_default()
        headers = [header_prefix]
        headers.extend([x for x in columns])
        return "\t".join(headers)
