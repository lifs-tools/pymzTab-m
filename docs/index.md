# pymzTab-m

Python implementation of the mzTab-M standard. Use it to parse, validate, and write mzTab-M files from Python code.

## Installation

The project uses [uv](https://docs.astral.sh/uv/) for environment management:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH=$HOME/.local/bin:$PATH
uv python install 3.12
uv sync
```

## Quickstart

```python
import json
from pathlib import Path

import mztabm

file_path = "tests/data/example/example.mztab"
result: mztabm.MzTabMLoadResult = mztabm.read(file_path)

for message in result.messages:
    print(message.message_type.name, message.message)

mztabm_dict = mztabm.convert_to_dict(result.mztabm)
print("mzTab-M Id", mztabm_dict.get("mzTab-ID"))

temp_folder = Path(".temp/mztabm")
target_path = temp_folder / Path("example.mztab")
mztabm.write(result.mztabm, str(target_path), format="tsv")
```

## Links

- Project repository: https://github.com/lifs-tools/pymzTab-m
- mzTab-M standard: https://github.com/HUPO-PSI/mzTab
