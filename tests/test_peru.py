import pandas as pd
import pytest

from cpilatam.parsers.base import CPI_SCHEMA
from cpilatam.parsers.peru import PeruCPIParser


class TestPeruParser:
    @pytest.fixture
    def setUp(self, monkeypatch):
        # crear instancia
        self.parser = PeruCPIParser()

        # mock download using monkeypatch
        monkeypatch.setattr(self.parser, "download", self.mock_download)

    def mock_download(self):
        # Read the data and assign it to self.data
        self.parser.data = pd.read_csv("data/raw/peru.csv")

    def test_parse(self, setUp):
        # read data
        self.parser.download()

        # assert that the schema is correct
        CPI_SCHEMA.validate(self.parser.data)
