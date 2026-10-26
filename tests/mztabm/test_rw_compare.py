import decimal
import logging
import pathlib
import re
from typing import List

import pytest

import mztab_m_io
from mztab_m_io.model.section.sme import SmallMoleculeEvidence
from mztab_m_io.model.section.smf import SmallMoleculeFeature
from mztab_m_io.model.section.sml import SmallMoleculeSummary
from mztab_m_io.model.serialization import TableSerialization

logger = logging.getLogger(__name__)


def is_ignored_table_field(field: str):
    return TableSerialization.model_validate(
        field.json_schema_extra or {}, by_alias=True
    ).ignore


headers = {
    "SFH": (
        "SMF",
        [
            SmallMoleculeFeature.model_fields.get(k).validation_alias or k
            for k, v in SmallMoleculeFeature.model_fields.items()
            if not is_ignored_table_field(v)
        ],
        SmallMoleculeFeature,
    ),
    "SEH": (
        "SME",
        [
            SmallMoleculeEvidence.model_fields.get(k).validation_alias or k
            for k, v in SmallMoleculeEvidence.model_fields.items()
            if not is_ignored_table_field(v)
        ],
        SmallMoleculeEvidence,
    ),
    "SMH": (
        "SML",
        [
            SmallMoleculeSummary.model_fields.get(k).validation_alias or k
            for k, v in SmallMoleculeSummary.model_fields.items()
            if not is_ignored_table_field(v)
        ],
        SmallMoleculeSummary,
    ),
}


def normalize_mztab_content(content: str) -> List[str]:
    """
    Normalize MzTab content for content comparison.
    1. Strip whitespace from lines.
    2. Ignore empty lines.
    3. Separate MTD lines and sort them (since order doesn't strictly matter).
    4. Keep other lines in order.
    5. Normalize internal whitespace (tabs vs spaces) - "ignore space differences".
    6. sort table columns alphabatically.
    Table column orders and missing/extra columns are ignored.
    """
    lines = [x for x in content.splitlines() if x and x.strip()]
    all_line_splits = []

    current_headers = {
        "SFH": "SMF",
        "SEH": "SME",
        "SMH": "SML",
    }
    sections = {"SMF": [], "SME": [], "SML": []}

    for idx, x in enumerate(lines):
        # normalize whitespaces before and after | ] characters
        normalized = re.sub(r"[\n\r ]+", " ", x)
        normalized2 = re.sub(r"\s*]", "]", normalized)
        normalized3 = re.sub(r"\s*,\s*", ", ", normalized2)
        normalized4 = re.sub(r"\s*\|\s*", " | ", normalized3)
        normalized5 = re.sub(r"\s*\|\s*$", "", normalized4)
        x = normalized5
        parts = [a.strip() for a in x.split("\t")]

        if parts[0] in current_headers:
            # remove table headers if they are empty
            if len(lines) <= idx + 1:
                continue
            elif len(lines) > idx + 1:
                if not lines[idx + 1].startswith(current_headers[parts[0]]):
                    continue
            parts = [x for x in parts if x and x.strip()]
            base = parts[1:]
            default_column_headers = headers[parts[0]][1]

            base_indices = {v: idx for idx, v in enumerate(parts)}
            # base_indices[0] = 0
            extra_columns = {
                x
                for x in base_indices
                if not x.startswith("opt_")
                and x != parts[0]
                and x.strip().split("[")[0] not in default_column_headers
            }
            # if extra_columns:
            # print("Extra columns:", extra_columns)
            sorted = [x for x in base if x not in extra_columns]
            sorted.sort()

            new_order = {idx: base_indices[v] for idx, v in enumerate(sorted, start=1)}
            new_order[0] = 0
            new_list_order_source = [new_order[idx] for idx in range(len(new_order))]
            sections[current_headers[parts[0]]].extend(new_list_order_source)
            new_parts = [
                parts[new_list_order_source[k]]
                for k in range(len(new_list_order_source))
            ]

            parts = new_parts
        elif parts[0] in sections and sections[parts[0]]:
            source = sections[parts[0]]
            if len(parts) < len(source):
                parts.extend(["null" for x in range(len(source) - len(parts))])

            new_parts = [parts[source[x]] for x in range(len(source))]
            parts = new_parts

        all_line_splits.append([x.replace('"', "") for x in parts])

    all_line_splits.sort(
        key=lambda x: (
            (1, x[0], x[1], x[2]) if not x[0].startswith("COM") else (2, x[0], x[1])
        )
    )

    return all_line_splits


