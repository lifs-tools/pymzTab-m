import json
from pathlib import Path

from mztab_m_io.model.mztabm import MzTabM

if __name__ == "__main__":
    schema = MzTabM.model_json_schema(by_alias=True)
    with Path("mztab_m_io/schema/mztabm.schema-2.1.0-M.json").open("w") as f:
        json.dump(schema, f, indent=2)
