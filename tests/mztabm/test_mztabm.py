import json
import shutil
from pathlib import Path

import mztab_m_io as mztabm


def test_read_01():
    """
    tsv file read
    """
    file_path = "tests/data/example/example2.mztab"
    result: mztabm.MzTabMLoadResult = mztabm.read(file_path)
    # for message in result.messages:
    #     print(message.message_type.name, message.message)

    assert result.success
    assert result.mztabm
    mztabm_dict, context = mztabm.convert_to_dict(result.mztabm)
    assert mztabm_dict


def test_read_02():
    """
    json file read
    """
    file_path = "tests/data/example/example.json"

    result: mztabm.MzTabMLoadResult = mztabm.read(file_path, format="json")
    # for message in result.messages:
    #     print(message.message_type.name, message.message)
    assert result.success
    assert result.mztabm
    mztabm_dict = mztabm.convert_to_dict(result.mztabm)
    assert mztabm_dict


def test_read_03():
    """
    yaml file read
    """
    file_path = "tests/data/example/example.yaml"

    result: mztabm.MzTabMLoadResult = mztabm.read(file_path, format="yaml")
    # for message in result.messages:
    #     print(message.message_type.name, message.message)
    assert result.success
    assert result.mztabm
    mztabm_dict = mztabm.convert_to_dict(result.mztabm)
    assert mztabm_dict


def test_load_from_dict():
    """
    Load from dict
    """
    file_path = "tests/data/example/example.json"
    with Path(file_path).open() as f:
        mztabm_dict = json.load(f)
    mztabm_model = mztabm.load_from_dict(mztabm_dict)
    assert mztabm_model


def test_write_01():
    """
    write an mztab-M model to tsv file
    """
    file_path = "tests/data/example/example.mztab"

    result: mztabm.MzTabMLoadResult = mztabm.read(file_path)
    # for message in result.messages:
    #     print(message.message_type.name, message.message)
    temp_folder = Path(".temp/mztabm")
    target_path = temp_folder / Path("example.mztab")
    try:
        mztabm.write(result.mztabm, str(target_path), format="tsv")
    finally:
        shutil.rmtree(temp_folder)
        pass


def test_write_02():
    """
    write an mztab-M model to json file
    """
    file_path = "tests/data/example/example.json"

    result: mztabm.MzTabMLoadResult = mztabm.read(file_path, format="json")
    # for message in result.messages:
    #     print(message.message_type.name, message.message)
    temp_folder = Path(".temp/mztabm")
    target_path = temp_folder / Path("example.json")
    try:
        mztabm.write(result.mztabm, str(target_path), format="json")
    finally:
        shutil.rmtree(temp_folder)


def test_write_03():
    """
    write an mztab-M model to yaml file
    """
    file_path = "tests/data/example/example.yaml"

    result: mztabm.MzTabMLoadResult = mztabm.read(file_path, format="yaml")
    # for message in result.messages:
    #     print(message.message_type.name, message.message)
    temp_folder = Path(".temp/mztabm")
    target_path = temp_folder / Path("example.yaml")
    try:
        mztabm.write(result.mztabm, str(target_path), format="yaml")
    finally:
        shutil.rmtree(temp_folder)
