import json
import pathlib

import pytest
import yaml

from mztab_m_io.model.mztabm import MzTabM


@pytest.fixture
def example_data_dir():
    return pathlib.Path("tests/data/example")


@pytest.fixture
def tsv_example(example_data_dir):
    return example_data_dir / "example.mztab"


@pytest.fixture
def json_example(example_data_dir):
    return example_data_dir / "example.json"


@pytest.fixture
def yaml_example(example_data_dir):
    return example_data_dir / "example.yaml"


def test_from_tsv_file(tsv_example):
    model, context = MzTabM.from_tsv_file(tsv_example)
    assert context is not None
    # We expect some validation messages might be present,
    # but basic parsing should succeed
    assert model is not None
    assert isinstance(model, MzTabM)
    assert model.metadata is not None


def test_from_json_file(json_example):
    model, context = MzTabM.from_json_file(json_example)
    assert context is not None
    assert model is not None
    assert isinstance(model, MzTabM)
    assert model.metadata is not None


def test_from_yaml_file(yaml_example):
    model, context = MzTabM.from_yaml_file(yaml_example)
    assert context is not None
    assert model is not None
    assert isinstance(model, MzTabM)
    assert model.metadata is not None


def test_from_dict(json_example):
    with json_example.open() as f:
        data = json.load(f)

    model, context = MzTabM.from_dict(data)
    assert context is not None
    assert model is not None
    assert isinstance(model, MzTabM)


def test_to_tsv(tsv_example):
    model, _ = MzTabM.from_tsv_file(tsv_example)
    assert model is not None

    # Create a dummy context for serialization
    from mztab_m_io.model.serialization import SerializationContext

    context = SerializationContext(source_format="tsv", messages=[])

    tsv_output = model.to_tsv(context)
    assert isinstance(tsv_output, str)
    assert len(tsv_output) > 0
    assert "MTD" in tsv_output


def test_save_load_tsv(tsv_example, tmp_path):
    model, _ = MzTabM.from_tsv_file(tsv_example)
    output_file = tmp_path / "test_output.mztab"

    # Test save
    context = model.save(str(output_file), format="tsv")
    assert context.success
    assert output_file.exists()

    # Test load
    loaded_model, load_context = model.load(str(output_file), format="tsv")
    assert loaded_model is not None
    assert isinstance(loaded_model, MzTabM)


def test_save_load_json(json_example, tmp_path):
    model, _ = MzTabM.from_json_file(json_example)
    output_file = tmp_path / "test_output.json"

    # Test save
    context = model.save(str(output_file), format="json")
    assert context.success
    assert output_file.exists()

    # Test load
    loaded_model, load_context = model.load(str(output_file), format="json")
    assert loaded_model is not None
    assert isinstance(loaded_model, MzTabM)


def test_save_load_yaml(yaml_example, tmp_path):
    model, _ = MzTabM.from_yaml_file(yaml_example)
    output_file = tmp_path / "test_output.yaml"

    # Test save
    context = model.save(str(output_file), format="yaml")
    assert context.success
    assert output_file.exists()

    # Test load
    loaded_model, load_context = model.load(str(output_file), format="yaml")
    assert loaded_model is not None
    assert isinstance(loaded_model, MzTabM)


def test_to_tsv_file(tsv_example, tmp_path):
    model, _ = MzTabM.from_tsv_file(tsv_example)
    output_file = tmp_path / "direct_output.mztab"

    context = model.to_tsv_file(str(output_file))
    assert context.success
    assert output_file.exists()
    assert "MTD" in output_file.read_text()


def test_to_json_file(json_example, tmp_path):
    model, _ = MzTabM.from_json_file(json_example)
    output_file = tmp_path / "direct_output.json"

    context = model.to_json_file(str(output_file))
    assert context.success
    assert output_file.exists()
    with output_file.open() as f:
        data = json.load(f)
    assert isinstance(data, dict)


def test_to_yaml_file(yaml_example, tmp_path):
    model, _ = MzTabM.from_yaml_file(yaml_example)
    output_file = tmp_path / "direct_output.yaml"

    context = model.to_yaml_file(str(output_file))
    assert context.success
    assert output_file.exists()

    with output_file.open() as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict)
