from pathlib import Path

from mztab_m_io.model.common import (
    CV,
    Assay,
    ColumnParameterMapping,
    Contact,
    Database,
    Instrument,
    MsRun,
    OptColumnMapping,
    Parameter,
    Publication,
    PublicationItem,
    Sample,
    SampleProcessing,
    Software,
    SpectraReference,
    StudyVariable,
    Uri,
)
from mztab_m_io.model.mztabm import MzTabM
from mztab_m_io.model.section.mtd import Metadata
from mztab_m_io.model.section.sme import SmallMoleculeEvidence
from mztab_m_io.model.section.smf import SmallMoleculeFeature
from mztab_m_io.model.section.sml import SmallMoleculeSummary


def create_full_mztabm():
    # 1. Metadata
    mtd = Metadata(
        mztab_version="2.0.0-M",
        mztab_id="Height_0_20201291324.mzTab",
        title="Metabolomics Study Example",
        description="Example metabolomics study from MS-DIAL export",
        cv=[
            CV(
                label="MS",
                full_name="PSI Mass Spectrometry Ontology",
                version="4.1.0",
                uri="https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo",
            ),
            CV(
                label="UO",
                full_name="Unit Ontology",
                version="14:07:2021",
                uri="https://raw.githubusercontent.com/bio-ontology-research-group/unit-ontology/master/unit.obo",
            ),
            CV(
                label="NCIT",
                full_name="NCI Thesaurus",
                version="20.10d",
                uri="https://raw.githubusercontent.com/NCI-Thesaurus/thesaurus-obo-edition/master/ncit.obo",
            ),
        ],
        database=[
            Database(
                id=1,
                prefix="MSP",
                uri="file://Z:/GCMS_DB.msp",
                version="Unknown",
                param=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1001013",
                    name="database name",
                    value="User-defined MSP library file",
                ),
            ),
            Database(
                id=2,
                prefix="HMDB",
                uri="http://www.hmdb.ca/",
                version="4.0",
                param=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1001013",
                    name="database name",
                    value="HMDB",
                ),
            ),
            Database(
                id=3,
                prefix="KEGG",
                uri="http://www.kegg.jp/",
                version="88.0",
                param=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1001013",
                    name="database name",
                    value="KEGG",
                ),
            ),
        ],
        software=[
            Software(
                id=1,
                parameter=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1003082",
                    name="MS-DIAL",
                    value="4.12",
                ),
            ),
            Software(
                id=2,
                parameter=Parameter(name="MS-DIAL mzTab exporter", value="1.05"),
                setting=["setting1", "setting2"],
            ),
            Software(
                id=3,
                parameter=Parameter(name="Python Script", value="1.0.0"),
                setting=["setting3"],
            ),
        ],
        instrument=[
            Instrument(
                id=1,
                name=Parameter(name="Thermo Fisher Q Exactive HF"),
                source=Parameter(cv_label="MS", cv_accession="MS:1000073", name="ESI"),
                analyzer=[
                    Parameter(cv_label="MS", cv_accession="MS:1000084", name="TOF")
                ],
                detector=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1000114",
                    name="Microchannel plate detector",
                ),
            ),
            Instrument(
                id=2,
                name=Parameter(name="Agilent 6550 iFunnel Q-TOF"),
                source=Parameter(cv_label="MS", cv_accession="MS:1000073", name="ESI"),
                analyzer=[
                    Parameter(cv_label="MS", cv_accession="MS:1000084", name="TOF")
                ],
                detector=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1000114",
                    name="Microchannel plate detector",
                ),
            ),
            Instrument(
                id=3,
                name=Parameter(name="Bruker impact II"),
                source=Parameter(cv_label="MS", cv_accession="MS:1000073", name="ESI"),
                analyzer=[
                    Parameter(cv_label="MS", cv_accession="MS:1000084", name="TOF"),
                    Parameter(cv_label="MS", cv_accession="MS:1000084", name="TOF"),
                ],
                detector=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1000114",
                    name="Microchannel plate detector",
                ),
            ),
        ],
        ms_run=[
            MsRun(
                id=1,
                name="run1",
                location="file://Z:/data/Cont13_1.abf",
                instrument_ref=1,
                format=Parameter(
                    cv_label="MS", cv_accession="MS:1001062", name="Mascot MGF file"
                ),
                id_format=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1001530",
                    name="mzML unique identifier",
                ),
                fragmentation_method=[
                    Parameter(cv_label="MS", cv_accession="MS:1000133", name="CID")
                ],
                scan_polarity=[
                    Parameter(
                        cv_label="MS", cv_accession="MS:1000130", name="positive scan"
                    )
                ],
                hash="de9f2c7fd25e1b3afad3e85a0bd17d9b100db4b3",
                hash_method=Parameter(
                    cv_label="MS", cv_accession="MS:1000569", name="SHA-1"
                ),
            ),
            MsRun(
                id=2,
                name="run2",
                location="file://Z:/data/Cont14_1.abf",
                instrument_ref=2,
                format=Parameter(
                    cv_label="MS", cv_accession="MS:1001062", name="Mascot MGF file"
                ),
                id_format=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1001530",
                    name="mzML unique identifier",
                ),
                fragmentation_method=[
                    Parameter(cv_label="MS", cv_accession="MS:1000133", name="CID")
                ],
                scan_polarity=[
                    Parameter(
                        cv_label="MS", cv_accession="MS:1000130", name="positive scan"
                    )
                ],
                hash="de9f2c7fd25e1b3afad3e85a0bd17d9b100db4b3",
                hash_method=Parameter(
                    cv_label="MS", cv_accession="MS:1000569", name="SHA-1"
                ),
            ),
            MsRun(
                id=3,
                name="run3",
                location="file://Z:/data/Cont16_1.abf",
                instrument_ref=3,
                format=Parameter(
                    cv_label="MS", cv_accession="MS:1001062", name="Mascot MGF file"
                ),
                id_format=Parameter(
                    cv_label="MS",
                    cv_accession="MS:1001530",
                    name="mzML unique identifier",
                ),
                fragmentation_method=[
                    Parameter(cv_label="MS", cv_accession="MS:1000133", name="CID")
                ],
                scan_polarity=[
                    Parameter(
                        id=1,
                        cv_label="MS",
                        cv_accession="MS:1000130",
                        name="positive scan",
                    )
                ],
                hash="de9f2c7fd25e1b3afad3e85a0bd17d9b100db4b3",
                hash_method=Parameter(
                    cv_label="MS", cv_accession="MS:1000569", name="SHA-1"
                ),
            ),
        ],
        sample=[
            Sample(
                name="Sample 1",
                description="Control sample 1",
                species=[
                    Parameter(
                        id=1,
                        cv_label="NCIT",
                        cv_accession="NCIT:C14175",
                        name="Homo sapiens",
                    )
                ],
                tissue=[
                    Parameter(
                        id=1,
                        cv_label="BTO",
                        cv_accession="BTO:0000131",
                        name="blood plasma",
                    )
                ],
                cell_type=[
                    Parameter(
                        id=1, cv_label="CL", cv_accession="CL:0000000", name="cell"
                    )
                ],
                disease=[
                    Parameter(
                        id=1, cv_label="DOID", cv_accession="DOID:4", name="disease"
                    )
                ],
                custom=[
                    Parameter(
                        id=1,
                        cv_label="MS",
                        cv_accession="MS:1000000",
                        name="custom param",
                    )
                ],
            ),
            Sample(
                id=2,
                name="Sample 2",
                description="Control sample 2",
                species=[
                    Parameter(
                        id=1,
                        cv_label="NCIT",
                        cv_accession="NCIT:C14175",
                        name="Homo sapiens",
                    )
                ],
                tissue=[
                    Parameter(
                        id=1,
                        cv_label="BTO",
                        cv_accession="BTO:0000131",
                        name="blood plasma",
                    )
                ],
                cell_type=[
                    Parameter(
                        id=1, cv_label="CL", cv_accession="CL:0000000", name="cell"
                    )
                ],
                disease=[
                    Parameter(
                        id=1, cv_label="DOID", cv_accession="DOID:4", name="disease"
                    )
                ],
                custom=[
                    Parameter(
                        id=1,
                        cv_label="MS",
                        cv_accession="MS:1000000",
                        name="custom param",
                    )
                ],
            ),
            Sample(
                id=3,
                name="Sample 3",
                description="Control sample 3",
                species=[
                    Parameter(
                        cv_label="NCIT", cv_accession="NCIT:C14175", name="Homo sapiens"
                    )
                ],
                tissue=[
                    Parameter(
                        cv_label="BTO", cv_accession="BTO:0000131", name="blood plasma"
                    )
                ],
                cell_type=[
                    Parameter(cv_label="CL", cv_accession="CL:0000000", name="cell")
                ],
                disease=[
                    Parameter(cv_label="DOID", cv_accession="DOID:4", name="disease")
                ],
                custom=[
                    Parameter(
                        cv_label="MS", cv_accession="MS:1000000", name="custom param"
                    )
                ],
            ),
        ],
        assay=[
            Assay(
                name="Cont13_1",
                ms_run_refs=[1],
                sample_ref=1,
                external_uri="http://example.com/assay1",
                custom=[
                    Parameter(
                        cv_label="MS", cv_accession="MS:1000000", name="custom param"
                    )
                ],
            ),
            Assay(
                name="Cont14_1",
                ms_run_refs=[2],
                sample_ref=2,
                external_uri="http://example.com/assay2",
                custom=[
                    Parameter(
                        cv_label="MS", cv_accession="MS:1000000", name="custom param"
                    )
                ],
            ),
            Assay(
                name="Cont16_1",
                ms_run_refs=[3],
                sample_ref=3,
                external_uri="http://example.com/assay3",
                custom=[
                    Parameter(
                        cv_label="MS", cv_accession="MS:1000000", name="custom param"
                    )
                ],
            ),
        ],
        study_variable=[
            StudyVariable(
                name="cont", description="Control group", assay_refs=[1, 2, 3]
            ),
            StudyVariable(
                name="treated", description="Treated group", assay_refs=[]
            ),  # Example with no assays
            StudyVariable(
                name="blank", description="Blank samples", assay_refs=[]
            ),  # Example with no assays
        ],
        contact=[
            Contact(
                name="John Doe",
                affiliation="University of Example",
                email="john.doe@example2.com",
            ),
            Contact(
                name="Jane Smith",
                affiliation="Institute of Science",
                email="jane.smith@example2.com",
            ),
            Contact(
                name="Bob Johnson",
                affiliation="Research Lab",
                email="bob.johnson@example2.com",
            ),
        ],
        publication=[
            Publication(
                publication_items=[
                    PublicationItem(type="doi", cv_accession="10.1000/182")
                ]
            ),
            Publication(
                publication_items=[
                    PublicationItem(type="pubmed", cv_accession="21345678")
                ]
            ),
            Publication(
                publication_items=[
                    PublicationItem(type="doi", cv_accession="10.1000/183")
                ]
            ),
        ],
        quantification_method=Parameter(name="Label-free raw feature quantitation"),
        small_molecule_quantification_unit=Parameter(
            name="precursor intensity (peak height)"
        ),
        small_molecule_feature_quantification_unit=Parameter(
            name="precursor intensity (peak height)"
        ),
        small_molecule_identification_reliability=Parameter(
            cv_label="MS",
            cv_accession="MS:1003032",
            name="compound identification confidence code in MS-DIAL",
        ),
        id_confidence_measure=[
            Parameter(name="MS-DIAL algorithm matching score"),
            Parameter(name="Retention time similarity"),
            Parameter(name="Dot product"),
        ],
        colunit_small_molecule=[
            ColumnParameterMapping(
                column_name="retention_time",
                param=Parameter(
                    cv_label="UO", cv_accession="UO:0000031", name="minute"
                ),
            ),
            ColumnParameterMapping(
                column_name="exp_mass_to_charge",
                param=Parameter(
                    cv_label="UO", cv_accession="UO:0000221", name="dalton"
                ),
            ),
            ColumnParameterMapping(
                column_name="opt_assay[2]_other_attribute",
                param=Parameter(
                    cv_label="UO", cv_accession="UO:0000186", name="dimensionless unit"
                ),
            ),
        ],
        colunit_small_molecule_feature=[
            ColumnParameterMapping(
                column_name="retention_time",
                param=Parameter(
                    cv_label="UO", cv_accession="UO:0000031", name="minute"
                ),
            ),
            ColumnParameterMapping(
                column_name="exp_mass_to_charge",
                param=Parameter(
                    cv_label="UO", cv_accession="UO:0000221", name="dalton"
                ),
            ),
            ColumnParameterMapping(
                column_name="opt_assay[2]_other_attribute",
                param=Parameter(
                    cv_label="UO", cv_accession="UO:0000186", name="dimensionless unit"
                ),
            ),
        ],
        colunit_small_molecule_evidence=[
            ColumnParameterMapping(
                column_name="retention_time",
                param=Parameter(
                    cv_label="UO", cv_accession="UO:0000031", name="minute"
                ),
            ),
            ColumnParameterMapping(
                column_name="exp_mass_to_charge",
                param=Parameter(
                    cv_label="UO", cv_accession="UO:0000221", name="dalton"
                ),
            ),
        ],
        uri=[Uri(value="http://www.ebi.ac.uk/metabolights/MTBLS1")],
        external_study_uri=[Uri(value="http://www.ebi.ac.uk/metabolights/MTBLS1")],
        custom=[
            Parameter(
                cv_label="MS",
                cv_accession="MS:1000000",
                name="custom param",
                value="custom value",
            )
        ],
        sample_processing=[
            SampleProcessing(
                sample_processing=[
                    Parameter(
                        cv_label="SEP", cv_accession="SEP:00142", name="extraction"
                    ),
                    Parameter(
                        cv_label="SEP", cv_accession="SEP:00210", name="centrifugation"
                    ),
                ]
            ),
            SampleProcessing(
                sample_processing=[
                    Parameter(
                        cv_label="MS", cv_accession="MS:1000085", name="silylation"
                    )
                ]
            ),
        ],
        derivatization_agent=[
            Parameter(cv_label="MS", cv_accession="MS:1000085", name="silylation")
        ],
    )

    # 2. Small Molecule Evidence (SME)
    sme = [
        SmallMoleculeEvidence(
            sme_id=1,
            evidence_input_id="ms_run[1]:440",
            database_identifier="MSP: Glycolic acid; GC-EI-TOF; MS; 2 TMS; BP",
            chemical_formula="C2H4O3",
            smiles="OCC(O)=O",
            inchi="InChI=1S/C2H4O3/c3-1-2(4)5/h3H,1H2,(H,4,5)",
            chemical_name="Glycolic acid; GC-EI-TOF; MS; 2 TMS; BP",
            uri="http://example.com/glycolic_acid",
            adduct_ion="[M]1+",
            exp_mass_to_charge=76.016,
            charge=1,
            theoretical_mass_to_charge=76.016,
            spectra_references=[SpectraReference(ms_run_ref=1, reference="scan=1")],
            identification_method=Parameter(name="MS-DIAL"),
            ms_level=Parameter(
                cv_label="MS", cv_accession="MS:1000511", name="ms level", value="1"
            ),
            id_confidence_measure=[82.9, 90.0, 95.5],
            rank=1,
        ),
        SmallMoleculeEvidence(
            sme_id=2,
            evidence_input_id="ms_run[1]:441",
            database_identifier="MSP: L-Alanine; GC-EI-TOF; MS; 3 TMS; BP",
            chemical_formula="C3H7NO2",
            smiles="CC(N)C(O)=O",
            inchi="InChI=1S/C3H7NO2/c1-2(4)3(5)6/h2H,4H2,1H3,(H,5,6)/t2-/m0/s1",
            chemical_name="L-Alanine; GC-EI-TOF; MS; 3 TMS; BP",
            uri="http://example.com/alanine",
            adduct_ion="[M]1+",
            exp_mass_to_charge=89.047,
            charge=1,
            theoretical_mass_to_charge=89.047,
            spectra_references=[SpectraReference(ms_run_ref=1, reference="scan=1")],
            identification_method=Parameter(name="MS-DIAL"),
            ms_level=Parameter(
                cv_label="MS", cv_accession="MS:1000511", name="ms level", value="1"
            ),
            id_confidence_measure=[97.1, 95.0, 98.0],
            rank=1,
        ),
        SmallMoleculeEvidence(
            sme_id=3,
            evidence_input_id="ms_run[1]:442",
            database_identifier="MSP: Glycine; GC-EI-TOF; MS; 3 TMS; BP",
            chemical_formula="C2H5NO2",
            smiles="NCC(O)=O",
            inchi="InChI=1S/C2H5NO2/c3-1-2(4)5/h1,3H2,(H,4,5)",
            chemical_name="Glycine; GC-EI-TOF; MS; 3 TMS; BP",
            uri="http://example.com/glycine",
            adduct_ion="[M]1+",
            exp_mass_to_charge=75.032,
            charge=1,
            theoretical_mass_to_charge=75.032,
            spectra_references=[SpectraReference(ms_run_ref=1, reference="scan=1")],
            identification_method=Parameter(name="MS-DIAL"),
            ms_level=Parameter(
                cv_label="MS", cv_accession="MS:1000511", name="ms level", value="1"
            ),
            id_confidence_measure=[92.6, 90.0, 94.0],
            rank=1,
        ),
    ]

    # 3. Small Molecule Feature (SMF)
    smf = [
        SmallMoleculeFeature(
            smf_id=1,
            sme_id_refs=[1],
            adduct_ion="[M]1+",
            exp_mass_to_charge=76.016,
            charge=1,
            retention_time_in_seconds=240.586,
            retention_time_in_seconds_start=240.3705,
            retention_time_in_seconds_end=240.8015,
            abundance_assay=[3039.111, 2944.111, 4589.333],
            sme_id_ref_ambiguity_code=None,
            isotopomer=Parameter(
                cv_label="MS", cv_accession="MS:1000000", name="isotopomer 1"
            ),
            opt=[
                OptColumnMapping(
                    identifier="global_cv_MS:1002217_decoy_peptide",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1002217", name="decoy_peptide"
                    ),
                    value="0",
                ),
                OptColumnMapping(
                    identifier="assay[2]_other_attribute",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1000000", name="other attribute"
                    ),
                    value="some value",
                ),
            ],
        ),
        SmallMoleculeFeature(
            smf_id=2,
            sme_id_refs=[2],
            adduct_ion="[M]1+",
            exp_mass_to_charge=89.047,
            charge=1,
            retention_time_in_seconds=241.7475,
            retention_time_in_seconds_start=240.6023,
            retention_time_in_seconds_end=242.8927,
            abundance_assay=[3529.222, 3671.222, 3765.778],
            sme_id_ref_ambiguity_code=None,
            isotopomer=Parameter(
                cv_label="MS", cv_accession="MS:1000000", name="isotopomer 1"
            ),
            opt=[
                OptColumnMapping(
                    identifier="global_cv_MS:1002217_decoy_peptide",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1002217", name="decoy_peptide"
                    ),
                    value="0",
                ),
                OptColumnMapping(
                    identifier="assay[2]_other_attribute",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1000000", name="other attribute"
                    ),
                    value="some value",
                ),
            ],
        ),
        SmallMoleculeFeature(
            smf_id=3,
            sme_id_refs=[3],
            adduct_ion="[M]1+",
            exp_mass_to_charge=75.032,
            charge=1,
            retention_time_in_seconds=244.0718,
            retention_time_in_seconds_start=243.0842,
            retention_time_in_seconds_end=245.0595,
            abundance_assay=[4232.333, 4626.889, 4731.778],
            sme_id_ref_ambiguity_code=None,
            isotopomer=Parameter(
                cv_label="MS", cv_accession="MS:1000000", name="isotopomer 1"
            ),
            opt=[
                OptColumnMapping(
                    identifier="global_cv_MS:1002217_decoy_peptide",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1002217", name="decoy_peptide"
                    ),
                    value="0",
                ),
                OptColumnMapping(
                    identifier="assay[2]_other_attribute",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1000000", name="other attribute"
                    ),
                    value="some value",
                ),
            ],
        ),
    ]

    # 4. Small Molecule Summary (SML)
    sml = [
        SmallMoleculeSummary(
            sml_id=1,
            smf_id_refs=[1],
            database_identifier=["MSP: Glycolic acid; GC-EI-TOF; MS; 2 TMS; BP"],
            chemical_formula=["C2H4O3"],
            smiles=["OCC(O)=O"],
            inchi=["InChI=1S/C2H4O3/c3-1-2(4)5/h3H,1H2,(H,4,5)"],
            chemical_name=["Glycolic acid; GC-EI-TOF; MS; 2 TMS; BP"],
            uri=["http://example.com/glycolic_acid"],
            theoretical_neutral_mass=[76.016],
            adduct_ions=["[M]1+"],
            reliability="1",
            best_id_confidence_measure=Parameter(
                name="MS-DIAL algorithm matching score"
            ),
            best_id_confidence_value=82.9,
            abundance_assay=[150717.3, 118989.2, 154902.1],
            abundance_study_variable=[141536.21875, 76471.703125, 0.0],
            abundance_variation_study_variable=[19638.06, 8369.48, 0.0],
            opt=[
                OptColumnMapping(
                    identifier="global_cv_MS:1002217_decoy_peptide",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1002217", name="decoy_peptide"
                    ),
                    value="0",
                ),
                OptColumnMapping(
                    identifier="assay[2]_other_attribute",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1000000", name="other attribute"
                    ),
                    value="some value",
                ),
            ],
        ),
        SmallMoleculeSummary(
            sml_id=2,
            smf_id_refs=[2],
            database_identifier=["MSP: L-Alanine; GC-EI-TOF; MS; 3 TMS; BP"],
            chemical_formula=["C3H7NO2"],
            smiles=["CC(N)C(O)=O"],
            inchi=["InChI=1S/C3H7NO2/c1-2(4)3(5)6/h2H,4H2,1H3,(H,5,6)/t2-/m0/s1"],
            chemical_name=["L-Alanine; GC-EI-TOF; MS; 3 TMS; BP"],
            uri=["http://example.com/alanine"],
            theoretical_neutral_mass=[89.047],
            adduct_ions=["[M]1+"],
            reliability="1",
            best_id_confidence_measure=Parameter(
                name="MS-DIAL algorithm matching score"
            ),
            best_id_confidence_value=97.1,
            abundance_assay=[296045.8, 272303.3, 169987.9],
            abundance_study_variable=[246112.338541667, 181112.260416667, 0.0],
            abundance_variation_study_variable=[66986.00, 32578.56, 0.0],
            opt=[
                OptColumnMapping(
                    identifier="global_cv_MS:1002217_decoy_peptide",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1002217", name="decoy_peptide"
                    ),
                    value="0",
                ),
                OptColumnMapping(
                    identifier="assay[2]_other_attribute",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1000000", name="other attribute"
                    ),
                    value="some value",
                ),
            ],
        ),
        SmallMoleculeSummary(
            sml_id=3,
            smf_id_refs=[3],
            database_identifier=["MSP: Glycine; GC-EI-TOF; MS; 3 TMS; BP"],
            chemical_formula=["C2H5NO2"],
            smiles=["NCC(O)=O"],
            inchi=["InChI=1S/C2H5NO2/c3-1-2(4)5/h1,3H2,(H,4,5)"],
            chemical_name=["Glycine; GC-EI-TOF; MS; 3 TMS; BP"],
            uri=["http://example.com/glycine"],
            theoretical_neutral_mass=[75.032],
            adduct_ions=["[M]1+"],
            reliability="1",
            best_id_confidence_measure=Parameter(
                name="MS-DIAL algorithm matching score"
            ),
            best_id_confidence_value=92.6,
            abundance_assay=[289172.3, 232538.9, 265559.4],
            abundance_study_variable=[262423.557291667, 122489.1484375, 0.0],
            abundance_variation_study_variable=[28446.66, 42891.80, 0.0],
            opt=[
                OptColumnMapping(
                    identifier="global_cv_MS:1002217_decoy_peptide",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1002217", name="decoy_peptide"
                    ),
                    value="0",
                ),
                OptColumnMapping(
                    identifier="assay[2]_other_attribute",
                    param=Parameter(
                        cv_label="MS", cv_accession="MS:1000000", name="other attribute"
                    ),
                    value="some value",
                ),
            ],
        ),
    ]

    # Create MzTabM object
    mztabm = MzTabM(
        metadata=mtd,
        small_molecule_summary=sml,
        small_molecule_feature=smf,
        small_molecule_evidence=sme,
    )

    # Validate
    mztabm.validate()

    # Optional: save to file to inspect results
    Path(".temp").mkdir(parents=True, exist_ok=True)
    mztabm.save(".temp/generated_full_example.mztab")

    return mztabm


if __name__ == "__main__":
    create_full_mztabm()
