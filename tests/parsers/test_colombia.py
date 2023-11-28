import pandas as pd
import pytest

from cpilatam.parsers.colombia import ColombiaCPIParser
from cpilatam.schemas import CPI_SCHEMA


class TestColombiaParser:
    @pytest.fixture
    def setUp(self, monkeypatch):
        # crear instancia
        self.parser = ColombiaCPIParser()

        # mock download using monkeypatch
        monkeypatch.setattr(self.parser, "download", self.mock_download)

    def mock_download(self):
        # Read the data and assign it to self.data
        self.parser.data = pd.read_excel("tests/data/colombia.xlsx")

    def test_parse(self, setUp):
        # read data
        self.parser.download()

        # proceed to parse the data
        self.parser.parse()

        # assert that the schema is correct
        CPI_SCHEMA.validate(self.parser.data)
