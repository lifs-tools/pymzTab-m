from typing import (
    Annotated,
    List,
    Optional,
)

from pydantic import Field

from mztab_m_io.model.common import AdductIon, OptColumnMapping, Parameter
from mztab_m_io.model.section.base_table_section import BaseTableSection
from mztab_m_io.model.serialization import TableSerialization, ValidationPolicy


class SmallMoleculeSummary(BaseTableSection):
    prefix: Annotated[
        Optional[str],
        Field(
            description="The small molecule table row prefix. "
            "SML MUST be used for rows of the small molecule table.",
            json_schema_extra=TableSerialization(
                ignore=True,
                validation_policy=ValidationPolicy(required=True, pattern=r"SML"),
            ).model_dump(),
        ),
    ] = "SML"
    header_prefix: Annotated[
        Optional[str],
        Field(
            description="The small molecule table header prefix. "
            "SMH MUST be used for the small molecule table "
            "header line (the column labels).",
            json_schema_extra=TableSerialization(
                ignore=True,
                validation_policy=ValidationPolicy(required=True, pattern=r"SMH"),
            ).model_dump(),
        ),
    ] = "SMH"
    sml_id: Annotated[
        Optional[int],
        Field(
            validation_alias="SML_ID",
            description="A within file unique identifier "
            "for the small molecule summary.",
            examples=[1],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(
                    required=True, value_constraint="non-negative-integer"
                ),
            ).model_dump(),
        ),
    ] = None
    smf_id_refs: Annotated[
        Optional[List[int]],
        Field(
            validation_alias="SMF_ID_REFS",
            description="References to the small molecule features (SMF elements) "
            "via referencing SMF_ID values. Multiple values MAY be provided "
            "as a | separated list to indicate which features were used "
            "to aggregate the SML row.",
            examples=[[2, 3, 11]],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|",
                validation_policy=ValidationPolicy(
                    value_constraint="non-negative-integer"
                ),
            ).model_dump(),
        ),
    ] = None
    database_identifier: Annotated[
        Optional[List[str]],
        Field(
            description="A list of | separated possible identifiers "
            "for the small molecule; multiple values MUST only be provided "
            "to indicate ambiguity in the identification of the molecule "
            "and not to demonstrate different identifier types for the same molecule. "
            "Alternative identifiers for the same molecule MAY be provided "
            "as optional columns. "
            "The database identifier must be preceded "
            "by the resource description (prefix) followed by a colon, "
            "as specified in the metadata section. "
            "A null value MAY be provided if the identification "
            "is sufficiently ambiguous as to be meaningless for reporting or "
            "the small molecule has not been identified.",
            examples=[["CID:00027395"], ["HMDB:HMDB0001847"], ["null"]],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|",
            ).model_dump(),
        ),
    ] = None
    chemical_formula: Annotated[
        Optional[List[str]],
        Field(
            description="The chemical formula of the identified compound e.g. "
            "in a database, assumed to match the theoretical mass to charge "
            "(in some cases this will be the derivatized form, including "
            "adducts and protons). This should be specified in Hill notation "
            "(EA Hill 1900), i.e. elements in the order C, H and then "
            "alphabetically all other elements. Counts of one may be omitted. "
            "Elements should be capitalized properly to avoid confusion "
            "(e.g., “CO” vs. “Co”). The chemical formula reported should "
            "refer to the neutral form. Charge state is reported by the "
            "charge field in the SME and SMF section.\n"
            "Example N-acetylglucosamine would be encoded by the string “C8H15NO6”",
            examples=[["C17H20N4O2"]],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|",
            ).model_dump(),
        ),
    ] = None
    smiles: Annotated[
        Optional[List[str]],
        Field(
            description="The potential molecule’s structure in the simplified "
            "molecular-input line-entry system (SMILES) for the small molecule.",
            examples=[["C1=CC=C(C=C1)CCNC(=O)CCNNC(=O)C2=CC=NC=C2"]],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|",
            ).model_dump(),
        ),
    ] = None
    inchi: Annotated[
        Optional[List[str]],
        Field(
            description="A standard IUPAC International Chemical Identifier "
            "(InChI) for the given substance.",
            examples=[
                [
                    "InChI=1S/C17H20N4O2/c22-16(19-12-6-14-4-2-1-3-5-14)9-13-20-"
                    "21-17(23)15-7-10-18-11-8-15/h1-5,7-8,10-11,20H,6,9,12-13H2,"
                    "(H,19,22)(H,21,23)"
                ]
            ],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|",
            ).model_dump(),
        ),
    ] = None
    chemical_name: Annotated[
        Optional[List[str]],
        Field(
            description="The small molecule’s chemical/common name, or "
            "general description if a chemical name is unavailable.",
            examples=[
                ["N-(2-phenylethyl)-3-[2-(pyridine-4-carbonyl)hydrazinyl]propanamide"]
            ],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|",
            ).model_dump(),
        ),
    ] = None
    uri: Annotated[
        Optional[List[str]],
        Field(
            description="A URI pointing to the small molecule’s entry in a "
            "database (e.g., the small molecule’s HMDB, Chebi or KEGG entry).",
            examples=[
                ["http://www.genome.jp/dbget-bin/www_bget?cpd:C00031"],
                ["http://www.hmdb.ca/metabolites/HMDB0001847"],
                ["http://identifiers.org/hmdb/HMDB0001847"],
            ],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|",
                validation_policy=ValidationPolicy(
                    value_constraint="any-url", minimum=1
                ),
            ).model_dump(),
        ),
    ] = None
    theoretical_neutral_mass: Annotated[
        Optional[List[Optional[float]]],
        Field(
            description="The theoretical neutral mass of the small molecule. "
            "This should be calculated from the chemical formula.",
            examples=[[1234.5]],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|",
            ).model_dump(),
        ),
    ] = None
    adduct_ions: Annotated[
        Optional[List[AdductIon]],
        Field(
            description="A | separated list of the detected adduct ion "
            "forms for this small molecule. The terms should follow the "
            "general style in the 2013 IUPAC recommendations on terms "
            "relating to MS e.g. [M+H]1+, [M+Na]1+, [M+NH4]1+, "
            "[M-H]1-, [M+Cl]1-.",
            examples=[["[M+H]1+", "[M+Na]1+"]],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|",
            ).model_dump(),
        ),
    ] = None
    reliability: Annotated[
        Optional[str],
        Field(
            description="The reliability of the given small molecule identification. "
            "This must be supplied by the resource and should be reported as an "
            "integer between 1-4:\n\n"
            "1: identified, rigorous. ...\n"
            "2: identified. ...\n"
            "3: putatively characterized class. ...\n"
            "4: unknown. ...",
            examples=["3", "0", "2a"],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    best_id_confidence_measure: Annotated[
        Optional[Parameter],
        Field(
            description="The small molecule confidence measure/score of the "
            "best identification for this small molecule summary. The type "
            "of the value is defined by the best_id_confidence_measure CV "
            "parameter. The value is reported in the best_id_confidence_value column.",
            examples=["[MS, MS:1001477, SpectraST,,]"],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    best_id_confidence_value: Annotated[
        Optional[float],
        Field(
            description="The small molecule confidence measure/score value "
            "of the best identification for this small molecule summary.",
            examples=[0.85],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(
                    required=True, enforcement_level="recommended"
                )
            ).model_dump(),
        ),
    ] = None
    abundance_assay: Annotated[
        Optional[List[Optional[float]]],
        Field(
            description="The small molecule’s abundance in every assay "
            "described in the metadata section MUST be reported. "
            "Null or zero values may be reported as appropriate.",
            examples=[[12340.0]],
            json_schema_extra=TableSerialization(
                multiple_columns=True,
            ).model_dump(),
        ),
    ] = None
    abundance_study_variable: Annotated[
        Optional[List[Optional[float]]],
        Field(
            description="The small molecule’s abundance in every study variable "
            "described in the metadata section. Null or zero values "
            "may be reported as appropriate.",
            examples=[[1230.0]],
            json_schema_extra=TableSerialization(
                multiple_columns=True,
            ).model_dump(),
        ),
    ] = None
    abundance_variation_study_variable: Annotated[
        Optional[List[Optional[float]]],
        Field(
            description="The small molecule’s abundance variation in "
            "every study variable described in the metadata section. "
            "Null or zero values may be reported as appropriate.",
            examples=[[0.2]],
            json_schema_extra=TableSerialization(
                multiple_columns=True,
            ).model_dump(),
        ),
    ] = None
    opt: Annotated[
        Optional[List[OptColumnMapping]],
        Field(
            description="Additional columns can be added to "
            "the end of the small molecule table. "
            "These column headers MUST start with the prefix “opt_” followed "
            "by the {identifier} of the object they reference: assay, "
            "study variable, MS run or “global” "
            "(if the value relates to all replicates). "
            "Column names MUST only contain the following characters: "
            "'A'-'Z', 'a'-'z', '0'-'9', '', '-', '[', ']', and ':'. "
            "CV parameter accessions MAY be used for optional columns "
            "following the format: opt{identifier}_cv_{accession}_{parameter name}. "
            "Spaces within the parameter's name MUST be replaced by '_'. ",
            examples=["opt_global_cv_MS:1002217_decoy_peptide=null"],
            json_schema_extra=TableSerialization(
                multiple_columns=True,
                column_value_field="value",
            ).model_dump(),
        ),
    ] = None
