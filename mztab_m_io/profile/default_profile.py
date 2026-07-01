import json
from importlib import resources
from pathlib import Path

from jsonprofile.profile import BaseCvTerm
from jsonprofile.profile.constraints import (
    BooleanConstraint,
    CollectionConstraint,
    ConstraintGroup,
    CVListConstraint,
    CVTermConstraint,
    CVTermEnumConstraint,
    DecimalConstraint,
    EmailConstraint,
    Evaluation,
    IntegerConstraint,
    IntegerEnumConstraint,
    NotNullConstraint,
    OpaPolicyConstraint,
    PositiveIntegerConstraint,
    Precondition,
    RegexConstraint,
    StringConstraint,
    StringEnumConstraint,
    UriConstraint,
)
from jsonprofile.profile.model import (
    FieldRequirement,
    FieldRequirementGroup,
    JsonProfile,
    JsonProfileConfiguration,
    WasmFileDefinition,
)

import mztab_m_io

DEFAULT_NULL_VALUES = [None, "null", "", '""', "''"]
DEFAULT_MZTABM_OPA_POLICY_WASM_FILE = resources.files(mztab_m_io.__name__).joinpath(
    "resources/mztabm-default-2.1.0-M.wasm"
)
DEFAULT_MZTABM_OPA_POLICY_WASM_FILE_URL = "https://github.com/HUPO-PSI/mzTab-M/raw/refs/heads/development/mztab_m_io/resources/mztabm-default-2.1.0-M.wasm"


