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

    def __init__(self, url: str, start_date: date, end_date: date):
        """Initializes the parser.

        Args:
            url (str): The url to the source data.
            start_date (date): The start date of the data.
            end_date (date): The end date of the data.

        Attributes:
            url (str): The url to the source data.
            start_date (date): The start date of the data.
            end_date (date): The end date of the data.
            data (pd.DataFrame): The data in a pandas DataFrame with the universal schema.
            reference_date (date): The reference/pivot for the CPI valuees.
        """
        self.url: str = url
        self.start_date: date = start_date
        self.end_date: date = end_date
        self.data: pd.DataFrame = None
        self.reference_date: date = None

    @abstractmethod
    def parse(self) -> DataFrame[CPI_SCHEMA]:
        """Parses the source cpi data into a pandas DataFrame with the universal schema.

        Returns:
            pd.DataFrame: A pandas DataFrame with the universal schema.
        """
        pass

    @abstractmethod
    def download(self) -> None:
        """Downloads the data from the internet and saves it to a local file."""
        pass

    @abstractmethod
    def read(self) -> None:
        """Reads the data from the local file into a pandas DataFrame."""
        pass
