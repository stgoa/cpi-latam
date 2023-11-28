import pandas as pd
import pytest

from cpilatam.parsers.peru import PeruCPIParser
from cpilatam.schemas import CPI_SCHEMA


class TestPeruParser:
    @pytest.fixture
    def setUp(self, monkeypatch):
        # crear instancia
        self.parser = PeruCPIParser()

        # mock download using monkeypatch
        monkeypatch.setattr(self.parser, "download", self.mock_download)

    def mock_download(self):
        # Read the data and assign it to self.data
        # The CSV has unrecognized Symbols. Another alternative is to replace those symbols "(?)" to "Í"
        self.parser.data = pd.read_csv("data/raw/peru.csv", encoding="latin-1")

    def test_parse(self, setUp):
        # read data
        self.parser.download()

        # proceed to parse the data
        self.parser.parse()

        # assert that the schema is correct
        CPI_SCHEMA.validate(self.parser.data)