DEFAULT_PROFILE = JsonProfile(
    id="https://github.com/HUPO-PSI/mzTab-M/tree/main/schema/mztabm-default-profile-2.1.0-M.json",
    version="2.1.0-M",
    name="mzTab-M 2.1.0-M Default Profile",
    description="mzTab-M Default Profile is used "
    " for checking minimum valid mzTab-M files",
    configuration=JsonProfileConfiguration(
        default_wasm_file_key="default",
        wasm_file_definitions={
            "default": WasmFileDefinition(
                wasm_file_download_url=DEFAULT_MZTABM_OPA_POLICY_WASM_FILE_URL,
                wasm_file_path=str(DEFAULT_MZTABM_OPA_POLICY_WASM_FILE),
            ),
        },
    ),
    requirements={
        "": FieldRequirementGroup(
            description="MzTabM general cross check rules",
            requirements=[
                FieldRequirement(
                    code="D-0010",
                    description="Verifies that smallMoleculeSummary and "
                    "smallMoleculeEvidence rows define the same number of "
                    "abundance_assay values as assays declared in metadata.",
                    enforcement_level="required",
                    value_constraint=OpaPolicyConstraint(
                        entrypoint="mztabm/policies/policy_D_0010"
                    ),
                ),
            ],
        ),
        "$": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="D-0001",
                    enforcement_level="required",
                    required_properties=["metadata"],
                    recommended_properties=["smallMoleculeSummary"],
                ),
            ]
        ),
        "$.comment[*]": FieldRequirement(
            code="D-COMMENT-0001",
            value_constraint=RegexConstraint(json_path=".prefix", pattern=r"^COM$"),
        ),
        "$.comment[*].message": FieldRequirement(
            code="D-COMMENT-MESSAGE-0001", value_constraint=StringConstraint(minimum=1)
        ),
        "$.comment[*].line_number": FieldRequirement(
            code="D-COMMENT-LINE_NUMBER-0001",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.metadata": FieldRequirement(
            code="D-METADATA-0001",
            match_is_required=True,
            required_properties=[
                "prefix",
                "mzTab-version",
                "mzTab-ID",
                "quantification_method",
                "ms_run",
                "assay",
                "study_variable",
                "cv",
                "database",
                "small_molecule-quantification_unit",
                "id_confidence_measure",
            ],
            recommended_properties=[
                "contact",
                "publication",
                "software",
                "sample",
            ],
        ),
        "$.metadata.prefix": FieldRequirement(
            code="D-METADATA-PREFIX-0001",
            match_is_required=True,
            value_constraint=RegexConstraint(pattern=r"^MTD$"),
        ),
        "$.metadata.mzTab-version": FieldRequirement(
            code="D-METADATA-MZTAB_VERSION-0001",
            match_is_required=True,
            value_constraint=RegexConstraint(pattern=r"^\d{1}\.\d{1}\.\d{1}-[A-Z]{1}$"),
        ),
        "$.metadata.mzTab-ID": FieldRequirement(
            code="D-METADATA-MZTAB_ID-0001",
            match_is_required=True,
            value_constraint=StringConstraint(
                minimum=1, null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.metadata.instrument": FieldRequirement(
            code="D-METADATA-INSTRUMENT-0001",
            enforcement_level="recommended",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.instrument[*]": FieldRequirement(
            code="D-METADATA-INSTRUMENT-0010",
            enforcement_level="recommended",
            recommended_properties=["name"],
        ),
        "$.metadata.software": FieldRequirement(
            code="D-METADATA-SOFTWARE-0001",
            enforcement_level="recommended",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.software[*]": FieldRequirement(
            code="D-METADATA-SOFTWARE-0010",
            enforcement_level="recommended",
            required_properties=["parameter"],
        ),
        "$.metadata.software[*].parameter": FieldRequirement(
            code="D-METADATA-SOFTWARE-0011",
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.publication": FieldRequirement(
            code="D-MTD-PUBLICATION-0001",
            enforcement_level="recommended",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.publication[*]": FieldRequirement(
            code="D-MTD-PUBLICATION-0010",
            required_properties=["publication_items"],
            value_constraint=CollectionConstraint(
                min_occurs=1, json_path=".publication_items"
            ),
        ),
        "$.metadata.publication[*].publication_items[*]": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="D-MTD-PUBLICATION-0020",
                    required_properties=["type", "accession"],
                    value_constraint=ConstraintGroup(
                        constraints=[
                            RegexConstraint(
                                json_path=".type",
                                pattern=r"^doi|pubmed|uri$",
                                null_values=DEFAULT_NULL_VALUES,
                            ),
                            NotNullConstraint(
                                json_path=".accession", null_values=DEFAULT_NULL_VALUES
                            ),
                        ],
                    ),
                ),
                FieldRequirement(
                    code="D-MTD-PUBLICATION-0021",
                    value_constraint=RegexConstraint(
                        precondition=Precondition(
                            evaluations=[
                                Evaluation(
                                    json_path=".type",
                                    constraint=RegexConstraint(pattern=r"^doi$"),
                                    default_evaluation=False,
                                )
                            ]
                        ),
                        json_path=".accession",
                        pattern=r"^10\..+/.+$",
                        exceptional_values=[None],
                        null_values=DEFAULT_NULL_VALUES,
                    ),
                ),
                FieldRequirement(
                    code="D-MTD-PUBLICATION-0022",
                    value_constraint=RegexConstraint(
                        precondition=Precondition(
                            evaluations=[
                                Evaluation(
                                    json_path=".type",
                                    constraint=RegexConstraint(pattern=r"^pubmed$"),
                                ),
                            ]
                        ),
                        json_path=".accession",
                        pattern=r"^\d+$",
                        exceptional_values=[None],
                        null_values=DEFAULT_NULL_VALUES,
                    ),
                ),
                FieldRequirement(
                    code="D-MTD-PUBLICATION-0023",
                    value_constraint=UriConstraint(
                        precondition=Precondition(
                            evaluations=[
                                Evaluation(
                                    json_path=".type",
                                    constraint=RegexConstraint(pattern=r"^uri$"),
                                ),
                            ]
                        ),
                        json_path=".accession",
                        exceptional_values=[None],
                        null_values=DEFAULT_NULL_VALUES,
                    ),
                ),
            ]
        ),
        "$.metadata.contact": FieldRequirement(
            code="D-MTD-CONTACT-0001",
            enforcement_level="recommended",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.contact[*]": FieldRequirement(
            code="D-MTD-CONTACT-0010",
            enforcement_level="recommended",
            recommended_properties=["name", "email", "affiliation", "orcid"],
        ),
        "$.metadata.contact[*].name": FieldRequirement(
            code="D-MTD-CONTACT-NAME-0001",
            enforcement_level="recommended",
            value_constraint=StringConstraint(minimum=5),
        ),
        "$.metadata.contact[*].email": FieldRequirement(
            code="D-MTD-CONTACT-EMAIL-0001",
            value_constraint=EmailConstraint(),
        ),
        "$.metadata.contact[*].affiliation": FieldRequirement(
            code="D-MTD-CONTACT-AFFILIATION-0001",
            enforcement_level="recommended",
            value_constraint=StringConstraint(minimum=2),
        ),
        "$.metadata.contact[*].orcid": FieldRequirement(
            code="D-MTD-CONTACT-ORCID-0001",
            value_constraint=RegexConstraint(
                pattern=r"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[X0-9]$",
                null_values=DEFAULT_NULL_VALUES,
                exceptional_values=[None],
            ),
        ),
        "$.metadata.uri[*]": FieldRequirement(
            code="D-MTD-CONTACT-URI-0010",
            value_constraint=UriConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.metadata.external_study_uri[*]": FieldRequirement(
            code="D-MTD-CONTACT-EXTERNAL_STUDY_URI-0010",
            value_constraint=UriConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.metadata.quantification_method": FieldRequirement(
            code="D-MTD-CONTACT-QUANTIFICATION_METHOD-0001",
            match_is_required=True,
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.sample": FieldRequirement(
            code="D-MTD-SAMPLE-0001",
            enforcement_level="recommended",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.sample[*]": FieldRequirement(
            code="D-MTD-SAMPLE-0010",
            enforcement_level="recommended",
            required_properties=["name"],
            recommended_properties=["species"],
        ),
        "$.metadata.sample[*].name": FieldRequirement(
            code="D-MTD-SAMPLE-0011",
            value_constraint=StringConstraint(minimum=1),
        ),
        "$.metadata.sample[*].species[*]": FieldRequirement(
            code="D-MTD-SAMPLE-0020",
            enforcement_level="recommended",
            value_constraint=CVListConstraint(
                allowed_cv_list=["NCBITaxon", "ENVO", "CHEBI"]
            ),
        ),
        "$.metadata.ms_run": FieldRequirement(
            code="D-MTD-MS_RUN-0001",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.ms_run[*]": FieldRequirement(
            code="D-MTD-MS_RUN-0010",
            required_properties=["location"],
            recommended_properties=["instrument_ref"],
        ),
        "$.metadata.ms_run[*].location": FieldRequirement(
            code="D-MTD-MS_RUN-0020",
            value_constraint=UriConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.metadata.ms_run[*].scan_polarity": FieldRequirement(
            code="D-MTD-MS_RUN-0030",
            value_constraint=CollectionConstraint(max_occurs=2),
        ),
        "$.metadata.ms_run[*].scan_polarity[*]": FieldRequirement(
            code="D-MTD-MS_RUN-0031",
            value_constraint=CVTermEnumConstraint(
                allowed_cv_terms=[
                    BaseCvTerm(
                        cv_label="MS", cv_accession="MS:1000129", name="negative scan"
                    ),
                    BaseCvTerm(
                        cv_label="MS", cv_accession="MS:1000130", name="positive scan"
                    ),
                ]
            ),
        ),
        "$.metadata.ms_run[*].instrument_ref": FieldRequirement(
            code="D-MTD-MS_RUN-0040",
            enforcement_level="recommended",
            value_constraint=PositiveIntegerConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.metadata.assay": FieldRequirement(
            code="D-MTD-ASSAY-0001",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.assay[*]": FieldRequirement(
            code="D-MTD-ASSAY-0020",
            required_properties=["name", "ms_run_ref"],
            recommended_properties=["sample_ref"],
        ),
        "$.metadata.assay[*].name": FieldRequirement(
            code="D-MTD-ASSAY-0030",
            value_constraint=StringConstraint(minimum=1),
        ),
        "$.metadata.assay[*].ms_run_ref": FieldRequirement(
            code="D-MTD-ASSAY-0040",
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.assay[*].ms_run_ref[*]": FieldRequirement(
            code="D-MTD-ASSAY-0041",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.metadata.assay[*].protocol_refs[*]": FieldRequirement(
            code="D-MTD-ASSAY-0050",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.metadata.assay[*].sample_ref": FieldRequirement(
            code="D-MTD-ASSAY-0060",
            value_constraint=PositiveIntegerConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.metadata.assay[*].external_uri": FieldRequirement(
            code="D-MTD-ASSAY-0070",
            value_constraint=UriConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.metadata.protocol[*]": FieldRequirement(
            code="D-MTD-PROTOCOL-0010",
            required_properties=["name", "type"],
        ),
        "$.metadata.protocol[*].name": FieldRequirement(
            code="D-MTD-PROTOCOL-0020",
            value_constraint=StringConstraint(min_occurs=2),
        ),
        "$.metadata.protocol[*].type": FieldRequirement(
            code="D-MTD-PROTOCOL-0030",
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.study_variable_group[*]": FieldRequirement(
            code="D-MTD-STUDY_VARIABLE_GROUP-0010",
            required_properties=["name"],
            recommended_properties=["type", "datatype"],
        ),
        "$.metadata.study_variable_group[*].name": FieldRequirement(
            code="D-MTD-STUDY_VARIABLE_GROUP-0020",
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.study_variable_group[*].type": FieldRequirement(
            code="D-MTD-STUDY_VARIABLE_GROUP-0030",
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.study_variable_group[*].datatype": FieldRequirement(
            code="D-MTD-STUDY_VARIABLE_GROUP-0040",
            value_constraint=StringEnumConstraint(
                options=[
                    "xsd:string",
                    "xsd:integer",
                    "xsd:decimal",
                    "xsd:boolean",
                    "xsd:date",
                    "xsd:time",
                    "xsd:dateTime",
                    "xsd:anyURI",
                    "Parameter",
                ]
            ),
        ),
        "$.metadata.study_variable": FieldRequirement(
            code="D-MTD-STUDY_VARIABLE-0001",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.study_variable[*]": FieldRequirement(
            code="D-MTD-STUDY_VARIABLE-0020",
            required_properties=["name"],
            recommended_properties=["group_refs"],
        ),
        "$.metadata.study_variable[*].name": FieldRequirement(
            code="D-MTD-STUDY_VARIABLE-0030",
            value_constraint=ConstraintGroup(
                constraints=[
                    CVTermConstraint(allow_user_defined_terms=True),
                    StringConstraint(minimum=1),
                    IntegerConstraint(),
                    DecimalConstraint(),
                    BooleanConstraint(),
                ],
                join_operator="or",
            ),
        ),
        "$.metadata.study_variable[*].group_refs[*]": FieldRequirement(
            code="D-MTD-STUDY_VARIABLE-0041",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.metadata.study_variable[*].assay_refs[*]": FieldRequirement(
            code="D-MTD-STUDY_VARIABLE-0051",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.metadata.study_variable[*].ms_run_refs[*]": FieldRequirement(
            code="D-MTD-STUDY_VARIABLE-0061",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.metadata.custom[*]": FieldRequirement(
            code="D-MTD-CUSTOM-0010",
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.cv": FieldRequirement(
            code="D-MTD-CV-0001",
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.cv[*]": FieldRequirement(
            code="D-MTD-CV-0010",
            required_properties=["label", "full_name", "version", "uri"],
        ),
        "$.metadata.cv[*].label": FieldRequirement(
            code="D-MTD-CV-0020",
            value_constraint=StringConstraint(
                minimum=1, null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.metadata.cv[*].full_name": FieldRequirement(
            code="D-MTD-CV-0030",
            value_constraint=StringConstraint(
                minimum=1, null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.metadata.cv[*].version": FieldRequirement(
            code="D-MTD-CV-0040",
            value_constraint=StringConstraint(
                minimum=1,
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.metadata.cv[*].uri": FieldRequirement(
            code="D-MTD-CV-0050",
            value_constraint=UriConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.metadata.small_molecule-quantification_unit": FieldRequirement(
            code="D-MTD-SML_QUANTIFICATION_UNIT-0001",
            match_is_required=True,
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.small_molecule_feature-quantification_unit": FieldRequirement(
            code="D-MTD-SMF_QUANTIFICATION_UNIT-0001",
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.small_molecule-identification_reliability": FieldRequirement(
            code="D-MTD-SML_IDENTIFICATION_RELIABILITY-0001",
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.database": FieldRequirement(
            code="D-MTD-DATABASE-0001",
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.database[*]": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="D-MTD-DATABASE-0010",
                    required_properties=["param", "prefix", "version", "uri"],
                ),
                FieldRequirement(
                    code="D-MTD-DATABASE-0020",
                    value_constraint=CVTermConstraint(
                        json_path=".param", allow_user_defined_terms=True
                    ),
                ),
                FieldRequirement(
                    code="D-MTD-DATABASE-0030",
                    value_constraint=StringConstraint(
                        json_path=".version", minimum=1, exceptional_values=["Unknown"]
                    ),
                ),
                FieldRequirement(
                    code="D-MTD-DATABASE-0040",
                    value_constraint=UriConstraint(
                        json_path=".uri",
                        exceptional_values=[None],
                        null_values=DEFAULT_NULL_VALUES,
                    ),
                ),
            ]
        ),
        "$.metadata.id_confidence_measure": FieldRequirement(
            code="D-MTD-ID_CONFIDENCE_MEASURE-0001",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.id_confidence_measure[*]": FieldRequirement(
            code="D-MTD-ID_CONFIDENCE_MEASURE-0010",
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.colunit-small_molecule[*]": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="D-MTD-COLUNIT_SML-0010",
                    required_properties=["column_name", "param"],
                ),
                FieldRequirement(
                    code="D-MTD-COLUNIT_SML-0020",
                    value_constraint=StringConstraint(
                        json_path=".column_name",
                        minimum=1,
                        null_values=DEFAULT_NULL_VALUES,
                    ),
                ),
                FieldRequirement(
                    code="D-MTD-COLUNIT_SML-0030",
                    value_constraint=CVTermConstraint(
                        json_path=".param", allow_user_defined_terms=True
                    ),
                ),
            ]
        ),
        "$.metadata.colunit-small_molecule_feature[*]": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="D-MTD-COLUNIT_SMF-0010",
                    required_properties=["column_name", "param"],
                ),
                FieldRequirement(
                    code="D-MTD-COLUNIT_SMF-0020",
                    value_constraint=StringConstraint(
                        json_path=".column_name",
                        minimum=1,
                        null_values=DEFAULT_NULL_VALUES,
                    ),
                ),
                FieldRequirement(
                    code="D-MTD-COLUNIT_SMF-0030",
                    value_constraint=CVTermConstraint(
                        json_path=".param", allow_user_defined_terms=True
                    ),
                ),
            ]
        ),
        "$.metadata.colunit-small_molecule_evidence[*]": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="D-MTD-COLUNIT_SME-0010",
                    required_properties=["column_name", "param"],
                ),
                FieldRequirement(
                    code="D-MTD-COLUNIT_SME-0020",
                    value_constraint=StringConstraint(
                        json_path=".column_name",
                        minimum=1,
                        null_values=DEFAULT_NULL_VALUES,
                    ),
                ),
                FieldRequirement(
                    code="D-MTD-COLUNIT_SME-0030",
                    value_constraint=CVTermConstraint(
                        json_path=".param", allow_user_defined_terms=True
                    ),
                ),
            ]
        ),
        "$.smallMoleculeSummary": FieldRequirement(
            code="D-SML-0001",
            enforcement_level="recommended",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.smallMoleculeSummary[*]": FieldRequirement(
            code="D-SML-0010",
            required_properties=[
                "prefix",
                "header_prefix",
                "sml_id",
                "smf_id_refs",
                "database_identifier",
                "chemical_formula",
                "smiles",
                "inchi",
                "chemical_name",
                "uri",
                "theoretical_neutral_mass",
                "adduct_ions",
                "reliability",
                "best_id_confidence_measure",
                "best_id_confidence_value",
            ],
        ),
        "$.smallMoleculeSummary[*].prefix": FieldRequirement(
            code="D-SML-PREFIX-0001",
            value_constraint=RegexConstraint(pattern=r"^SML$"),
        ),
        "$.smallMoleculeSummary[*].header_prefix": FieldRequirement(
            code="D-SML-HEADER_PREFIX-0001",
            value_constraint=RegexConstraint(pattern=r"^SMH$"),
        ),
        "$.smallMoleculeSummary[*].sml_id": FieldRequirement(
            code="D-SML-SML_ID-0001",
            enforcement_level="required",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.smallMoleculeSummary[*].smf_id_refs[*]": FieldRequirement(
            code="D-SML-SMF_ID_REFS-0010",
            enforcement_level="required",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.smallMoleculeSummary[*].database_identifier[*]": FieldRequirement(
            code="D-SML-DATABASE_IDENTIFIER-0010",
            value_constraint=NotNullConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.smallMoleculeSummary[*].chemical_formula[*]": FieldRequirement(
            code="D-SML-CHEMICAL_FORMULA-0010",
            value_constraint=NotNullConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.smallMoleculeSummary[*].smiles[*]": FieldRequirement(
            code="D-SML-SMILES-0010",
            value_constraint=NotNullConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.smallMoleculeSummary[*].inchi[*]": FieldRequirement(
            code="D-SML-INCHI-0010",
            value_constraint=NotNullConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.smallMoleculeSummary[*].chemical_name[*]": FieldRequirement(
            code="D-SML-CHEMICAL_NAME-0010",
            value_constraint=NotNullConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.smallMoleculeSummary[*].uri[*]": FieldRequirement(
            code="D-SML-URI-0010",
            value_constraint=UriConstraint(
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeSummary[*].theoretical_neutral_mass[*]": FieldRequirement(
            code="D-SML-THEORETICAL_NEUTRAL_MASS-0010",
            value_constraint=DecimalConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeSummary[*].adduct_ions[*]": FieldRequirement(
            code="D-SML-ADDUCT_IONS-0010",
            value_constraint=RegexConstraint(
                pattern=r"^\[\d*M([+-][\w\d]+)*\]\d*[+-]$"
            ),
        ),
        "$.smallMoleculeSummary[*].best_id_confidence_measure": FieldRequirement(
            code="D-SML-BEST_ID_CONFIDENCE_MEASURE-0001",
            value_constraint=CVTermConstraint(
                allow_user_defined_terms=True,
                exceptional_values=[None],
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeSummary[*].best_id_confidence_value": FieldRequirement(
            code="D-SML-BEST_ID_CONFIDENCE_VALUE-0001",
            enforcement_level="recommended",
            value_constraint=DecimalConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.smallMoleculeSummary[*].abundance_assay[*]": FieldRequirement(
            code="D-SML-ABUNDANCE_ASSAY-0010",
            value_constraint=DecimalConstraint(
                exceptional_values=[None],
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeSummary[*].abundance_study_variable[*]": FieldRequirement(
            code="D-SML-ABUNDANCE_STUDY_VARIABLE-0010",
            value_constraint=DecimalConstraint(
                exceptional_values=[None],
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeSummary[*]."
        "abundance_variation_study_variable[*]": FieldRequirement(
            code="D-SML-ABUNDANCE_VARIATION_STUDY_VARIABLE-0010",
            value_constraint=DecimalConstraint(
                exceptional_values=[None],
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeSummary[*].opt[*]": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="D-SML-OPT-0010",
                    enforcement_level="required",
                    recommended_properties=["identifier", "param"],
                ),
                FieldRequirement(
                    code="D-SML-OPT-0020",
                    value_constraint=RegexConstraint(
                        json_path=".identifier",
                        pattern=r"^global|ms_run\[\d+\]|assay\[\d+\]|study_variable\[\d+\]$",
                    ),
                ),
                FieldRequirement(
                    code="D-SML-OPT-0030",
                    value_constraint=CVTermConstraint(
                        json_path=".param",
                        null_values=DEFAULT_NULL_VALUES,
                        allow_user_defined_terms=True,
                    ),
                ),
            ]
        ),
        "$.smallMoleculeFeature": FieldRequirement(
            code="D-SMF-0001",
            enforcement_level="recommended",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.smallMoleculeFeature[*]": FieldRequirement(
            code="D-SMF-0010",
            required_properties=[
                "prefix",
                "header_prefix",
                "smf_id",
                "sme_id_refs",
                "sme_id_ref_ambiguity_code",
                "adduct_ion",
                "isotopomer",
                "exp_mass_to_charge",
                "charge",
                "retention_time_in_seconds",
                "retention_time_in_seconds_start",
                "retention_time_in_seconds_end",
            ],
        ),
        "$.smallMoleculeFeature[*].prefix": FieldRequirement(
            code="D-SMF-PREFIX-0001",
            value_constraint=RegexConstraint(pattern=r"^SMF$"),
        ),
        "$.smallMoleculeFeature[*].header_prefix": FieldRequirement(
            code="D-SMF-HEADER_PREFIX-0001",
            value_constraint=RegexConstraint(pattern=r"^SFH$"),
        ),
        "$.smallMoleculeFeature[*].smf_id": FieldRequirement(
            code="D-SMF-SMF_ID-0001",
            enforcement_level="required",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.smallMoleculeFeature[*].sme_id_refs[*]": FieldRequirement(
            code="D-SMF-SME_ID_REFS-0010",
            enforcement_level="required",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.smallMoleculeFeature[*].sme_id_ref_ambiguity_code": FieldRequirement(
            code="D-SMF-SME_ID_REF_AMBIGUITY_CODE-0001",
            enforcement_level="required",
            value_constraint=IntegerEnumConstraint(
                options={
                    1: "Ambiguous identification",
                    2: "Only different evidence streams for the same molecule "
                    "with no ambiguity",
                    3: "Both ambiguous identification and multiple evidence streams",
                },
                exceptional_values=[None],
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeFeature[*].adduct_ion": FieldRequirement(
            code="D-SMF-ADDUCT_ION-0001",
            value_constraint=RegexConstraint(
                pattern=r"^\[\d*M([+-][\w\d]+)*\]\d*[+-]$",
                exceptional_values=[None],
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeFeature[*].isotopomer": FieldRequirement(
            code="D-SMF-ISOTOPOMER-0001",
            value_constraint=CVTermConstraint(
                allow_user_defined_terms=True,
                exceptional_values=[None],
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeFeature[*].exp_mass_to_charge": FieldRequirement(
            code="D-SMF-EXP_MASS_TO_CHARGE-0001",
            value_constraint=DecimalConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.smallMoleculeFeature[*].charge": FieldRequirement(
            code="D-SMF-CHARGE-0001",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.smallMoleculeFeature[*].retention_time_in_seconds": FieldRequirement(
            code="D-SMF-RETENTION_TIME_IN_SECONDS-0001",
            value_constraint=DecimalConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeFeature[*].retention_time_in_seconds_start": FieldRequirement(
            code="D-SMF-RETENTION_TIME_IN_SECONDS_START-0001",
            value_constraint=DecimalConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeFeature[*].retention_time_in_seconds_end": FieldRequirement(
            code="D-SMF-RETENTION_TIME_IN_SECONDS_END-0001",
            value_constraint=DecimalConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeFeature[*].abundance_assay[*]": FieldRequirement(
            code="D-SMF-ABUNDANCE_ASSAY-0010",
            value_constraint=DecimalConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeFeature[*].opt[*]": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="D-SMF-OPT-0010",
                    enforcement_level="required",
                    recommended_properties=["identifier", "param"],
                ),
                FieldRequirement(
                    code="D-SMF-OPT-0020",
                    value_constraint=RegexConstraint(
                        json_path=".identifier",
                        pattern=r"^global|ms_run\[\d+\]|assay\[\d+\]|study_variable\[\d+\]$",
                    ),
                ),
                FieldRequirement(
                    code="D-SMF-OPT-0030",
                    value_constraint=CVTermConstraint(
                        json_path=".param",
                        null_values=DEFAULT_NULL_VALUES,
                        allow_user_defined_terms=True,
                    ),
                ),
            ]
        ),
        "$.smallMoleculeEvidence": FieldRequirement(
            code="D-SME-0001",
            enforcement_level="recommended",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.smallMoleculeEvidence[*]": FieldRequirement(
            code="D-SME-0010",
            required_properties=[
                "prefix",
                "header_prefix",
                "sme_id",
                "evidence_input_id",
                "database_identifier",
                "chemical_formula",
                "smiles",
                "inchi",
                "chemical_name",
                "uri",
                "derivatized_form",
                "adduct_ion",
                "exp_mass_to_charge",
                "charge",
                "theoretical_mass_to_charge",
                "spectra_ref",
                "identification_method",
                "ms_level",
                "id_confidence_measure",
                "rank",
            ],
        ),
        "$.smallMoleculeEvidence[*].prefix": FieldRequirement(
            code="D-SME-PREFIX-0001",
            value_constraint=RegexConstraint(pattern=r"^SME$"),
        ),
        "$.smallMoleculeEvidence[*].header_prefix": FieldRequirement(
            code="D-SME-HEADER_PREFIX-0001",
            value_constraint=RegexConstraint(pattern=r"^SEH$"),
        ),
        "$.smallMoleculeEvidence[*].sme_id": FieldRequirement(
            code="D-SME-SME_ID-0001",
            enforcement_level="required",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.smallMoleculeEvidence[*].evidence_input_id": FieldRequirement(
            code="D-SME-EVIDENCE_INPUT_ID-0001",
            enforcement_level="required",
            value_constraint=StringConstraint(
                minimum=1, null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeEvidence[*].database_identifier": FieldRequirement(
            code="D-SME-DATABASE_IDENTIFIER-0001",
            enforcement_level="required",
            value_constraint=RegexConstraint(
                pattern=r"^[0-9a-zA-Z_]+:.+$",
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeEvidence[*].chemical_formula": FieldRequirement(
            code="D-SME-CHEMICAL_FORMULA-0001",
            value_constraint=StringConstraint(
                minimum=1, exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeEvidence[*].smiles": FieldRequirement(
            code="D-SME-SMILES-0001",
            value_constraint=StringConstraint(
                minimum=1, exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeEvidence[*].inchi": FieldRequirement(
            code="D-SME-INCHI-0001",
            value_constraint=StringConstraint(
                minimum=1, exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeEvidence[*].chemical_name": FieldRequirement(
            code="D-SME-CHEMICAL_NAME-0001",
            value_constraint=StringConstraint(
                minimum=1, exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeEvidence[*].uri": FieldRequirement(
            code="D-SME-URI-0001",
            value_constraint=UriConstraint(
                exceptional_values=[None],
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeEvidence[*].derivatized_form": FieldRequirement(
            code="D-SME-DERIVATIZED_FORM-0001",
            value_constraint=CVTermConstraint(
                allow_user_defined_terms=True,
                exceptional_values=[None],
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeEvidence[*].adduct_ion": FieldRequirement(
            code="D-SME-ADDUCT_ION-0001",
            value_constraint=RegexConstraint(
                pattern=r"^\[\d*M([+-][\w\d]+)*\]\d*[+-]$",
                exceptional_values=[None],
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.smallMoleculeEvidence[*].exp_mass_to_charge": FieldRequirement(
            code="D-SME-EXP_MASS_TO_CHARGE-0001",
            value_constraint=DecimalConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.smallMoleculeEvidence[*].charge": FieldRequirement(
            code="D-SME-CHARGE-0001",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.smallMoleculeEvidence[*].theoretical_mass_to_charge": FieldRequirement(
            code="D-SME-THEORETICAL_MASS_TO_CHARGE-0001",
            value_constraint=DecimalConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.smallMoleculeEvidence[*].spectra_ref": FieldRequirement(
            code="D-SME-SPECTRA_REF-0001",
            value_constraint=CollectionConstraint(
                min_occurs=1, null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeEvidence[*].spectra_ref[*]": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="D-SME-SPECTRA_REF-0010",
                    required_properties=["ms_run", "reference"],
                ),
                FieldRequirement(
                    code="D-SME-SPECTRA_REF-0011",
                    value_constraint=PositiveIntegerConstraint(
                        json_path=".ms_run",
                    ),
                ),
                FieldRequirement(
                    code="D-SME-SPECTRA_REF-0012",
                    value_constraint=NotNullConstraint(
                        json_path=".reference", null_values=DEFAULT_NULL_VALUES
                    ),
                ),
            ]
        ),
        "$.smallMoleculeEvidence[*].identification_method": FieldRequirement(
            code="D-SME-IDENTIFICATION_METHOD-0001",
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.smallMoleculeEvidence[*].ms_level": FieldRequirement(
            code="D-SME-MS_LEVEL-0001",
            value_constraint=CVTermEnumConstraint(
                allowed_cv_terms=[
                    BaseCvTerm(
                        cv_label="MS", cv_accession="MS:1000511", name="ms level"
                    )
                ],
                is_cv_term_value_required=True,
            ),
        ),
        "$.smallMoleculeEvidence[*].id_confidence_measure[*]": FieldRequirement(
            code="D-SME-ID_CONFIDENCE_MEASURE-0010",
            value_constraint=DecimalConstraint(
                exceptional_values=[None], null_values=DEFAULT_NULL_VALUES
            ),
        ),
        "$.smallMoleculeEvidence[*].rank": FieldRequirement(
            code="D-SME-RANK-0001",
            value_constraint=PositiveIntegerConstraint(),
        ),
        "$.smallMoleculeEvidence[*].opt[*]": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="D-SME-OPT-0010",
                    enforcement_level="required",
                    recommended_properties=["identifier", "param"],
                ),
                FieldRequirement(
                    code="D-SME-OPT-0020",
                    value_constraint=RegexConstraint(
                        json_path=".identifier",
                        pattern=r"^global|ms_run\[\d+\]|assay\[\d+\]|study_variable\[\d+\]$",
                    ),
                ),
                FieldRequirement(
                    code="D-SME-OPT-0030",
                    value_constraint=CVTermConstraint(
                        json_path=".param",
                        null_values=DEFAULT_NULL_VALUES,
                        allow_user_defined_terms=True,
                    ),
                ),
            ]
        ),
    },
)


if __name__ == "__main__":
    json_schema = JsonProfile.model_json_schema(by_alias=True, mode="serialization")
    with Path("mztab_m_io/resources/profiles/mztabm-profile-2.1.0-M.schema.json").open(
        "w"
    ) as f:
        json.dump(json_schema, f, indent=4)
    with Path("mztab_m_io/resources/profiles/mztabm-default-profile-2.1.0-M.json").open(
        "w"
    ) as f:
        json.dump(DEFAULT_PROFILE.model_dump(exclude_none=True), f, indent=4)
