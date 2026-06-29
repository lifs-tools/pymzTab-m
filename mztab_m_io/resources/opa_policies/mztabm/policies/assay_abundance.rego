package mztabm.policies

import data.mztabm.utils as utils
import rego.v1

# METADATA
# title: Validate assay abundance columns
# description: Verifies that smallMoleculeSummary and smallMoleculeEvidence rows define the same number of abundance_assay values as assays declared in metadata.
# custom:
#  policy_id: policy_000_0001
policy_D_0010 contains result if {

    assays_count := count(utils.get_normalized_object_array(input.root.metadata, "assay"),)
    tables := {
        "smallMoleculeSummary": utils.get_normalized_object_array(input.root, "smallMoleculeSummary"),
        "smallMoleculeFeature": utils.get_normalized_object_array(input.root, "smallMoleculeFeature"),
    }

    violations := [msg |
        some name, table in tables
        count(table) > 0
        item := table[0]
        referenced := count(utils.get_normalized_object_array(item, "abundance_assay"))
        referenced != assays_count
        msg := sprintf(
            "Number of assays in metadata section: %v, number of abundance_assay columns in %v: %v",
            [assays_count, name, referenced],
        )
    ]
    result := {
        "evaluation": count(violations) == 0,
        "message": concat(", ", violations),
    }
}
