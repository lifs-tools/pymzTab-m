# mzTab-M Python Implementation

## Requirements

Python 3.12 and 3.12+

## Installation

```bash
# install python package manager uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# add $HOME/.local/bin to your PATH, either restart your shell or run
export PATH=$HOME/.local/bin:$PATH

# install git from https://git-scm.com/downloads
# Linux command
# apt update; apt install git -y

# Mac command
# brew install git

# clone project from github
git clone https://github.com/lifs-tools/pymzTab-m

git checkout development

# install python if it is not installed
uv python install 3.12

# install python dependencies
uv sync

# open your IDE (vscode, pycharm, etc.) and set python interpreter as .venv/bin/python

```

## Usage

```python
# These features are still experimental.

import mztab_m_io as mztabm

file_path = "tests/data/example/example.mztab"
result: mztabm.MzTabMLoadResult = mztabm.read(file_path)
for message in result.messages:
    print(message.message_type.name, message.message)
mztabm_model = result.mztabm

# You can use model object to get data in mzTab-M file
print("mzTab-M Id", result.mztabm.metadata.mztab_id)

# You can convert model to json and fetch values from dictionary
mztabm_dict = mztabm.convert_to_dict(result.mztabm)
print("mzTab-M Id",  mztabm_dict.get("mzTab-ID"))

# if you have a json version of mzTab-M, you can read it with format parameter.
file_path = "tests/data/example/example.json"
result: mztabm.MzTabMLoadResult = mztabm.read(file_path, format="json")

# you can also load from dictionary
with open(file_path) as f:
    mztabm_dict = json.load(f)
mztabm_model = mztabm.load_from_dict(mztabm_dict)

# You can write model object to mzTab-M file as tsv, json or yaml
temp_folder = Path(".temp/mztabm")
target_path = temp_folder / Path("example.mztab")
mztabm.write(result.mztabm, str(target_path), format="tsv")

# Following feature are not tested yet
target_path = temp_folder / Path("example.json")
mztabm.write(result.mztabm, str(target_path), format="json")
target_path = temp_folder / Path("example.yaml")
mztabm.write(result.mztabm, str(target_path), format="yaml")
```

Example mztabm object model definition

```python

from mztab_m_io.model.common import (
    CV,
    Assay,
    ColumnParameterMapping,
    Contact,
    Database,
    Instrument,
    MsRun,
    Parameter,
    Publication,
    Sample,
    SampleProcessing,
    Software,
    StudyVariable,
    Uri,
)
from mztab_m_io.model.mztabm import MzTabM
from mztab_m_io.model.section.mtd import Metadata
from mztab_m_io.model.section.sme import SmallMoleculeEvidence
from mztab_m_io.model.section.smf import SmallMoleculeFeature
from mztab_m_io.model.section.sml import SmallMoleculeSummary
import mztab_m_io as mztabm

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
    assay=[Assay(id=1, name="assay 1", ms_run_ref=[1])],
    study_variable=[
        StudyVariable(
            name="study variable 1",
            assay_refs=[1],
            factors=[Parameter(cv_label="XX", cv_accession="XX:0012", name="factor 1")],
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

mztabm_model = mztabm.MzTabM(
    metadata=MTD,
    small_molecule_summary=[
        SmallMoleculeSummary(sml_id=1, database_identifier=["HMDB0002111"])
    ],
)

mztabm.write(mztabm=mztabm_model, file_path="./output.mztab")


```

## Authors

ozgury@ebi.ac.uk, n.hoffmann@fz-juelich.de
