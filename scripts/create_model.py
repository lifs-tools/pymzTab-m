import logging

from mztab_m_io.model.common import (
    CV,
    Assay,
    Database,
    MsRun,
    Parameter,
    Software,
    StudyVariable,
)
from mztab_m_io.model.mztabm import MzTabM
from mztab_m_io.model.section.mtd import Metadata
from mztab_m_io.model.serialization import SerializationContext

logger = logging.getLogger(__name__)

MTD = Metadata(
    mztab_version="2.0.0-M",
    mztab_id="study id",
    quantification_method=Parameter(
        cv_label="MS",
        cv_accession="MS:1001834",
        name="LC-MS label-free quantitation analysis",
    ),
    software=[Software(id=1, parameter=Parameter(name="inhouse"))],
    ms_run=[MsRun(id=1, location="ftp://ftp.ebi.ac.uk/path/to/file")],
    assay=[Assay(id=1, name="assay 1", ms_run_refs=[1])],
    study_variable=[
        StudyVariable(
            name="study variable 1",
            assay_refs=[1],
        )
    ],
    cv=[
        CV(
            label="MS",
            full_name="Mass Spectrometry Ontology",
            version="4.1.38",
            uri="https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo",
        )
    ],
    small_molecule_quantification_unit=Parameter(
        cv_label="MS",
        cv_accession="MS:1002887",
        name="Progenesis QI normalised abundance",
    ),
    small_molecule_feature_quantification_unit=Parameter(
        cv_label="MS",
        cv_accession="MS:1002887",
        name="Progenesis QI normalised abundance",
    ),
    small_molecule_identification_reliability=Parameter(
        cv_label="MS",
        cv_accession="MS:1002896",
        name="compound identification confidence level",
    ),
    database=[
        Database(
            param=Parameter(name="inhouse"),
            prefix="HMDB",
            version="",
            uri="http://www.hmdb.org",
        )
    ],
    id_confidence_measure=[
        Parameter(cv_label="MS", cv_accession="MS:1002890", name="fragmentation score")
    ],
)

mztabm = MzTabM(metadata=MTD)
context = SerializationContext(convert_to="tsv")
logger.info(mztabm.to_tsv(context))
