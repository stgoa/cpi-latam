# -*- coding: utf-8 -*-
"""This module contains the base class for CPI parsers."""

from abc import ABC, abstractmethod
from datetime import date
from enum import Enum

import pandas as pd
from pandera import Check, Column, DataFrameSchema, DateTime, Float
from pandera.typing import DataFrame


class CPIColumns(Enum):
    """Enum for the CPI columns."""

    DATE = "date"
    CPI = "cpi"
    REFERENCE_DATE = "reference_date"


CPI_SCHEMA = DataFrameSchema(
    columns={
        CPIColumns.DATE.value: Column(
            DateTime,
            nullable=False,
            checks=[
                Check(lambda x: x.dt.day == 1, error="The day must be the first day of the month."),
            ],
        ),
        CPIColumns.CPI.value: Column(Float, nullable=False),
        CPIColumns.REFERENCE_DATE.value: Column(
            DateTime,
            nullable=False,
            checks=[
                Check(lambda x: x.dt.day == 1, error="The day must be the first day of the month."),
            ],
        ),
    },
    coerce=True,
    strict=True,
)


class BaseCPIParser(ABC):
    """Base class for CPI parsers."""

    month_map = {
        # Peru format
        "Ene": 1,
        "Feb": 2,
        "Mar": 3,
        "Abr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Ago": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dic": 12,
        # Colombia/Chile format
        "Enero": 1,
        "Febrero": 2,
        "Marzo": 3,
        "Abril": 4,
        "Mayo": 5,
        "Junio": 6,
        "Julio": 7,
        "Agosto": 8,
        "Septiembre": 9,
        "Octubre": 10,
        "Noviembre": 11,
        "Diciembre": 12,
    }

    def __init__(self, local_file_path: str, url: str, source_format: str, country: str):
        """Initializes the parser.

        Args:
            local_file_path (str): The path to the local file.
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
        self.local_file_path: str = local_file_path
        self.url: str = url
        self.data: pd.DataFrame = None
        self.reference_date: date = None
        self.start_date: date = None
        self.end_date: date = None
        self.source_format: str = source_format
        self.country: str = country
        # initialize the data
        self.read()

    @abstractmethod
    def parse(self) -> None:
        """Parses the source cpi data into a pandas DataFrame with the universal schema.

        Returns:
            pd.DataFrame: A pandas DataFrame with the universal schema.
        """
        pass

    @abstractmethod
    def download(self) -> None:
        """Downloads the raw data from the internet and saves it to a local file in csv format."""
        pass

    @abstractmethod
    def save(self) -> None:
        """Saves the parsed data to a local csv file."""
        pass

    def read(self) -> None:
        """Reads the parsed csv data from the local csv file into a pandas DataFrame."""
        self.data = pd.read_csv(self.local_file_path, parse_dates=["date"])

    def update(self) -> None:
        """Updates the data by downloading the raw data and reading it into a pandas DataFrame."""
        self.download()
        self.read()

    def get_data(self) -> DataFrame[CPI_SCHEMA]:
        """Returns the data in a pandas DataFrame with the universal schema.

        Returns:
            pd.DataFrame: A pandas DataFrame with the universal schema.
        """
        return self.data
