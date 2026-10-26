import re
from typing import (
    Annotated,
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    OrderedDict,
    Tuple,
)

from pydantic import (
    Field,
    ValidationInfo,
)
from pydantic.functional_validators import ModelWrapValidatorHandler, model_validator

from mztab_m_io.model.base import MzTabBaseModel
from mztab_m_io.model.common import (
    CV,
    Assay,
    ColumnParameterMapping,
    Contact,
    Database,
    ExtendedParameter,
    Instrument,
    MsRun,
    Parameter,
    Protocol,
    Publication,
    Sample,
    SampleProcessing,
    Software,
    StudyVariable,
    StudyVariableGroup,
    Uri,
)
from mztab_m_io.model.field_utils import get_field_type_info, sanitize_str
from mztab_m_io.model.serialization import (
    CompactObjectModel,
    CustomSerializer,
    IdentifiableModel,
    MetadataInfo,
    MetadataSerialization,
    MzTabSerializableModel,
    SerializationContext,
    ValidationPolicy,
)
from mztab_m_io.model.validation import (
    Category,
    MessageType,
    MzTabMessage,
    ValidationContext,
)


class Metadata(MzTabSerializableModel, CustomSerializer):
    prefix: Annotated[
        Optional[str],
        Field(
            description="Metadata section prefix identifier.\n\n"
            "Value must be 'MTD'. Used to identify metadata lines "
            "in the mzTab-M file format.",
            examples=["MTD"],
            frozen=True,
            json_schema_extra=MetadataSerialization(
                ignore=True,
                validation_policy=ValidationPolicy(required=True, pattern=r"MTD"),
            ).model_dump(),
        ),
    ] = "MTD"

    mztab_version: Annotated[
        Optional[str],
        Field(
            alias="mzTab-version",
            description="Version number of the mzTab format used.\n\n"
            "Format: `major.minor.patch-variant`\n"
            'Must end with "-M" suffix for metabolomics variant.\n\n'
            "Used to ensure compatibility and processing correctness.",
            examples=["2.0.0-M", "2.1.0-M"],
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(
                    required=True, pattern=r"^\d{1}\.\d{1}\.\d{1}-[A-Z]{1}$"
                )
            ).model_dump(),
        ),
    ] = "2.1.0-M"

    mztab_id: Annotated[
        Optional[str],
        Field(
            alias="mzTab-ID",
            description="Unique identifier for the mzTab-M document.\n"
            "REQUIRED. Can be:\n"
            "- Repository accession number (e.g., MTBLS214)\n"
            "- Laboratory internal identifier\n"
            "- Study-specific identifier\n"
            "NOT intended as a globally unique identifier,\n"
            "but SHOULD have local meaning within its context.",
            examples=["MTBLS214", "LAB001_2023", "STUDY123_BATCH1"],
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = None

    title: Annotated[
        Optional[str],
        Field(
            description="Human-readable title of the experiment or study.\n"
            "OPTIONAL. SHOULD be:\n"
            "- Concise but informative\n"
            "- Reflect the main focus of the study\n"
            "- Unique within a collection of related studies",
            examples=[
                "Metabolomic Analysis of Human Plasma in Diabetes Type 2",
                "Lipidomics Study of Brain Tissue in Alzheimer's Disease",
            ],
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    description: Annotated[
        Optional[str],
        Field(
            description="Detailed description of the experiment or study.\n"
            "OPTIONAL. SHOULD include:\n"
            "- Study objectives\n"
            "- Experimental design overview\n"
            "- Key methodological approaches\n"
            "- Any unique aspects of the study\n"
            "Provides context for understanding the data and its significance.",
            examples=[
                "Investigation of metabolic changes in human plasma samples "
                "from type 2 diabetes patients compared to healthy controls. "
                "Study includes both fasting and post-prandial measurements.",
                "Analysis of lipid profiles in brain tissue samples examining "
                "the relationship between specific lipid species and "
                "Alzheimer's disease progression.",
            ],
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    contact: Annotated[
        Optional[List[Contact]],
        Field(
            description="Contact information for study personnel.\n\n"
            "Format\n"
            "- Name: `[first name] [initials] [last name]`\n"
            "- Multiple contacts numbered `[1-n]`\n\n"
            "Fields\n"
            "- Name of the contact person\n"
            "- Institutional affiliation\n"
            "- Email address",
            examples=[
                "MTD\tcontact[1]\t[MS,MS:1000586,contact name,John X Smith]",
                "MTD\tcontact[1]-affiliation\tUniversity of Somewhere",
                "MTD\tcontact[1]-email\tjohn.smith@university.edu",
            ],
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    publication: Annotated[
        Optional[List[Publication]],
        Field(
            description="Associated research publications.\n\n"
            "Reference Format\n"
            "- PubMed IDs: prefix with `pubmed:`\n"
            "- DOIs: prefix with `doi:`\n"
            "- Multiple IDs: separate with `|`\n\n"
            "Multiple publications numbered `[1-n]`",
            examples=[
                "MTD\tpublication[1]\tdoi:10.1021/example.2023",
                "MTD\tpublication[2]\tpubmed:12345678|doi:10.1021/another.2023",
            ],
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    uri: Annotated[
        Optional[List[Uri]],
        Field(
            description="A URI pointing to the file's source data "
            "(e.g., a MetaboLights records).",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    external_study_uri: Annotated[
        Optional[List[Uri]],
        Field(
            description="A URI pointing to an external file with more details "
            "about the study design (e.g., an ISA-TAB file).",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    instrument: Annotated[
        Optional[List[Instrument]],
        Field(
            description="Mass spectrometry instrument specifications.\n\n"
            "Each instrument includes:\n"
            "- `name`: Full instrument name and model\n"
            "- `source`: Ion source type (e.g., ESI, MALDI)\n"
            "- `analyzer`: Mass analyzer(s) used (e.g., quadrupole, TOF)\n"
            "- `detector`: Detector type\n\n"
            "Multiple instruments are numbered `[1-n]`. "
            "Referenced by `instrument_ref` in `ms_run` entries.",
            examples=[
                "MTD\tinstrument[1]-name\tThermo Fisher Q Exactive HF",
                "MTD\tinstrument[1]-source\t[MS,MS:1000073,ESI,]",
                "MTD\tinstrument[1]-analyzer[1]\t[MS,MS:1000084,TOF,]",
            ],
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    quantification_method: Annotated[
        Optional[Parameter],
        Field(
            description="The quantification method used in the "
            "experiment reported in the file.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = None

    sample: Annotated[
        Optional[List[Sample]],
        Field(
            description="Specification of sample. "
            "A name for each sample to serve as a list of the samples "
            "that MUST be reported in the following tables. "
            "Samples MUST be reported if a statistical design is being captured "
            "(i.e. bio or tech replicates). "
            "If the type of replicates are not known, samples SHOULD NOT be reported. "
            "species: The respective species of the samples analysed. "
            "For more complex cases, such as metagenomics, optional columns and "
            "userParams should be used."
            "tissue: The respective tissue(s) of the sample. "
            "cell_type: The respective cell type(s) of the sample. "
            "disease: The respective disease(s) of the sample. "
            "description: A human readable description of the sample. "
            "custom: Custom parameters describing the sample's additional properties. "
            "Dates MUST be provided in ISO-8601 format.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    protocol: Annotated[
        Optional[List[Protocol]],
        Field(
            description="The protocol(s) used in the experiment.",
            examples=[
                "MTD\tprotocol[1]-name\tMass Spectrometry\n",
                "MTD\tprotocol[1]-type\t[CHMO, CHMO:0000470, mass spectrometry, ]\n",
                "MTD\tprotocol[1]-description\tEluting compounds were detected ...\n",
                "MTD\tprotocol[1]-parameters\t[MS, MS:1000008, ionization type, "
                "[MS,MS:1000073, electrospray ionization, ]]\n",
            ],
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    sample_processing: Annotated[
        Optional[List[SampleProcessing]],
        Field(
            description="Sample preparation and processing steps.\n\n"
            "Processing Documentation\n"
            "- Sequential steps numbered `[1-n]` in order of execution\n"
            "- Multiple parameters per step separated by `|`\n\n"
            "Special Cases\n"
            "- Derivatization:\n"
            "  - Report general step (e.g., 'silylation')\n"
            "  - Specify agents in derivatization_agent field\n\n"
            "Follows biological/analytical methods report format",
            examples=[
                "MTD\tsample_processing[1]\t[SEP,SEP:00142,extraction,]",
                "MTD\tsample_processing[2]\t[SEP,SEP:00210,centrifugation,]|"
                "[SEP,SEP:00211,13000g]",
                "MTD\tsample_processing[3]\t[MS,MS:1000085,silylation,]",
            ],
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    software: Annotated[
        Optional[List[Software]],
        Field(
            description="Analysis software specifications.\n\n"
            "For each software entry:\n"
            "- Include version information\n"
            "- Number entries (`[1-n]`) to reflect usage order\n"
            "- Settings can be specified multiple times per software\n"
            "- Use string values for settings without CV terms",
            examples=[
                "MTD\tsoftware[1]\t[MS,MS:1000532,Xcalibur,3.1]",
                "MTD\tsoftware[2]\t[MS,MS:1002342,MetaboScape,2022b]",
            ],
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True, minimum=1)
            ).model_dump(),
        ),
    ] = None

    derivatization_agent: Annotated[
        Optional[List[Parameter]],
        Field(
            description="A description of derivatization agents "
            "applied to small molecules, "
            "using userParams or CV terms where possible.",
            examples=[
                "MTD\tderivatization_agent[1]\t[XLMOD, XLMOD:07014, "
                "N-methyl-N-t-butyldimethylsilyltrifluoroacetamide, ]"
            ],
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    ms_run: Annotated[
        Optional[List[MsRun]],
        Field(
            alias="ms_run",
            description="Specification of ms_run. "
            "location: Location of the external data file e.g. raw files on which "
            "analysis has been performed. "
            "If the actual location of the MS run is unknown, a “null” MUST be "
            "used as a place holder value, "
            "since the [1-n] cardinality is referenced elsewhere. "
            "If pre-fractionation has been performed, "
            "then [1-n] ms_runs SHOULD be created per assay."
            "instrument_ref: If different instruments are used in different runs, "
            "instrument_ref can be used to link a specific instrument "
            "to a specific run. "
            "format: Parameter specifying the data format of the "
            "external MS data file. "
            "If ms_run[1-n]-format is present, ms_run[1-n]-id_format "
            "SHOULD also be present, "
            "following the parameters specified in Table 1. "
            "id_format: Parameter specifying the id format used "
            "in the external data file. "
            "If ms_run[1-n]-id_format is present, ms_run[1-n]-format "
            "SHOULD also be present."
            "fragmentation_method: The type(s) of fragmentation "
            "used in a given ms run."
            "scan_polarity: The polarity mode of a given run. "
            "Usually only one value SHOULD be given here except for "
            "the case of mixed polarity runs."
            "hash: Hash value of the corresponding external MS data f"
            "ile defined in ms_run[1-n]-location. "
            "If ms_run[1-n]-hash is present, ms_run[1-n]-hash_method "
            "SHOULD also be present."
            "hash_method: A parameter specifying the hash methods used to "
            "generate the String in ms_run[1-n]-hash. "
            "Specifics of the hash method used MAY follow the definitions "
            "of the mzML format. "
            "If ms_run[1-n]-hash is present, ms_run[1-n]-hash_method "
            "SHOULD also be present.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True, minimum=1)
            ).model_dump(),
        ),
    ] = None

    assay: Annotated[
        Optional[List[Assay]],
        Field(
            description="Specification of assay. "
            "(empty) name: A name for each assay, to serve as a list of "
            "the assays that MUST be "
            "reported in the following tables. "
            "custom: Additional custom parameters or values for a given assay. "
            "external_uri: An external reference uri to further "
            "information about the assay, "
            "for example via a reference to an object within an ISA-TAB file. "
            "sample_ref: An association from a given assay to the sample analysed. "
            "ms_run_refs: An association from a given assay to the source MS run. "
            "All assays MUST reference exactly one ms_run unless a workflow with "
            "pre-fractionation "
            "is being encoded, in which case each assay MUST reference n ms_runs "
            "where n fractions have been collected. "
            "Multiple assays SHOULD reference the same ms_run to capture "
            "multiplexed experimental designs.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True, minimum=1)
            ).model_dump(),
        ),
    ] = None
    study_variable_group: Annotated[
        Optional[List[StudyVariableGroup]],
        Field(
            description="A parameter defining the group to which study variables "
            "belong, allowing grouping of related study variables that belong "
            "to the same experimental design factor in multi-factorial designs. "
            "For software that does not capture study variables, a single "
            "study_variable_group MUST be reported, linking to the single "
            "study variable, and MUST have the identifier 'undefined'.",
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None
    study_variable: Annotated[
        Optional[List[StudyVariable]],
        Field(
            description="Specification of study_variable. "
            "(empty) name: A name for each study variable (experimental "
            "condition or factor), "
            "to serve as a list of the study variables that MUST be "
            "reported in the following tables. "
            "For software that does not capture study variables, "
            "a single study variable MUST be reported, "
            "linking to all assays. This single study variable MUST have "
            "the identifier “undefined“. "
            "assay_refs: Bar-separated references to the IDs of assays "
            "grouped in the study variable. "
            "average_function: The function used to calculate the study variable "
            "quantification value "
            "and the operation used is not arithmetic mean (default) "
            "e.g. “geometric mean”, “median”. "
            "The 1-n refers to different study variables. "
            "variation_function: The function used to calculate "
            "the study variable quantification variation value "
            "if it is reported and the operation used is not coefficient "
            "of variation (default) e.g. "
            "“standard error”. description: A textual description of "
            "the study variable. "
            "group_refs: Related study variable group IDs.",
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True, minimum=1)
            ).model_dump(),
        ),
    ] = None

    custom: Annotated[
        Optional[List[ExtendedParameter]],
        Field(
            description="Any additional parameters describing the analysis reported.",
            examples=["MTD\tcustom\t[MS, MS:1000001, custom param, value]"],
            json_schema_extra=MetadataSerialization(
                list_concatenation_str="|"
            ).model_dump(),
        ),
    ] = None
    cv: Annotated[
        Optional[List[CV]],
        Field(
            description="Controlled vocabulary specifications.\n\n"
            "Fields\n"
            "- `label`: Short identifier (e.g., 'MS' for PSI-MS)\n"
            "- `full_name`: Complete ontology name\n"
            "- `version`: CV/ontology version\n"
            "- `uri`: Reference URI for the vocabulary",
            examples=[
                "MTD\tcv[1]-label\tMS",
                "MTD\tcv[1]-full_name\tPSI Mass Spectrometry Ontology",
                "MTD\tcv[1]-version\t4.1.0",
                "MTD\tcv[1]-uri\thttp://purl.obolibrary.org/obo/ms.obo",
            ],
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True, minimum=1)
            ).model_dump(),
        ),
    ]

    small_molecule_quantification_unit: Annotated[
        Optional[Parameter],
        Field(
            description="Defines what type of units are reported "
            "in the small molecule summary quantification / abundance fields",
            alias="small_molecule-quantification_unit",
            examples=[
                "MTD\tsmall_molecule-quantification_unit\t[MS, MS:1001113, peak area, ]"
            ],
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = None

    small_molecule_feature_quantification_unit: Annotated[
        Optional[Parameter],
        Field(
            description="Defines what type of units are reported in "
            "the small molecule feature quantification / abundance fields.",
            alias="small_molecule_feature-quantification_unit",
            examples=[
                "MTD\tsmall_molecule_feature-quantification_unit\t"
                "[MS, MS:1001113, peak area, ]"
            ],
            json_schema_extra=MetadataSerialization().model_dump(),
        ),
    ] = None

    small_molecule_identification_reliability: Annotated[
        Optional[Parameter],
        Field(
            description="The system used for giving reliability / confidence codes "
            "to small molecule identifications MUST be specified "
            "if not using the default codes.",
            alias="small_molecule-identification_reliability",
            examples=[
                "MTD\tsmall_molecule-identification_reliability\t"
                "[MS, MS:1000932, identification reliability, ]"
            ],
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True)
            ).model_dump(),
        ),
    ] = None

    database: Annotated[
        Optional[List[Database]],
        Field(
            description="Specification of databases. "
            "(empty): The description of databases used. "
            "For cases, where a known database has not been used for identification, "
            "a userParam SHOULD be inserted to describe any identification performed. "
            "e.g. de novo. "
            "If no identification has been performed at all then 'no database' "
            "should be inserted followed by null. prefix: The prefix used in the "
            "“identifier” column of data tables. "
            "For the 'no database' case 'null' must be used. "
            "version: The database version is mandatory "
            "where identification has been performed. "
            "This may be a formal version number e.g. “1.4.1”, "
            "a date of access “2016-10-27” (ISO-8601 format) or “Unknown” "
            "if there is no suitable version that can be annotated. "
            "uri: The URI to the database. "
            "For the 'no database' case, 'null' must be reported. ",
            examples=[
                "MTD\tdatabase[1]\t[MS, MS:1002992, HMDB, 4.0]",
                "MTD\tdatabase[1]-prefix\tHMDB",
                "MTD\tdatabase[1]-uri\thttp://www.hmdb.ca/metabolites/",
            ],
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True, minimum=1)
            ).model_dump(),
        ),
    ] = None

    id_confidence_measure: Annotated[
        Optional[List[Parameter]],
        Field(
            description="Small molecule identification confidence metrics.<br/>"
            "Scoring System\n"
            "- Use CV parameters numbered `[1-n]`\n"
            "- Define score direction (high-to-low or low-to-high)\n"
            "- Order by importance for identification ranking\n\n"
            "Scores determine confidence in molecular identifications",
            examples=[
                "MTD\tid_confidence_measure[1]\t[MS,MS:1002890,fragmentation score,]",
                "MTD\tid_confidence_measure[2]\t[MS,MS:1002891,retention time score,]",
            ],
            json_schema_extra=MetadataSerialization(
                validation_policy=ValidationPolicy(required=True, minimum=1)
            ).model_dump(),
        ),
    ] = None

    colunit_small_molecule: Annotated[
        Optional[List[ColumnParameterMapping]],
        Field(
            alias="colunit-small_molecule",
            description="Unit definitions for small molecule data columns.\n\n"
            "Format\n"
            "- Pattern: `{column_name}={unit_parameter}`\n"
            "- Use CV parameters for units when possible\n\n"
            "Important Notes\n"
            "- Not for quantification columns\n"
            "- Use `small_molecule-quantification_unit` for quantification values",
            examples=[
                "MTD\tcolunit-small_molecule\tretention_time=[UO,UO:0000031,minute,]",
                "MTD\tcolunit-small_molecule\tmass=[UO,UO:0000221,dalton,]",
            ],
            json_schema_extra=MetadataSerialization(
                non_indexed_list_value=True,
                json_schema_extra=MetadataSerialization().model_dump(),
            ).model_dump(),
        ),
    ] = None

    colunit_small_molecule_feature: Annotated[
        Optional[List[ColumnParameterMapping]],
        Field(
            alias="colunit-small_molecule_feature",
            description="Defines the used unit for a column in the "
            "small molecule feature section. "
            "The format of the value has to be {column name}="
            "{Parameter defining the unit}. "
            "This field MUST NOT be used to define a unit for quantification columns. "
            "The unit used for small molecule quantification values MUST be set "
            "in small_molecule_feature-quantification_unit.",
            examples=[
                "MTD\tcolunit-small_molecule_feature\tretention_time="
                "[UO, UO:0000031, minute, ]"
            ],
            json_schema_extra=MetadataSerialization(
                non_indexed_list_value=True,
                json_schema_extra=MetadataSerialization().model_dump(),
            ).model_dump(),
        ),
    ] = None

    colunit_small_molecule_evidence: Annotated[
        Optional[List[ColumnParameterMapping]],
        Field(
            alias="colunit-small_molecule_evidence",
            description="Defines the used unit for a column in the "
            "small molecule evidence section. "
            "The format of the value has to be {column name}="
            "{Parameter defining the unit}.",
            examples=[
                "MTD\tcolunit-small_molecule_evidence\tretention_time="
                "[UO, UO:0000031, minute, ]"
            ],
            json_schema_extra=MetadataSerialization(
                non_indexed_list_value=True,
                json_schema_extra=MetadataSerialization().model_dump(),
            ).model_dump(),
        ),
    ] = None

    def to_tsv(self, context: SerializationContext) -> str:
        lines = []
        prefix = self.__class__.model_fields.get("prefix", "").default
        self._serialize_object(prefix, "", self, lines, context)
        return "\n".join(lines)

    @model_validator(mode="wrap")
    @classmethod
    def validate_model(
        cls,
        input_data: Any,
        handler: ModelWrapValidatorHandler["Metadata"],
        info: ValidationInfo,
    ) -> "Metadata":
        if isinstance(input_data, Metadata):
            return handler(input_data)
        if info and info.context and isinstance(info.context, ValidationContext):
            if info.context.source_format in {"json", "yaml"}:
                return handler(input_data)

        data = input_data
        new_data = OrderedDict()
        for field, field_info in cls.model_fields.items():
            metadata_info = cls.get_metadata_info()
            json_extra: MetadataSerialization = (
                metadata_info.metadata_serializations.get(
                    field, cls.__default_serialization__
                )
            )
            if json_extra.ignore:
                continue
            val = None
            if field_info.validation_alias:
                field_name = field_info.validation_alias
                val = data.get(field_info.validation_alias)
            else:
                field_name = field
            if val is None:
                val = data.get(field)
            is_list, field_type = get_field_type_info(cls, field)
            if not is_list:
                if issubclass(field_type, str):
                    str_val = val
                    if isinstance(val, Mapping):
                        str_val = val.get(None)
                    new_data[field_name] = str_val
                elif issubclass(field_type, int):
                    int_val = val
                    if isinstance(val, Mapping):
                        int_val = val.get(None)
                    ref_match = re.match(r"(.+)\[(\d+)\]")
                    if ref_match:
                        int_val = ref_match.groups(1)
                    new_data[field_name] = None if int_val is None else int(int_val)
                elif issubclass(field_type, MzTabBaseModel):
                    if isinstance(val, MzTabBaseModel):
                        new_data[field_name] = val
                    else:
                        str_val = val
                        if isinstance(val, Mapping):
                            str_val = val.get(None)
                        new_data[field_name] = field_type.model_validate(
                            str_val, by_alias=True
                        )
            else:
                if issubclass(field_type, int):
                    int_val = val
                    if isinstance(val, Mapping):
                        int_val = val.get(None)
                    ref_match = re.match(r"(.+)\[(\d+)\]")
                    if ref_match:
                        int_val = ref_match.groups(1)
                    new_data[field_name] = None if int_val is None else int(int_val)
                elif issubclass(field_type, MzTabSerializableModel):
                    sub_field = val
                    if not val:
                        continue
                    metadata_info = field_type.get_metadata_info()
                    if json_extra.non_indexed_list_value:
                        if field_name not in new_data:
                            new_data[field_name] = []
                        current_list = new_data[field_name]
                        if isinstance(sub_field, list):
                            for item in sub_field:
                                if isinstance(item, MzTabBaseModel):
                                    current_list.append(item)
                                else:
                                    current_list.append(
                                        field_type.model_validate(item, by_alias=True)
                                    )
                        elif isinstance(sub_field, MzTabBaseModel):
                            current_list.append(sub_field)
                        else:
                            current_list.append(
                                field_type.model_validate(val, by_alias=True)
                            )
                    else:
                        new_list = []
                        sub_field = sub_field or []
                        for item in sub_field:
                            if isinstance(item, MzTabBaseModel):
                                new_list.append(item)
                            else:
                                cls._update_dict(metadata_info, item)
                                new_list.append(
                                    field_type.model_validate(item, by_alias=True)
                                )
                        new_data[field_name] = new_list or None

        return handler(new_data)

    @classmethod
    def parse_metadata(
        cls, lines: List[str], context: SerializationContext
    ) -> Dict[str, Any]:
        """Parse metadata section of mzTab-M file."""
        pattern = re.compile(
            r"^(?P<field>[^\[\]]+)"
            r"(?:\[(?P<field_index>\d+)\])?"
            r"(?:-(?P<subfield>[^\[\]]+)"
            r"(?:\[(?P<subfield_index>\d+)\])?)?$"
        )

        metadata_dict = OrderedDict()
        for line in lines:
            if not line.startswith("MTD") and not line.startswith("COM"):
                continue
            if line.startswith("COM"):
                if "comment" not in metadata_dict:
                    metadata_dict["comment"] = []
                parts = line.split("\t", maxsplit=1)
                if len(parts) < 2 or not parts[1]:
                    continue
                metadata_dict["comment"].append(
                    {"prefix": "COM", "msg": parts[1].strip()}
                )
                continue
            key, value = cls._parse_metadata_line(line)

            if not key:
                continue
            match = re.match(pattern, key)

            if match:
                parts = match.groups()
                field = parts[0]
                field_index = int(parts[1]) if parts[1] else None
                sub_field = parts[2]
                sub_field_index = int(parts[3]) if parts[3] else None
                cls._set_dict_value(
                    value=value,
                    data_dict=metadata_dict,
                    field=field,
                    field_index=field_index,
                    sub_field=sub_field,
                    sub_field_index=sub_field_index,
                )
            else:
                context.messages.append(
                    MzTabMessage(
                        message_type=MessageType.WARNING,
                        category=Category.FORMAT,
                        msg=f"unexpected line '{key}'",
                    )
                )

        return metadata_dict

    @classmethod
    def _parse_metadata_line(cls, line: str) -> Tuple[str, str]:
        """Parse a metadata line into key and value."""
        parts = line.split("\t", 2)
        if len(parts) < 3:
            return None, None
        key = parts[1]
        value = parts[2].strip()
        return key, value

    @classmethod
    def _update_dict(cls, metadata_info: MetadataInfo, item: Dict[str, Any]):
        if not item:
            return

        if metadata_info.object_level_value_field:
            if not item.get(metadata_info.object_level_value_field):
                item[metadata_info.object_level_value_field] = item.get(None, None)
                if None in item:
                    del item[None]
        for join_field, join_op in metadata_info.list_concatenation_str_dict.items():
            if join_field in item:
                item[join_field] = item[join_field] or ""
                if not isinstance(item[join_field], list):
                    item[join_field] = [
                        x.strip() for x in item[join_field].split(join_op)
                    ]
        for ref_field, ref in metadata_info.referenced_field_names.items():
            if ref_field in item:
                val = item[ref_field]
                if isinstance(val, list):
                    new_val = []
                    for v in val:
                        if not isinstance(v, int):
                            ref_match = re.match(rf"\s*{ref}\[(\d+)\]\s*", str(v))
                            if ref_match:
                                new_val.append(int(ref_match.groups()[0]))
                        else:
                            new_val.append(v)
                    item[ref_field] = new_val
                else:
                    if not isinstance(item[ref_field], int):
                        ref_match = re.match(rf"{ref}\[(\d+)\]", str(item[ref_field]))
                        if ref_match:
                            item[ref_field] = int(ref_match.groups()[0])

        for k, v in item.items():
            if (
                v is not None
                and k in metadata_info.subfield_lists
                and not isinstance(v, list)
            ):
                item[k] = [v]

    @classmethod
    def _set_dict_value(
        cls,
        value,
        data_dict,
        field: str,
        field_index: Optional[int],
        sub_field: str,
        sub_field_index: Optional[int],
    ):
        if field not in data_dict:
            if field_index is not None:
                data_dict[field] = []
            else:
                data_dict[field] = OrderedDict()
        base_item = data_dict[field]
        if field_index is not None:
            i = len(data_dict[field])
            if i < field_index:
                while i < field_index:
                    data_dict[field].append(None)
                    i += 1
                data_dict[field][field_index - 1] = OrderedDict()
            base_item = data_dict[field][field_index - 1]

        if sub_field not in base_item:
            if sub_field_index is not None:
                base_item[sub_field] = []
            else:
                base_item[sub_field] = OrderedDict()
        if sub_field_index is not None:
            i = len(base_item[sub_field])
            while i < sub_field_index:
                base_item[sub_field].append(None)
                i += 1
            base_item[sub_field][sub_field_index - 1] = value
        else:
            base_item[sub_field] = value

    def _quote(self, value: Any) -> str:
        """Quote a value if it contains whitespace."""
        return f'"{value}"' if "|" in str(value) or "," in str(value) else str(value)

    def _serialize_object(
        self,
        section: str,
        prefix: str,
        model: MzTabBaseModel,
        lines: List[str],
        context: SerializationContext,
    ):
        for field, field_info in model.__class__.model_fields.items():
            metadata_info = model.__class__.get_metadata_info()
            extra: MetadataInfo = metadata_info.metadata_serializations.get(
                field, self.__default_serialization__
            )
            if extra.ignore:
                continue
            value = getattr(model, field, None)
            alias = field_info.alias if field_info.alias else field
            key_name = alias
            if prefix:
                key_name = prefix if extra.object_level_value else f"{prefix}-{alias}"

            if value is None:
                continue
            elif isinstance(value, str):
                line = f"{section}\t{key_name}\t{sanitize_str(value)}"
                lines.append(line)
            elif isinstance(value, int):
                if value is None:
                    line = f"{section}\t{key_name}\t"
                elif extra.referenced_field_name:
                    ref = extra.referenced_field_name
                    line = f"{section}\t{key_name}\t{ref}[{value}]"
                else:
                    line = f"{section}\t{key_name}\t{value}"
                lines.append(line)
            elif isinstance(value, MzTabBaseModel):
                if isinstance(value, CompactObjectModel):
                    line_value = value.to_tsv(context)
                    line = f"{section}\t{key_name}\t{line_value or ''}"
                    lines.append(line)
                else:
                    self._serialize_object(section, key_name, value, line, context)
            elif isinstance(value, list):
                if not value:
                    continue
                if isinstance(value[0], str):
                    separator = extra.list_concatenation_str
                    if separator:
                        line_value = separator.join(
                            [sanitize_str(x, separator) for x in value]
                        )
                        line = f"{section}\t{key_name}\t{line_value}"
                    else:
                        for idx, item in enumerate(value, start=1):
                            indexed_key_name = f"{key_name}[{idx}]"
                            line = (
                                f"{section}\t{indexed_key_name}\t{sanitize_str(item)}"
                            )
                            lines.append(line)
                elif isinstance(value[0], int):
                    separator = extra.list_concatenation_str or "|"
                    if extra.referenced_field_name:
                        values = [f"{extra.referenced_field_name}[{x}]" for x in value]
                        line_value = separator.join(values)
                        line = f"{section}\t{key_name}\t{line_value}"
                    else:
                        values = [str(x) for x in value if x is not None]
                        line = f"{section}\t{key_name}\t{separator.join(values)}"
                    lines.append(line)
                elif isinstance(value[0], MzTabBaseModel):
                    separator = extra.list_concatenation_str or None
                    if separator:
                        if isinstance(value[0], CustomSerializer):
                            line_value = separator.join(
                                [x.to_tsv(context) for x in value]
                            )
                            line = f"{section}\t{key_name}\t{line_value or ''}"
                            lines.append(line)
                        else:
                            line_value = separator.join([str(x) for x in value])
                            line = f"{section}\t{key_name}\t{line_value or ''}"
                            lines.append(line)
                    else:
                        for idx, item in enumerate(value, start=1):
                            indexed_key_name = f"{key_name}[{idx}]"
                            if extra.non_indexed_list_value:
                                indexed_key_name = key_name
                            elif isinstance(item, IdentifiableModel):
                                id_val = item.get_id()
                                if id_val:
                                    indexed_key_name = f"{key_name}[{id_val}]"
                            if isinstance(item, CompactObjectModel):
                                line_value = item.to_tsv(context)
                                line = (
                                    f"{section}\t{indexed_key_name}\t{line_value or ''}"
                                )
                                lines.append(line)
                            else:
                                self._serialize_object(
                                    section, indexed_key_name, item, lines, context
                                )
                else:
                    context.messages.append(
                        MzTabMessage(
                            category=Category.WARNING,
                            message_type=MessageType.INFO,
                            message=f"not expected type: {type(value[0])} "
                            f"and value: {value[0]}",
                        )
                    )
            else:
                context.messages.append(
                    MzTabMessage(
                        category=Category.WARNING,
                        message_type=MessageType.INFO,
                        message=f"Skipping unsupported value: key: {key_name} "
                        f"extra: {extra}",
                    )
                )
