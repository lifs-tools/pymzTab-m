import abc
from typing import Annotated, Any, List, Literal, Mapping, Optional, OrderedDict, Union

from pydantic import (
    Field,
    ModelWrapValidatorHandler,
    ValidationInfo,
    model_validator,
)

from mztab_m_io.model.field_utils import sanitize_str
from mztab_m_io.model.serialization import (
    CompactObjectModel,
    CustomSerializer,
    IdentifiableModel,
    MetadataSerialization,
    MzTabSerializableModel,
    SerializationContext,
    ValidationPolicy,
)
from mztab_m_io.model.validation import ValidationContext

AdductIon = Annotated[str, Field(pattern=r"^\[\d*M([+-][\w\d]+)*\]\d*[+-]$")]


class Parameter(CompactObjectModel, IdentifiableModel, CustomSerializer):
    cv_label: Annotated[
        Optional[str],
        Field(
            description="CV label",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = ""
    cv_accession: Annotated[
        Optional[str],
        Field(
            description="CV accession in CURIE format",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(value_constraint="curie")
            ).model_dump(),
        ),
    ] = ""
    name: Annotated[
        Optional[str],
        Field(
            description="The name of the parameter term.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = ""
    value: Annotated[
        Optional[str],
        Field(
            description="The user value for the parameter.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = ""

    def to_tsv(self, context: SerializationContext) -> str:
        return (
            f"[{sanitize_str(self.cv_label)}, "
            f"{sanitize_str(self.cv_accession)}, "
            f"{sanitize_str(self.name)}, "
            f"{sanitize_str(self.value)}]"
        )

    @model_validator(mode="wrap")
    @classmethod
    def validate_model(
        cls,
        data: Any,
        handler: ModelWrapValidatorHandler["Parameter"],
        info: ValidationInfo,
    ) -> "Parameter":
        if not data:
            return None
        if isinstance(data, Parameter):
            return handler(data)
        if info and isinstance(info.context, ValidationContext):
            if info.context.source_format in {"json", "yaml"}:
                return handler(data)

        val = data
        if isinstance(val, Mapping):
            if len(val) == 1 and None in val:
                val = data[None]
        if isinstance(val, str):
            cleaned = val.strip("[]")
            parts = cleaned.split(",", maxsplit=3)

            cv_label = parts[0].strip() if len(parts) > 0 else ""
            cv_accession = parts[1].strip() if len(parts) > 1 else ""
            name = parts[2].strip() if len(parts) > 2 else ""
            value = parts[3].strip() if len(parts) > 3 else ""

            val = {
                "cv_label": cv_label,
                "cv_accession": cv_accession,
                "name": name,
                "value": value,
            }
        return handler(val)


class ExtendedParameter(Parameter):
    value: Annotated[
        Optional[str | Parameter],
        Field(
            description="The user value for the parameter.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    def to_tsv(self, context: SerializationContext) -> str:
        if isinstance(self.value, Parameter):
            return (
                f"[{sanitize_str(self.cv_label)}, "
                f"{sanitize_str(self.cv_accession)}, "
                f"{sanitize_str(self.name)}, "
                f"{sanitize_str(self.value.to_tsv(context))}]"
            )
        return super().to_tsv(context)

    @model_validator(mode="wrap")
    @classmethod
    def validate_model(
        cls,
        data: Any,
        handler: ModelWrapValidatorHandler["ExtendedParameter"],
        info: ValidationInfo,
    ) -> "ExtendedParameter":
        if not data:
            return None
        if isinstance(data, ExtendedParameter):
            return handler(data)
        if info and isinstance(info.context, ValidationContext):
            if info.context.source_format in {"json", "yaml"}:
                return handler(data)

        val = data
        if isinstance(val, Mapping):
            if len(val) == 1 and None in val:
                val = data[None]
        if isinstance(val, dict):
            value_str = val.get("value", "")
            value_str = value_str.strip('"')
            if value_str.startswith("["):
                value = Parameter.model_validate(value_str.strip("[]"))
                val["value"] = value.model_dump(by_alias=True)
        elif isinstance(val, str):
            cleaned = val.strip("[]")
            parts = cleaned.split(",", maxsplit=3)

            cv_label = parts[0].strip() if len(parts) > 0 else ""
            cv_accession = parts[1].strip() if len(parts) > 1 else ""
            name = parts[2].strip() if len(parts) > 2 else ""
            value = ""
            if len(parts) > 3:
                value_str = parts[3].strip('"').strip()
                value = value_str
                if value_str.startswith("["):
                    value = Parameter.model_validate(value_str.strip("[]"))

            val = {
                "cv_label": cv_label,
                "cv_accession": cv_accession,
                "name": name,
                "value": value.strip('"'),
            }
        return handler(val)


class Instrument(IdentifiableModel):
    name: Annotated[
        Optional[Parameter],
        Field(
            description="The instrument's name.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    source: Annotated[
        Optional[Parameter],
        Field(
            description="The instrument's ion source.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    analyzer: Annotated[
        Optional[List[Parameter]],
        Field(
            description="The instrument's mass analyzer, as defined by the parameter.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    detector: Annotated[
        Optional[Parameter],
        Field(
            description="The instrument's mass analyzer, as defined by the parameter.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    @model_validator(mode="wrap")
    @classmethod
    def validate_model(
        cls,
        data: Any,
        handler: ModelWrapValidatorHandler["Instrument"],
        info: ValidationInfo,
    ) -> "Instrument":
        if info and isinstance(info.context, ValidationContext):
            if info.context.source_format in {"json", "yaml"}:
                return handler(data)
        if isinstance(data, Mapping):
            if "analyzer" in data:
                val = data["analyzer"]
                if isinstance(val, (str, Parameter)):
                    data["analyzer"] = [val]
        return handler(data)


class Protocol(IdentifiableModel):
    name: Annotated[
        Optional[str],
        Field(
            description="The protocol name.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = None
    type: Annotated[
        Optional[Parameter],
        Field(
            description="The protocol type, as defined by the parameter.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = None
    description: Annotated[
        Optional[str],
        Field(
            description="Description of the protocol.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy()
            ).model_dump(),
        ),
    ] = None
    parameters: Annotated[
        Optional[List[ExtendedParameter]],
        Field(
            description="The protocol parameters.",
            json_schema_extra=MetadataSerialization(
                list_concatenation_str="|"
            ).model_dump(),
        ),
    ] = None


class SampleProcessing(IdentifiableModel):
    sample_processing: Annotated[
        Optional[List[Parameter]],
        Field(
            description="Parameters specifying sample processing "
            "that was applied within one step.",
            json_schema_extra=MetadataSerialization(
                list_concatenation_str="|", object_level_value=True
            ).model_dump(),
        ),
    ] = None


class Software(IdentifiableModel):
    parameter: Annotated[
        Optional[Parameter],
        Field(
            description="The software utilized.",
            json_schema_extra=MetadataSerialization(
                object_level_value=True,
            ).model_dump(),
        ),
    ] = None
    setting: Annotated[
        Optional[List[str]],
        Field(
            description="A software setting used. "
            "This field MAY occur multiple times for a single software. "
            "The value of this field is deliberately set as a String, "
            "since there currently do not exist cvParams for every possible setting.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None


class PublicationItem(MzTabSerializableModel, CustomSerializer):
    type: Annotated[
        Optional[str],
        Field(
            description="The type qualifier of this publication item.",
            examples=["doi", "pubmed", "uri"],
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(pattern=r"doi|pubmed|uri")
            ).model_dump(),
        ),
    ] = None
    accession: Annotated[
        Optional[str],
        Field(
            description="The native accession id for this publication item.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = None

    def to_tsv(self, context: SerializationContext) -> str:
        return f"{sanitize_str(self.type)}:{sanitize_str(self.accession)}"

    @model_validator(mode="wrap")
    @classmethod
    def deserialize(
        cls,
        data: Any,
        handler: ModelWrapValidatorHandler["PublicationItem"],
        info: ValidationInfo,
    ) -> "PublicationItem":
        if isinstance(data, PublicationItem):
            return handler(data)
        if info and isinstance(info.context, ValidationContext):
            if info.context.source_format in {"json", "yaml"}:
                return handler(data)
        val = data
        if isinstance(data, (OrderedDict, dict)):
            if len(data) == 1 and None in data:
                val = data[None]
        if isinstance(val, str) and ":" in val:
            parts = val.split(":", maxsplit=1)
            val = {"type": parts[0], "accession": parts[1]}
        return handler(val)


class Contact(IdentifiableModel):
    name: Annotated[
        Optional[str],
        Field(
            description="The contact's name.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    affiliation: Annotated[
        Optional[str],
        Field(
            description="The contact's affiliation.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    email: Annotated[
        Optional[str],
        Field(
            description="The contact's e-mail address.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(
                    value_constraint="email",
                )
            ).model_dump(),
        ),
    ] = None
    orcid: Annotated[
        Optional[str],
        Field(
            description="The contact's orcid id, without https prefix.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(
                    pattern=r"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]{1}$",
                )
            ).model_dump(),
        ),
    ] = None


class Uri(IdentifiableModel):
    value: Annotated[
        Optional[str],
        Field(
            description="The URI pointing to the external resource.",
            json_schema_extra=MetadataSerialization(
                object_level_value=True,
                validation_policy=ValidationPolicy(value_constraint="any-url"),
            ).model_dump(),
        ),
    ] = None


class Sample(IdentifiableModel):
    name: Annotated[
        Optional[str],
        Field(
            description="The sample's name.",
            json_schema_extra=MetadataSerialization(
                object_level_value=True
            ).model_dump(),
        ),
    ] = None
    custom: Annotated[
        Optional[List[Parameter]],
        Field(
            description="Additional user or cv parameters.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    species: Annotated[
        Optional[List[Parameter]],
        Field(
            description="Biological species information on the sample.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    tissue: Annotated[
        Optional[List[Parameter]],
        Field(
            description="Biological tissue information on the sample.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    cell_type: Annotated[
        Optional[List[Parameter]],
        Field(
            description="Biological cell type information on the sample.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    disease: Annotated[
        Optional[List[Parameter]],
        Field(
            description="Disease information on the sample.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    description: Annotated[
        Optional[str],
        Field(
            description="A free form description of the sample.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None


class MsRun(IdentifiableModel):
    name: Annotated[
        Optional[str],
        Field(
            description="The msRun's name.",
            json_schema_extra=MetadataSerialization(ignore=True).model_dump(),
        ),
    ] = None
    location: Annotated[
        Optional[str],
        Field(
            description="The msRun's location URI.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(
                    required=True, value_constraint="any-url"
                )
            ).model_dump(),
        ),
    ] = None
    instrument_ref: Annotated[
        Optional[int],
        Field(
            description="Sample reference.",
            json_schema_extra=MetadataSerialization(
                referenced_field_name="instrument",
            ).model_dump(),
        ),
    ] = None

    format: Annotated[
        Optional[Parameter],
        Field(
            description="The format of the MS run file.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    id_format: Annotated[
        Optional[Parameter],
        Field(
            description="The format of the IDs in the MS run file.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    fragmentation_method: Annotated[
        Optional[List[Parameter]],
        Field(
            description="The fragmentation methods applied during this msRun.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    scan_polarity: Annotated[
        Optional[List[Parameter]],
        Field(
            description="The scan polarity/polarities used during this msRun.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    hash: Annotated[
        Optional[str],
        Field(
            description="The file hash value of this msRun's data file.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    hash_method: Annotated[
        Optional[Parameter],
        Field(
            description="The method used to calculate the hash.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    parameters: Annotated[
        Optional[List[ExtendedParameter]],
        Field(
            description="Additional parameters of the assay, separated by bars.",
            json_schema_extra=MetadataSerialization(
                list_concatenation_str="|"
            ).model_dump(),
        ),
    ] = None


class Assay(IdentifiableModel):
    name: Annotated[
        Optional[str],
        Field(
            description="The assay name.",
            json_schema_extra=MetadataSerialization(
                object_level_value=True,
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    custom: Annotated[
        Optional[List[Parameter]],
        Field(
            description="Additional user or cv parameters.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = []
    external_uri: Annotated[
        Optional[str],
        Field(
            description="An external URI to further information about this assay.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(value_constraint="any-url"),
            ).model_dump(),
        ),
    ] = None
    sample_ref: Annotated[
        Optional[int],
        Field(
            description="Sample reference.",
            json_schema_extra=MetadataSerialization(
                referenced_field_name="sample",
            ).model_dump(),
        ),
    ] = None
    ms_run_refs: Annotated[
        Optional[List[int]],
        Field(
            alias="ms_run_ref",
            description="The ms run(s) referenced by this assay.",
            json_schema_extra=MetadataSerialization(
                referenced_field_name="ms_run",
                list_concatenation_str="|",
                validation_policy=ValidationPolicy(
                    required=True, minimum=1, value_constraint="non-negative-integer"
                ),
            ).model_dump(),
        ),
    ] = None
    protocol_refs: Annotated[
        Optional[List[int]],
        Field(
            description="The protocol(s) referenced by this assay.",
            json_schema_extra=MetadataSerialization(
                referenced_field_name="protocol",
                list_concatenation_str="|",
                validation_policy=ValidationPolicy(
                    value_constraint="non-negative-integer"
                ),
            ).model_dump(),
        ),
    ] = []
    parameters: Annotated[
        Optional[List[ExtendedParameter]],
        Field(
            description="Additional parameters of the assay, separated by bars.",
            json_schema_extra=MetadataSerialization(
                list_concatenation_str="|"
            ).model_dump(),
        ),
    ] = None


class CV(IdentifiableModel):
    label: Annotated[
        Optional[str],
        Field(
            description="The abbreviated CV label.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    full_name: Annotated[
        Optional[str],
        Field(
            description="The full name of this CV, for humans.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    version: Annotated[
        Optional[str],
        Field(
            description="The CV version used when the file was generated.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    uri: Annotated[
        Optional[str],
        Field(
            description="A URI to the CV definition.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(
                    required=True, value_constraint="any-url"
                ),
            ).model_dump(),
        ),
    ] = None


class Database(IdentifiableModel):
    param: Annotated[
        Parameter,
        Field(
            description="The database name.",
            json_schema_extra=MetadataSerialization(
                object_level_value=True,
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    prefix: Annotated[
        Optional[str],
        Field(
            description="The prefix used in the “identifier” column of data tables. "
            "For the 'no database' case 'null' must be used.",
            json_schema_extra=MetadataSerialization(
                validation_policy=(
                    ValidationPolicy(required=True, enforcement_level="recommended")
                )
            ).model_dump(),
        ),
    ] = None
    version: Annotated[
        Optional[str],
        Field(
            description="The database version is mandatory where identification "
            "has been performed. This may be a formal version number "
            "e.g. “1.4.1”, a date of access “2016-10-27” (ISO-8601 format) "
            "or “Unknown” if there is no suitable version that can be annotated.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    uri: Annotated[
        Optional[str],
        Field(
            description="The URI to the database. "
            "For the “no database” case, 'null' must be reported.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(
                    required=True,
                    enforcement_level="recommended",
                )
            ).model_dump(),
        ),
    ] = None

    def get_id(self):
        return self.param.id if self.param else None


class Publication(IdentifiableModel):
    publication_items: Annotated[
        Optional[List[PublicationItem]],
        Field(
            description="The publication item ids referenced by this publication.",
            json_schema_extra=MetadataSerialization(
                object_level_value=True,
                list_concatenation_str="|",
                validation_policy=ValidationPolicy(required=True, minimum=1),
            ).model_dump(),
        ),
    ] = None


class StudyVariableGroup(IdentifiableModel):
    name: Annotated[
        Optional[Parameter],
        Field(
            description="The study variable group name.",
            json_schema_extra=MetadataSerialization(
                object_level_value=True,
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None

    description: Annotated[
        Optional[str],
        Field(
            description="Description of the study variable group.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    type: Annotated[
        Optional[Parameter],
        Field(
            description="The study variable group type, as defined by the parameter.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    datatype: Annotated[
        Optional[
            Literal[
                "xsd:string",
                "xsd:integer",
                "xsd:decimal",
                "xsd:boolean",
                "xsd:date",
                "xsd:time",
                "xsd:dateTime",
                "xsd:anyURI",
            ]
        ],
        Field(
            description="The study variable group datatype",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    unit: Annotated[
        Optional[Parameter],
        Field(
            description="The study variable group unit, as defined by the parameter.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None


class StudyVariable(IdentifiableModel):
    name: Annotated[
        Optional[str],
        Field(
            description="The study variable name.",
            json_schema_extra=MetadataSerialization(
                object_level_value=True,
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    group_refs: Annotated[
        Optional[List[int]],
        Field(
            description="The study variable group this study variable belongs to.",
            json_schema_extra=MetadataSerialization(
                referenced_field_name="study_variable_group",
                validation_policy=ValidationPolicy(
                    value_constraint="non-negative-integer"
                ),
            ).model_dump(),
        ),
    ] = None
    assay_refs: Annotated[
        Optional[List[int]],
        Field(
            description="The assays referenced by this study variable.",
            json_schema_extra=MetadataSerialization(
                referenced_field_name="assay",
                list_concatenation_str="|",
                validation_policy=ValidationPolicy(
                    value_constraint="non-negative-integer"
                ),
            ).model_dump(),
        ),
    ] = None
    ms_run_refs: Annotated[
        Optional[List[int]],
        Field(
            description="The ms run(s) referenced by this study variable.",
            json_schema_extra=MetadataSerialization(
                referenced_field_name="ms_run",
                list_concatenation_str="|",
                validation_policy=ValidationPolicy(
                    value_constraint="non-negative-integer"
                ),
            ).model_dump(),
        ),
    ] = None
    average_function: Annotated[
        Optional[Parameter],
        Field(
            description="The function used to calculate "
            "the study variable quantification value "
            "and the operation used is not arithmetic mean (default). "
            "e.g. geometric mean, median.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    variation_function: Annotated[
        Optional[Parameter],
        Field(
            description="The function used to calculate "
            "the study variable quantification variation value "
            "if it is reported and the operation used is not coefficient of variation "
            "(default). e.g. standard error.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    description: Annotated[
        Optional[str],
        Field(
            description="A free-form description of this study variable.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    factors: Annotated[
        Optional[List[Parameter]],
        Field(
            description="Parameters indicating which factors were used "
            "for the assays referenced by this study variable, and at which levels.",
            json_schema_extra=MetadataSerialization(
                list_concatenation_str="|"
            ).model_dump(),
        ),
    ] = None


class SpectraReference(MzTabSerializableModel, CustomSerializer):
    ms_run_ref: Annotated[
        Optional[int],
        Field(
            validation_alias="ms_run",
            # alias="ms_run_ref",
            description="Reference to MsRun",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(
                    required=True, value_constraint="positive-integer"
                )
            ).model_dump(),
        ),
    ] = None
    reference: Annotated[
        Optional[str],
        Field(
            description="The (vendor-dependent) reference string "
            "to the actual mass spectrum.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = None

    def to_tsv(self, context: SerializationContext) -> str:
        return f"ms_run[{self.ms_run_ref}]:{sanitize_str(self.reference)}"

    @model_validator(mode="wrap")
    @classmethod
    def validate_model(
        cls,
        data: Any,
        handler: ModelWrapValidatorHandler["SpectraReference"],
        info: ValidationInfo,
    ) -> "SpectraReference":
        if isinstance(data, SpectraReference):
            return handler(data)
        if info and isinstance(info.context, ValidationContext):
            if info.context.source_format in {"json", "yaml"}:
                return handler(data)
        val = data
        if isinstance(val, Mapping):
            if len(val) == 1 and None in val:
                val = data[None]

        if isinstance(val, str):
            parts = val.strip().split(":", maxsplit=1)
            if len(parts) < 2:
                return None
            ms_run_val = parts[0].removeprefix("ms_run").strip("[]")
            ms_run = int(ms_run_val)
            val = {
                "ms_run_ref": ms_run,
                "reference": parts[1].strip(),
            }
        return handler(val)


class ColumnParameterMapping(
    MzTabSerializableModel, CompactObjectModel, CustomSerializer
):
    column_name: Annotated[
        Optional[str],
        Field(
            description="The fully qualified target column name.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = None
    param: Annotated[
        Optional[Parameter],
        Field(
            description="The parameter defining the unit.",
            json_schema_extra=MetadataSerialization(
                object_level_value=True,
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None

    def to_tsv(self, context: SerializationContext) -> str:
        if self.param:
            return f"{sanitize_str(self.column_name)}={self.param.to_tsv(context)}"
        return f"{sanitize_str(self.column_name)}=null"

    @model_validator(mode="wrap")
    @classmethod
    def validate_model(
        cls,
        data: Any,
        handler: ModelWrapValidatorHandler["OptColumnMapping"],
        info: ValidationInfo,
    ) -> "ColumnParameterMapping":
        if not data:
            return None
        if isinstance(data, ColumnParameterMapping):
            return handler(data)
        if info and isinstance(info.context, ValidationContext):
            if info.context.source_format in {"json", "yaml"}:
                return handler(data)
        val = data
        if isinstance(val, Mapping):
            if len(val) == 1 and None in val:
                val = data[None]
        if isinstance(val, str):
            parts = val.split("=", maxsplit=1)

            if len(parts) < 2:
                return None
            if parts[0]:
                val = {
                    "column_name": parts[0].strip() if parts[0] else None,
                    "param": Parameter.model_validate(parts[1].strip())
                    if parts[1]
                    else None,
                }

        return handler(val)


class OptionalTableColumn(abc.ABC):
    """
    An abstract base class to show that a model is a optional table column.
    """

    @abc.abstractmethod
    def get_header(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_value(self) -> Union[int, float, bool, str, MzTabSerializableModel, None]:
        raise NotImplementedError


class OptColumnMapping(MzTabSerializableModel, OptionalTableColumn):
    identifier: Annotated[
        Union[None, Parameter, str],
        Field(
            description="The fully qualified column name.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(
                    required=True,
                    pattern=r"^global|ms_run\[\d+\]|assay\[\d+\]|study_variable\[\d+\]",
                )
            ).model_dump(),
        ),
    ] = None
    param: Annotated[
        Optional[Parameter],
        Field(
            description="The fully qualified column parameter.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = None
    value: Annotated[
        Optional[str],
        Field(
            description="The value for this column in a particular row.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    def get_header(self) -> str:
        if self.param and self.param.cv_accession:
            return (
                f"opt_{self.identifier}_cv_{self.param.cv_accession}_{self.param.name}"
            )
        elif self.param and self.param.name:
            return f"opt_{self.identifier}_{self.param.name}"
        return f"opt_{self.identifier}"

    def get_value(self) -> str:
        return self.value


class Comment(MzTabSerializableModel, CustomSerializer):
    """
    Comment lines can be placed anywhere in an mzTab file.
    These lines must start with the three-letter code COM
    and are ignored by most parsers.
    Empty lines can also occur anywhere in an mzTab file and are ignored.
    """

    __mztab_example__ = "COM\tThis is a comment"

    prefix: Annotated[
        str,
        Field(
            description="Comment prefix",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True, pattern=r"COM")
            ).model_dump(),
        ),
    ] = "COM"

    msg: Annotated[
        Optional[str],
        Field(
            description="message",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = ""

    line_number: Annotated[
        Optional[int],
        Field(
            description="line number",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(value_constraint="positive-integer")
            ).model_dump(),
        ),
    ] = None

    def to_tsv(self, context: SerializationContext) -> str:
        return f"{self.prefix}\t{self.msg}"


__all__ = [
    "AdductIon",
    "Parameter",
    "Instrument",
    "SampleProcessing",
    "Software",
    "PublicationItem",
    "Contact",
    "Uri",
    "Sample",
    "MsRun",
    "Assay",
    "CV",
    "Database",
    "Publication",
    "StudyVariable",
    "SpectraReference",
    "ColumnParameterMapping",
    "OptColumnMapping",
    "Comment",
]
