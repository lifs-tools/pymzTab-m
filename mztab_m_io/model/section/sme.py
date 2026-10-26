from typing import (
    Annotated,
    List,
    Optional,
)

from pydantic import Field

from mztab_m_io.model.common import OptColumnMapping, Parameter, SpectraReference
from mztab_m_io.model.section.base_table_section import BaseTableSection
from mztab_m_io.model.serialization import (
    TableSerialization,
    ValidationPolicy,
)


class SmallMoleculeEvidence(BaseTableSection):
    prefix: Annotated[
        str,
        Field(
            description="The small molecule evidence table row prefix. "
            "SME MUST be used for rows of the small "
            "molecule evidence table.",
            json_schema_extra=TableSerialization(
                ignore=True,
                validation_policy=ValidationPolicy(required=True, pattern=r"SME"),
            ).model_dump(),
        ),
    ] = "SME"
    header_prefix: Annotated[
        str,
        Field(
            description="The small molecule evidence table header prefix. "
            "SEH MUST be used for the small molecule evidence "
            "table header line (the column labels).",
            json_schema_extra=TableSerialization(
                ignore=True,
                validation_policy=ValidationPolicy(required=True, pattern=r"SEH"),
            ).model_dump(),
        ),
    ] = "SEH"
    sme_id: Annotated[
        Optional[int],
        Field(
            validation_alias="SME_ID",
            description="A within file unique identifier for the small "
            "molecule evidence result.",
            examples=[1],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    evidence_input_id: Annotated[
        Optional[str],
        Field(
            description="A within file unique identifier for the input data "
            "used to support this identification e.g. fragment spectrum, "
            "RT and m/z pair, isotope profile that was used "
            "for the identification process, to serve as a grouping mechanism, "
            "whereby multiple rows of results from the same input data "
            "share the same ID. The identifiers may be human readable "
            "but should not be assumed to be interpretable. "
            "For example, if fragmentation spectra have been searched "
            "then the ID may be the spectrum reference, "
            "or for accurate mass search, the ms_run[2]:458.75.",
            examples=["ms_run[1]:mass=278.65;rt=376.5"],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    database_identifier: Annotated[
        Optional[str],
        Field(
            description="The putative identification for the small molecule "
            "sourced from an external database, using the same prefix "
            "specified in database[1-n]-prefix.  "
            "This could include additionally a chemical class or an "
            "identifier to a spectral "
            "library entity, even if its actual identity is unknown.  "
            "For the “no database” case, "
            "'null' must be used. The unprefixed use of 'null' "
            "is prohibited for any other case. "
            "If no putative identification can be reported for a "
            "particular database, "
            "it MUST be reported as the database prefix followed by null.",
            examples=["CID:00027395"],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    chemical_formula: Annotated[
        Optional[str],
        Field(
            description="The chemical formula of the identified compound "
            "e.g. in a database, "
            "assumed to match the theoretical mass to charge (in some cases "
            "this will be the "
            "derivatized form, including adducts and protons).  "
            "This should be specified in Hill notation (EA Hill 1900), "
            "i.e. elements in the order C, H and then alphabetically "
            "all other elements. "
            "Counts of one may be omitted. Elements should be capitalized properly to "
            "avoid confusion (e.g., “CO” vs. “Co”). The chemical formula "
            "reported should "
            "refer to the neutral form. Charge state is reported by the charge field.  "
            "Example N-acetylglucosamine would be encoded by the string “C8H15NO6” ",
            examples=["C17H20N4O2"],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    smiles: Annotated[
        Optional[str],
        Field(
            description="The potential molecule's structure in the "
            "simplified molecular-input "
            "line-entry system (SMILES) for the small molecule.",
            examples=["C1=CC=C(C=C1)CCNC(=O)CCNNC(=O)C2=CC=NC=C2"],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    inchi: Annotated[
        Optional[str],
        Field(
            description="A standard IUPAC International Chemical Identifier (InChI) "
            "for the given substance.",
            examples=[
                "InChI=1S/C17H20N4O2/c22-16(19-12-6-14-4-2-1-3-5-14)9-13-"
                "20-21-17(23)15-7-10-18-11-8-15/h1-5,7-8,10-11,20H,6,9,"
                "12-13H2,(H,19,22)(H,21,23)"
            ],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    chemical_name: Annotated[
        Optional[str],
        Field(
            description="The small molecule's chemical/common name, "
            "or general description "
            "if a chemical name is unavailable.",
            examples=[
                "N-(2-phenylethyl)-3-[2-(pyridine-4-carbonyl)hydrazinyl]propanamide"
            ],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    uri: Annotated[
        Optional[str],
        Field(
            description="A URI pointing to the small molecule's entry in a database "
            "(e.g., the small molecule's HMDB, Chebi or KEGG entry).",
            examples=["http://www.hmdb.ca/metabolites/HMDB00054"],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(value_constraint="any-url"),
            ).model_dump(),
        ),
    ] = None
    derivatized_form: Annotated[
        Optional[Parameter],
        Field(
            description="The derivatized form of the small molecule, if the "
            "identification was based on a specific derivative (e.g. 2 TMS). "
            "This MUST be specified using CV terms (where possible) otherwise “null”.",
            examples=["[CHEBI, CHEBI:51088, trimethylsilyl group, 3]"],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    adduct_ion: Annotated[
        Optional[str],
        Field(
            description="The assumed classification of this molecule’s adduct "
            "ion after detection, following the general style in the 2013 "
            "IUPAC recommendations on terms relating to MS e.g. [M+H]1+, "
            "[M+Na]1+, [M+NH4]1+, [M-H]1-, [M+Cl]1-. If the adduct "
            "classification is ambiguous with regards to identification "
            "evidence it MAY be null.",
            examples=["[M+H]+"],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(
                    pattern=r"^\[\d*M([+-][\w\d]+)*\]\d*[+-]$"
                ),
            ).model_dump(),
        ),
    ] = None
    exp_mass_to_charge: Annotated[
        Optional[float],
        Field(
            "ion. If multiple adduct forms have been combined into a "
            "single identification event/search, then a single value e.g. "
            "for the protonated form SHOULD be reported here.",
            examples=[1234.5],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    charge: Annotated[
        Optional[int],
        Field(
            description="The small molecule evidence's charge value "
            "using positive integers "
            "both for positive and negative polarity modes.",
            examples=[1],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    theoretical_mass_to_charge: Annotated[
        Optional[float],
        Field(
            description="The theoretical mass/charge value for the small molecule or "
            "the database mass/charge value (for a spectral library match).",
            examples=[1234.71],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    spectra_references: Annotated[
        Optional[List[SpectraReference]],
        Field(
            validation_alias="spectra_ref",
            description="Reference to a spectrum in a spectrum file, for example a "
            "fragmentation spectrum "
            "has been used to support the identification. "
            "If a separate spectrum file has been used for fragmentation spectrum, "
            "this MUST be reported in the metadata section as additional ms_runs. "
            "The reference must be in the format ms_run[1-n]:{SPECTRA_REF} "
            "where SPECTRA_REF MUST follow the format defined in 5.2 (including "
            "references to chromatograms "
            "where these are used to inform identification). "
            "Multiple spectra MUST be "
            "referenced using a | "
            "delimited list for the (rare) cases in which search engines "
            "have combined or "
            "aggregated multiple "
            "spectra in advance of the search to make identifications.  "
            "If a fragmentation spectrum has not been used, the value should indicate "
            "the ms_run to which "
            "is identification is mapped e.g. “ms_run[1]”. ",
            examples=[["ms_run[1]:index=5"]],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|",
                validation_policy=ValidationPolicy(required=True, minimum=1),
            ).model_dump(),
        ),
    ] = None
    identification_method: Annotated[
        Optional[Parameter],
        Field(
            description="The search engine or algorithm used for the "
            "identification. This SHOULD be specified using CV terms.",
            examples=["[MS, MS:1001477, SpectraST,]"],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    ms_level: Annotated[
        Optional[Parameter],
        Field(
            description="The MS level of the spectrum used for the identification. "
            "This SHOULD be specified using CV terms.",
            examples=["[MS, MS:1000511, ms level, 2]"],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(required=True),
            ).model_dump(),
        ),
    ] = None
    id_confidence_measure: Annotated[
        Optional[List[Optional[float]]],
        Field(
            description="Any statistical value or score for the identification. "
            "The metadata section reports the type of score used, "
            "as id_confidence_measure[1-n] of type Param.",
            examples=[[0.7]],
            json_schema_extra=TableSerialization(
                multiple_columns=True,
                json_schema_extra=TableSerialization().model_dump(),
            ).model_dump(),
        ),
    ] = None
    rank: Annotated[
        Optional[int],
        Field(
            description="The rank of this identification from this approach "
            "as increasing integers from 1 (best ranked identification). "
            "Ties (equal score) are represented by using the same rank - "
            "defaults to 1 if there is no ranking system used.",
            examples=[1],
            json_schema_extra=TableSerialization(
                validation_policy=ValidationPolicy(
                    required=True, value_constraint="positive-integer"
                ),
            ).model_dump(),
        ),
    ] = None
    opt: Annotated[
        Optional[List[OptColumnMapping]],
        Field(
            description="Additional columns can be added to the end of "
            "the small molecule evidence table. "
            "These column headers MUST start with the prefix “opt_” "
            "followed by the {identifier} of "
            "the object they reference: assay, study variable, MS run or "
            "“global” (if the value relates to "
            "all replicates). Column names MUST only contain the following characters: "
            "'A'-'Z', 'a'-'z', '0'-'9', '_', '-', '[', ']', and ':'. "
            "CV parameter accessions MAY be used for optional columns following "
            "the format: opt_{identifier}_cv_{accession}_{parameter name}. "
            "Spaces within the parameter's name MUST be replaced by '_'. ",
            examples=[
                "opt_assay[1]_my_value=My value",
                "opt_global_another_value=some other value",
            ],
            json_schema_extra=TableSerialization(
                multiple_columns=True,
                column_value_field="value",
                json_schema_extra=TableSerialization().model_dump(),
            ).model_dump(),
        ),
    ] = None
