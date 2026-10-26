# SmallMoleculeFeature

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

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
prefix|<code><code>str</code></code> (<code>SMF</code>)|**required**<br/>pattern: <code>SMF</code><br/>Validation type: **<code>error</code>**|The small molecule feature table row prefix\. SMF MUST be used for rows of the small molecule feature table\.
header_prefix|<code><code>str</code></code> (<code>SFH</code>)|**required**<br/>pattern: <code>SFH</code><br/>Validation type: **<code>error</code>**|The small molecule feature table header prefix\. SFH MUST be used for the small molecule feature table header line \(the column labels\)\.
comment|List of <code>Comment</code>|-|
smf_id<br/>(SMF_ID)|<code>int</code>|**required**<br/>format: <code>non-negative-integer</code><br/>Validation type: **<code>error</code>**|A within file unique identifier for the small molecule feature\.
sme_id_refs<br/>(SME_ID_REFS)|List of <code>int</code>|min: 1<br/>format: <code>non-negative-integer</code><br/>Validation type: **<code>error</code>**|References to the identification evidence \(SME elements\) via referencing SME\_ID values\. Multiple values MAY be provided as a \| separated list to indicate ambiguity in the identification or to indicate that different types of data supported the identifiction \(see SME\_ID\_REF\_ambiguity\_code\)\. For the case of a consensus approach where multiple adduct forms are used to infer the SML ID, different features should just reference the same SME\_ID value\(s\)\.
sme_id_ref_ambiguity_code<br/>(SME_ID_REF_ambiguity_code)|<code>int</code>|min: 1<br/>max: 3<br/>Validation type: **<code>error</code>**|If multiple values are given under SME\_ID\_REFS, one of the following codes MUST be provided\. 1=Ambiguous identification; 2=Only different evidence streams for the same molecule with no ambiguity; 3=Both ambiguous identification and multiple evidence streams\. If there are no or one value under SME\_ID\_REFs, this MUST be reported as null\.
adduct_ion|<code>str</code>|-|The assumed classification of this molecule’s adduct ion after detection, following the general style in the 2013 IUPAC recommendations on terms relating to MS e\.g\. \[M\+H\]1\+, \[M\+Na\]1\+, \[M\+NH4\]1\+, \[M\-H\]1\-, \[M\+Cl\]1\-\.
isotopomer|<code>Parameter</code>|-|If de\-isotoping has not been performed, then the isotopomer quantified MUST be reported here e\.g\. “\+1”, “\+2”, “13C peak” using CV terms, otherwise \(i\.e\. for approaches were SMF rows are de\-isotoped features\) this MUST be null\.
exp_mass_to_charge|<code>float</code>|**required**<br/>Validation type: **<code>error</code>**|The experimental mass/charge value for the feature, by default assumed to be the mean across assays or a representative value\. For approaches that report isotopomers as SMF rows, then the m/z of the isotopomer MUST be reported here\.
charge|<code>int</code>|**required**<br/>Validation type: **<code>error</code>**|The feature’s charge value using positive integers both for positive and negative polarity modes\.
retention_time_in_seconds|<code>float</code>|-|The apex of the feature on the retention time axis, in a Master or aggregate MS run\. Retention time MUST be reported in seconds\. Retention time values for individual MS runs \(i\.e\. before alignment\) MAY be reported as optional columns\. Retention time SHOULD only be null in the case of direct infusion MS or other techniques where a retention time value is absent or unknown\. Relative retention time or retention time index values MAY be reported as optional columns, and could be considered for inclusion in future versions of mzTab as appropriate\.
retention_time_in_seconds_start|<code>float</code>|-|The start time of the feature on the retention time axis, in a Master or aggregate MS run\. Retention time MUST be reported in seconds\. Retention time start and end SHOULD only be null in the case of direct infusion MS or other techniques where a retention time value is absent or unknown and MAY be reported in optional columns\.
retention_time_in_seconds_end|<code>float</code>|-|The end time of the feature on the retention time axis, in a Master or aggregate MS run\. Retention time MUST be reported in seconds\. Retention time start and end SHOULD only be null in the case of direct infusion MS or other techniques where a retention time value is absent or unknown and MAY be reported in optional columns\.
abundance_assay|List of <code>float</code>|-|The feature’s abundance in every assay described in the metadata section MUST be reported\. Null or zero values may be reported as appropriate\.
opt|List of <code>OptColumnMapping</code>|-|Additional columns can be added to the end of the small molecule feature table\. These column headers MUST start with the prefix “opt\_” followed by the \{identifier\} of the object they reference: assay, study variable, MS run or “global” \(if the value relates to all replicates\)\. Column names MUST only contain the following characters: 'A'\-'Z', 'a'\-'z', '0'\-'9', '', '\-', '\[', '\]', and ':'\. CV parameter accessions MAY be used for optional columns following the format: opt\{identifier\}\_cv\_\{accession\}\_parameter name\}\. Spaces within the parameter's name MUST be replaced by '\_'\.