def is_scientific_number(s):
    try:
        if s and s.lower() in ["nan", "inf", "-inf"]:
            return False
        float(s)
        return True
    except ValueError:
        return False


# Dynamically collect files
files_to_test = list(pathlib.Path("tests/data/mztabm").glob("*.[mM][zZ][tT][aA][bB]"))


@pytest.mark.parametrize("source_path", files_to_test)
def test_mztab_roundtrip(source_path):
    """
    Test roundtrip for a given mztab file.
    """
    # print(f"Testing {source_path.name}")

    # 1. Read
    # Default format is TSV if not specified, but these are mztab files
    # which are TSV based.
    # We use from_tsv_file explicitly or read()
    result = mztab_m_io.read(str(source_path))

    # If read fails, test fails (unless we expect some to fail? user didn't say)
    assert result.success, f"Failed to read {source_path}: {result.messages}"
    mztabm = result.mztabm

    # 2. Write to .temp
    temp_dir = pathlib.Path(".temp")
    temp_dir.mkdir(exist_ok=True)
    target_path = temp_dir / source_path.name

    # Use write function which uses to_tsv
    result = mztab_m_io.write(mztabm, str(target_path), format="tsv")
    assert result.success, f"Failed to write {target_path}: {result.messages}"

    # 2.5. Normalize content
    source_content = normalize_mztab_content(source_path.read_text())
    target_content = normalize_mztab_content(target_path.read_text())
    normalized_source_content = "\n".join(
        ["\t".join(x).strip() for x in source_content]
    )
    normalized_target_content = "\n".join(
        ["\t".join(x).strip() for x in target_content]
    )
    normalized_source_path = temp_dir / (source_path.name + ".normalized_source")
    normalized_target_path = temp_dir / (source_path.name + ".normalized_target")
    normalized_source_path.write_text(normalized_source_content)
    normalized_target_path.write_text(normalized_target_content)
    inconsistencies = []
    for i, line in enumerate(source_content):
        if len(target_content) <= i:
            line_str = "\t".join(line)
            inconsistencies.append(f"Line {i} missing in target: {line_str}")
            continue
        min_len = min(len(line), len(target_content[i]))
        for cell in range(min_len):
            val1 = line[cell]
            val2 = target_content[i][cell]
            matched = False
            if not line[0].startswith("COM") and (
                is_scientific_number(val1) and is_scientific_number(val2)
            ):
                try:
                    v1 = decimal.Decimal(float(val1)).quantize(
                        decimal.Decimal("1." + "0" * 5),
                        rounding=decimal.ROUND_HALF_UP,
                    )
                    v2 = decimal.Decimal(float(val2)).quantize(
                        decimal.Decimal("1." + "0" * 5),
                        rounding=decimal.ROUND_HALF_UP,
                    )
                    # compare first 4 digits
                    matched = str(v1)[:4] == str(v2)[:4]
                except Exception as e:
                    matched = str(val1.replace('"', "")) == str(val2.replace('"', ""))
                    if not matched:
                        inconsistencies.append(
                            f"Numeric comparison failed: {val1} {val2}: {e}"
                        )
            else:
                matched = str(val1.replace('"', "")) == str(val2.replace('"', ""))
            if not matched:
                inconsistencies.append(
                    f"{line[0]} {line[1]} mismatched column {cell}: {val1} != {val2}"
                )
    if inconsistencies:
        raise AssertionError("Inconsistencies found:\n" + "\n".join(inconsistencies))

    assert len(source_content) == len(target_content), "Line count mismatch"
