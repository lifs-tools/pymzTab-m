from jsonprofile.profile.constraints import (
    CollectionConstraint,
    CVTermConstraint,
)
from jsonprofile.profile.model import (
    FieldRequirement,
    FieldRequirementGroup,
    JsonProfile,
)

FULL_PROFILE = JsonProfile(
    id="https://github.com/HUPO-PSI/mzTab-M/tree/main/schema/mztabm-full-profile-2.1.0-M.json",
    version="2.1.0-M",
    name="mzTab-M 2.1.0-M Full Profile",
    description="mzTab-M Profile with 4 required sections",
    requirements={
        "$": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="FULL-0001",
                    enforcement_level="required",
                    required_properties=[
                        "metadata",
                        "smallMoleculeSummary",
                        "smallMoleculeFeature",
                        "smallMoleculeEvidence",
                    ],
                ),
            ]
        ),
        "$.metadata.small_molecule-quantification_unit": FieldRequirement(
            code="FULL-MTD-SML_QUANTIFICATION_UNIT-0001",
            match_is_required=True,
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.metadata.small_molecule_feature-quantification_unit": FieldRequirement(
            code="FULL-MTD-SMF_QUANTIFICATION_UNIT-0001",
            match_is_required=True,
            value_constraint=CVTermConstraint(allow_user_defined_terms=True),
        ),
        "$.smallMoleculeSummary": FieldRequirement(
            code="FULL-SML-0001",
            enforcement_level="required",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.smallMoleculeFeature": FieldRequirement(
            code="FULL-SMF-0001",
            enforcement_level="required",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.smallMoleculeEvidence": FieldRequirement(
            code="FULL-SME-0001",
            enforcement_level="required",
            match_is_required=True,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
    },
)
