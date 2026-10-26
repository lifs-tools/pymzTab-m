from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal


class MzTabBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_default=True,
        validate_assignment=True,
        validation_error_cause=True,
        field_title_generator=lambda field_name, field_info: to_pascal(
            field_name.replace("_", " ").strip()
        ),
    )
