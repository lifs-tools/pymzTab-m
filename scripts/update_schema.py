import json
from pathlib import Path

from mztab_m_io.model.mztabm import MzTabM

if __name__ == "__main__":
    schema = MzTabM.model_json_schema(mode="serialization")
    with Path("mztab_m_io/resources/profiles/mztabm.schema-2.1.0-M.json").open(
        "w"
    ) as f:
        json.dump(schema, f, indent=2, sort_keys=True)
