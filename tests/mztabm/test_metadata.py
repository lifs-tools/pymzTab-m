from mztab_m_io.model import Metadata


def test_empty_instantiation():
    instance = Metadata()
    assert instance.cv is None
