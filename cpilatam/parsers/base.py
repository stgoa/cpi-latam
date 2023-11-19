# -*- coding: utf-8 -*-
"""This module contains the base class for CPI parsers."""

from abc import ABC, abstractmethod
from datetime import date

import pandas as pd
from pandera import Check, Column, DataFrameSchema, Int, String
from pandera.typing import DataFrame

# Define the schema for the universal CPI data.
CPI_SCHEMA = DataFrameSchema(
    columns={
        "date": Column(
            String,
            nullable=False,
            checks=[
                Check.str_matches(
                    r"^(0[1-9]|1[0-2])-(19|20)\d{2}$",
                    error="The date must be in the format MM-YYYY.",
                )
            ],
        ),
        "cpi": Column(Int, nullable=False),
        "reference_date": Column(
            String,
            nullable=False,
            checks=[
                Check.str_matches(
                    r"^(0[1-9]|1[0-2])-(19|20)\d{2}$",
                    error="The reference date must be in the format MM-YYYY.",
                )
            ],
        ),
    },
    coerce=True,
    strict=True,
)


class BaseCPIParser(ABC):
    """Base class for CPI parsers."""

    def __init__(self, url: str, source_format: str, country: str):
        """Initializes the parser.

        Args:
            url (str): The url to the source data.
            source_format (str): The format of the source data (e.g. csv, xls, etc.)
            country (str): The country of the CPI data.

        Attributes:
            url (str): The url to the source data.
            data (pd.DataFrame): The data in a pandas DataFrame with the universal schema.
            reference_date (date): The reference/pivot for the CPI valuees.
            start_date (date): The start date of the CPI data.
            end_date (date): The end date of the CPI data.
            source_format (str): The format of the source data (e.g. csv, xls, etc.)
            country (str): The country of the CPI data.
        """
        self.url: str = url
        self.data: pd.DataFrame = None
        self.reference_date: date = None
        self.start_date: date = None
        self.end_date: date = None
        self.source_format: str = source_format
        self.country: str = country

    @abstractmethod
    def parse(self) -> DataFrame[CPI_SCHEMA]:
        """Parses the source cpi data into a pandas DataFrame with the universal schema.

        Returns:
            pd.DataFrame: A pandas DataFrame with the universal schema.
        """
        pass

    @abstractmethod
    def download(self) -> None:
        """Downloads the data from the internet and saves it to a local file in csv format."""
        pass

    @abstractmethod
    def read(self) -> None:
        """Reads the data from the local csv file into a pandas DataFrame."""
        pass
