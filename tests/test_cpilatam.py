import pytest


def test_import():
    import cpilatam  # noqa: F401


def test_dataframe_schemas():
    from cpilatam import DF_CPI
    from cpilatam.schemas import CPI_SCHEMA

    assert isinstance(DF_CPI, dict)
    for df in DF_CPI.values():
        CPI_SCHEMA.validate(df)


@pytest.mark.scrapping
def test_update():
    from cpilatam import update

    update()
