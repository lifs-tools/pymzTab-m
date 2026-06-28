from typing import (
    Annotated,
    List,
    Optional,
)

from pydantic import Field

from mztab_m_io.model.common import OptColumnMapping, Parameter
from mztab_m_io.model.section.base_table_section import BaseTableSection
from mztab_m_io.model.serialization import (
    TableSerialization,
)


class SmallMoleculeFeature(BaseTableSection):
    """
    The small molecule feature section is table-based, representing individual
    MS regions (generally considered to be the elution profile for all isotopomers
    formed from a single charge state of a molecule), that have been
    measured/quantified. However, for approaches that quantify individual isotopomers.
    e.g. stable isotope labelling/flux studies,
    then each SMF row SHOULD represent a single isotopomer.

    Different adducts or derivatives and different charge states of
    individual molecules should be reported as separate SMF rows.

    The small molecule feature section MUST always come after the Small Molecule Table.
    All table columns MUST be Tab separated. There MUST NOT be any empty cells.
    Missing values MUST be reported using “null”.

    The order of columns MUST follow the order specified below.

    All columns are MANDATORY except for “opt_” columns.
    """

    prefix: Annotated[
        Optional[str],
        Field(
            description="The small molecule feature table row prefix. "
            "SMF MUST be used for rows of the small molecule feature table.",
            json_schema_extra=TableSerialization(ignore=True).model_dump(),
        ),
    ] = "SMF"
    header_prefix: Annotated[
        str,
        Field(
            description="The small molecule feature table header prefix. "
            "SFH MUST be used for the small molecule feature table header line "
            "(the column labels).",
            json_schema_extra=TableSerialization(ignore=True).model_dump(),
        ),
    ] = "SFH"
    smf_id: Annotated[
        Optional[int],
        Field(
            validation_alias="SMF_ID",
            description="A within file unique identifier for the "
            "small molecule feature.",
            examples=[1],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    sme_id_refs: Annotated[
        Optional[List[int]],
        Field(
            validation_alias="SME_ID_REFS",
            description="References to the identification evidence (SME elements) "
            "via referencing SME_ID values. Multiple values MAY be provided as "
            "a | separated list to indicate ambiguity in the identification or "
            "to indicate that different types of data supported the identifiction "
            "(see SME_ID_REF_ambiguity_code). For the case of a consensus approach "
            "where multiple adduct forms are used to infer the SML ID, "
            "different features should just reference the same SME_ID value(s).",
            examples=[[5, 6, 12]],
            json_schema_extra=TableSerialization(
                list_concatenation_str="|"
            ).model_dump(),
        ),
    ] = None
    sme_id_ref_ambiguity_code: Annotated[
        Optional[int],
        Field(
            validation_alias="SME_ID_REF_ambiguity_code",
            description="If multiple values are given under SME_ID_REFS, one "
            "of the following codes MUST be provided. 1=Ambiguous identification; "
            "2=Only different evidence streams for the same molecule with no "
            "ambiguity; 3=Both ambiguous identification and multiple evidence "
            "streams. If there are no or one value under SME_ID_REFs, this "
            "MUST be reported as null.",
            examples=[1],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    adduct_ion: Annotated[
        Optional[str],
        Field(
            description="The assumed classification of this molecule’s adduct ion "
            "after detection, following the general style in the 2013 IUPAC "
            "recommendations on terms relating to MS e.g. [M+H]1+, [M+Na]1+, "
            "[M+NH4]1+, [M-H]1-, [M+Cl]1-. ",
            examples=["[M+H]1+", "[M+2Na]2+"],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    isotopomer: Annotated[
        Optional[Parameter],
        Field(
            description="If de-isotoping has not been performed, then the "
            "isotopomer quantified MUST be reported here e.g. “+1”, “+2”, "
            "“13C peak” using CV terms, otherwise (i.e. for approaches were "
            "SMF rows are de-isotoped features) this MUST be null.",
            examples=["[MS,MS:1002957,”isotopomer MS peak”,”13C peak”]"],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    exp_mass_to_charge: Annotated[
        Optional[float],
        Field(
            description="The experimental mass/charge value for the feature, "
            "by default assumed to be the mean across assays or a representative "
            "value. For approaches that report isotopomers as SMF rows, "
            "then the m/z of the isotopomer MUST be reported here.",
            examples=[1234.5],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    charge: Annotated[
        Optional[int],
        Field(
            description="The feature’s charge value using positive integers "
            "both for positive and negative polarity modes.",
            examples=[1],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    retention_time_in_seconds: Annotated[
        Optional[float],
        Field(
            description="The apex of the feature on the retention time axis, "
            "in a Master or aggregate MS run. Retention time MUST be reported "
            "in seconds. Retention time values for individual MS runs "
            "(i.e. before alignment) MAY be reported as optional columns. "
            "Retention time SHOULD only be null in the case of direct infusion "
            "MS or other techniques where a retention time value is absent or "
            "unknown. Relative retention time or retention time index values "
            "MAY be reported as optional columns, and could be considered for "
            "inclusion in future versions of mzTab as appropriate.",
            examples=[1345.7],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    retention_time_in_seconds_start: Annotated[
        Optional[float],
        Field(
            description="The start time of the feature on the retention time axis, "
            "in a Master or aggregate MS run. Retention time MUST be reported "
            "in seconds. Retention time start and end SHOULD only be null in "
            "the case of direct infusion MS or other techniques where a retention "
            "time value is absent or unknown and MAY be reported in optional columns.",
            examples=[1327.0],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    retention_time_in_seconds_end: Annotated[
        Optional[float],
        Field(
            description="The end time of the feature on the retention time axis, "
            "in a Master or aggregate MS run. Retention time MUST be reported "
            "in seconds. Retention time start and end SHOULD only be null in "
            "the case of direct infusion MS or other techniques where a retention "
            "time value is absent or unknown and MAY be reported in optional columns.",
            examples=[1327.8],
            json_schema_extra=TableSerialization().model_dump(),
        ),
    ] = None
    abundance_assay: Annotated[
        Optional[List[Optional[float]]],
        Field(
            description="The feature’s abundance in every assay described in "
            "the metadata section MUST be reported. Null or zero values "
            "may be reported as appropriate.",
            examples=[[38648.0]],
            json_schema_extra=TableSerialization(
                multiple_columns=True,
            ).model_dump(),
        ),
    ] = None
    opt: Annotated[
        Optional[List[OptColumnMapping]],
        Field(
            description="Additional columns can be added to the end of "
            "the small molecule feature table. These column headers MUST start "
            "with the prefix “opt_” followed by the {identifier} of the object "
            "they reference: assay, study variable, MS run or “global” "
            "(if the value relates to all replicates). "
            "Column names MUST only contain the following characters: "
            "'A'-'Z', 'a'-'z', '0'-'9', '', '-', '[', ']', and ':'. "
            "CV parameter accessions MAY be used for optional columns "
            "following the format: opt{identifier}_cv_{accession}_parameter name}. "
            "Spaces within the parameter's name MUST be replaced by '_'. ",
            examples=[
                "opt_assay[1]_my_value=My value",
                "opt_global_another_value=some other value",
            ],
            json_schema_extra=TableSerialization(
                multiple_columns=True,
                column_value_field="value",
            ).model_dump(),
        ),
    ] = None
