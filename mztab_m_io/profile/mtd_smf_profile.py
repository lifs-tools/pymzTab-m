from jsonprofile.profile.constraints import (
    CollectionConstraint,
)
from jsonprofile.profile.model import (
    FieldRequirement,
    FieldRequirementGroup,
    JsonProfile,
)

MTD_SMF_PROFILE = JsonProfile(
    id="https://github.com/HUPO-PSI/mzTab-M/tree/main/schema/mztabm-mtd_smf-profile-2.1.0-M.json",
    version="2.1.0-M",
    name="mzTab-M 2.1.0-M File Profile with feature section",
    description="mzTab-M Default Profile  with metadata and feature section",
    requirements={
        "$": FieldRequirementGroup(
            requirements=[
                FieldRequirement(
                    code="MTD_SML-0001",
                    enforcement_level="required",
                    required_properties=["metadata", "smallMoleculeFeature"],
                ),
            ]
        ),
        "$.smallMoleculeSummary": FieldRequirement(
            code="MTD_SML-SML-0001",
            enforcement_level="optional",
            match_is_required=False,
            value_constraint=CollectionConstraint(min_occurs=1),
        ),
        "$.smallMoleculeFeature": FieldRequirement(
            code="MTD_SML-SMF-0001",
            enforcement_level="required",
            match_is_required=True,
        ),
        "$.smallMoleculeEvidence": FieldRequirement(
            code="D-MTD_SML-0001",
            enforcement_level="optional",
            match_is_required=False,
        ),
    },
)
