import json
from pathlib import Path

from jsonprofile.profile.constraints import (
    CollectionConstraint,
    ConstraintGroup,
    CVListConstraint,
    CVTermConstraint,
    EmailConstraint,
    PositiveIntegerConstraint,
    RegexConstraint,
    StringConstraint,
)
from jsonprofile.profile.model import (
    FieldRequirement,
    FieldRequirementGroup,
    JsonProfile,
    JsonProfileConfiguration,
)

from mztab_m_io.profile.default_profile import DEFAULT_NULL_VALUES

METABOLIGHTS_PROFILE = JsonProfile(
    id="https://github.com/HUPO-PSI/mzTab-M/tree/main/schema/mztabm-metabolights-profile-2.1.0-M.json",
    extends="https://github.com/HUPO-PSI/mzTab-M/tree/main/schema/mztabm-default-profile-2.1.0-M.json",
    version="2.1.0-M",
    name="mzTab-M 2.1.0-M Profile for MetaboLights Submissions",
    description="mzTab-M MetaboLights Profile is used "
    " for checking additional requirements of MetaboLights",
    configuration=JsonProfileConfiguration(),
    requirements={
        "$": FieldRequirement(
            code="MTBLS-0001",
            enforcement_level="required",
            required_properties=["metadata", "smallMoleculeSummary"],
        ),
        "$.metadata": FieldRequirement(
            code="MTBLS-METADATA-0001",
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
                "study_variable_group",
                "protocol",
                "sample",
                "contact",
            ],
            recommended_properties=["software", "publication"],
        ),
        "$.metadata.instrument": None,
        "$.metadata.instrument[*]": None,
        "$.metadata.publication": FieldRequirement(
            code="MTBLS-METADATA-PUBLICATION-0001",
            enforcement_level="recommended",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        # "$.metadata.publication[*].publication_items": FieldRequirement(
        #     value_constraint=CollectionConstraint(min_occurs=1, max_occurs=1),
        # ),
        # "$.metadata.publication[*].publication_items[*]": FieldRequirement(
        #     required_properties=["type", "accession"],
        # ),
        # "$.metadata.publication[*].publication_items[*].type": FieldRequirement(
        #     value_constraint=RegexConstraint(pattern=r"^doi$"),
        # ),
        # "$.metadata.publication[*].publication_items[*].accession": FieldRequirement(
        #     value_constraint=RegexConstraint(pattern=r"^10\..+/.+$"),
        # ),
        "$.metadata.contact": FieldRequirement(
            code="MTBLS-METADATA-CONTACT-0001",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.contact[*]": FieldRequirement(
            code="MTBLS-METADATA-CONTACT-0010",
            required_properties=["name", "email", "affiliation"],
            recommended_properties=["orcid"],
        ),
        "$.metadata.contact[*].name": FieldRequirement(
            code="MTBLS-METADATA-CONTACT-0020",
            value_constraint=StringConstraint(minimum=5),
        ),
        "$.metadata.contact[*].email": FieldRequirement(
            code="MTBLS-METADATA-CONTACT-0030",
            value_constraint=EmailConstraint(),
        ),
        "$.metadata.contact[*].affiliation": FieldRequirement(
            code="MTBLS-METADATA-CONTACT-0040",
            value_constraint=StringConstraint(minimum=2),
        ),
        "$.metadata.contact[*].orcid": FieldRequirement(
            code="MTBLS-METADATA-CONTACT-0050",
            enforcement_level="recommended",
            value_constraint=RegexConstraint(
                pattern=r"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[X0-9]$",
                null_values=DEFAULT_NULL_VALUES,
            ),
        ),
        "$.metadata.sample": FieldRequirement(
            code="MTBLS-METADATA-SAMPLE-0001",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.sample[*]": FieldRequirement(
            code="MTBLS-METADATA-SAMPLE-0010",
            enforcement_level="recommended",
            required_properties=["name", "species"],
            recommended_properties=["tissue", "cell_type"],
        ),
        "$.metadata.sample[*].name": FieldRequirement(
            code="MTBLS-METADATA-SAMPLE-0020",
            value_constraint=StringConstraint(minimum=2),
        ),
        "$.metadata.sample[*].species": FieldRequirement(
            code="MTBLS-METADATA-SAMPLE-0030",
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.sample[*].species[*]": FieldRequirement(
            code="MTBLS-METADATA-SAMPLE-0031",
            value_constraint=CVListConstraint(
                allowed_cv_list=["NCBITaxon", "ENVO", "CHEBI"]
            ),
        ),
        "$.metadata.ms_run": FieldRequirement(
            code="MTBLS-METADATA-MS_RUN-0001",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.ms_run[*]": FieldRequirement(
            code="MTBLS-METADATA-MS_RUN-0010",
            required_properties=["location"],
        ),
        "$.metadata.ms_run[*].instrument_ref": None,
        "$.metadata.assay": FieldRequirement(
            code="MTBLS-METADATA-ASSAY-0001",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.assay[*]": FieldRequirement(
            code="MTBLS-METADATA-ASSAY-0010",
            required_properties=["name", "ms_run_ref", "sample_ref"],
        ),
        "$.metadata.assay[*].sample_ref": FieldRequirement(
            code="MTBLS-METADATA-ASSAY-0020",
            value_constraint=PositiveIntegerConstraint(null_values=DEFAULT_NULL_VALUES),
        ),
        "$.metadata.protocol": FieldRequirement(
            code="MTBLS-METADATA-PROTOCOL-0001",
            match_is_required=True,
            value_constraint=CollectionConstraint(
                min_occurs=1,
                item_value_jsonpath_list=["$[*].type.cv_accession"],
                match_reference_values=[
                    "EFO:0005518",
                    "EFO:0000490",
                    "CHMO:0000470",
                    "CHMO:0001000",
                    "OBI:0200000",
                    "MI:2131",
                ],
                min_match=6,
                min_referenced_value_match=6,
            ),
        ),
        "$.metadata.protocol[*]": FieldRequirement(
            code="MTBLS-METADATA-PROTOCOL-0010",
            required_properties=["name", "type"],
        ),
        "$.metadata.protocol[*].name": FieldRequirement(
            code="MTBLS-METADATA-PROTOCOL-0020",
            value_constraint=StringConstraint(min_occurs=2),
        ),
        "$.metadata.protocol[*].type": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="MTBLS-METADATA-PROTOCOL-0030",
                    value_constraint=CVTermConstraint(allow_user_defined_terms=True),
                )
            ],
        ),
        "$.metadata.study_variable_group": FieldRequirement(
            code="MTBLS-METADATA-STUDY_VARIABLE_GROUP-0001",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.study_variable_group[*]": FieldRequirement(
            code="MTBLS-METADATA-STUDY_VARIABLE_GROUP-0010",
            required_properties=["name", "type"],
            recommended_properties=["datatype"],
        ),
        "$.metadata.study_variable_group[*].name": FieldRequirement(
            code="MTBLS-METADATA-STUDY_VARIABLE_GROUP-0020",
            value_constraint=ConstraintGroup(
                constraints=[
                    CVTermConstraint(allow_user_defined_terms=True),
                    StringConstraint(minimum=2),
                ],
                join_operator="or",
            ),
        ),
        "$.metadata.study_variable[*]": FieldRequirement(
            code="MTBLS-METADATA-STUDY_VARIABLE-0010",
            required_properties=["name", "group_refs", "assay_refs"],
        ),
        "$.metadata.study_variable[*].group_refs": FieldRequirement(
            code="MTBLS-METADATA-STUDY_VARIABLE-0020",
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.metadata.study_variable[*].assay_refs": FieldRequirement(
            code="MTBLS-METADATA-STUDY_VARIABLE-0030",
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.smallMoleculeSummary": FieldRequirement(
            code="MTBLS-SML-0001",
            enforcement_level="required",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.smallMoleculeSummary[*].smf_id_refs[*]": None,
    },
)

if __name__ == "__main__":
    file_path = Path(
        "mztab_m_io/resources/profiles/mztabm-metabolights-profile-2.1.0-M.json"
    )

    with file_path.open("w") as f:
        json.dump(METABOLIGHTS_PROFILE.model_dump(exclude_none=True), f, indent=4)
