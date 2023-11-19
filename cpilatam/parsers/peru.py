# -*- coding: utf-8 -*-
"""This module contains a parser for the Peruvian CPI data."""

from datetime import date

import pandas as pd
import requests
from bs4 import BeautifulSoup

from cpilatam.parsers.base import CPI_SCHEMA, BaseCPIParser


class PeruCPIParser(BaseCPIParser):
    BASE_URL = (
        "https://estadisticas.bcrp.gob.pe/estadisticas/"
        "series/mensuales/resultados/PN38705PM/html/{start_date}/{end_date}"
    )

    def __init__(
        self,
    ):
        start_date = date(1991, 1, 1).strftime("%Y-%-m")
        end_date = date.today().strftime("%Y-%-m")
        super().__init__(
            url=self.BASE_URL.format(start_date=start_date, end_date=end_date),
            source_format="html",
            country="Peru",
        )

    def convert_spanish_date_to_numeric_date(self, date_str: str) -> str:
        """Converts a Spanish date string to a numeric date string.

        Args:
            date_str (str): A Spanish date string in the format "MMMYYYY".

        Returns:
            str: A numeric date string in the format "MM-YYYY".

        Example:
            >>> convert_spanish_date_to_numeric_date("Dic2021")
            "12-2021"
        """
        month = date_str[:3]
        year = date_str[3:]
        month_num = self.month_map[month]
        new_date = f"{month_num:02}-{year}"
        return new_date

    def parse_spanish_date_col(self, df: pd.DataFrame, col_name: str = "date"):
        df[col_name] = df[col_name].apply(self.convert_spanish_date_to_numeric_date)
        df[col_name] = pd.to_datetime(df[col_name], format="%m-%y")
        return df

    def set_reference_date(self) -> None:
        """Extracts the reference date from the column name of the CPI column.

        Example:
            >>> parser = PeruCPIParser()
            >>> parser.download()
            >>> parser.data.columns[1]
            Índice de precios Lima Metropolitana (índice Dic.2021 = 100) - Índice de Precios al Consumidor (IPC)'
            >>> parser.set_reference_date()
            >>> parser.reference_date
            "2021-12-01"
        """
        if self.data is not None:
            # extract the column name
            cpi_col = self.data.columns[1]
            # extract the reference date from the column name
            reference_date_str = (
                cpi_col.split("Índice de precios Lima Metropolitana (índice ")[1].split(" =")[0].replace(".", "")
            )
            # convert the reference date to a datetime object
            reference_date = self.convert_spanish_date_to_numeric_date(reference_date_str)
            self.reference_date = reference_date
        else:
            print("No data to parse. Please run the 'download' method first.")
            return None

    def download(self):
        # Send a GET request to the URL
        response = requests.get(self.url, timeout=10)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the table based on the specified XPath
            table = soup.select_one("#frmMensual > div.barra-resultados > table")

            # Check if the table is found
            if table:
                # Use pandas to read the HTML table into a DataFrame
                self.data = pd.read_html(str(table))[0]
            else:
                print("Table not found on the webpage.")
        else:
            print(
                "Failed to retrieve the webpage. Status code:",
                response.status_code,
            )

    def parse(self):
        if self.data is not None:
            # Extract reference date from the column name
            self.set_reference_date()

            # rename the columns
            self.data.columns = ["date", "CPI"]

            # Extract year and month from the "Fecha" column
            self.data = self.parse_spanish_date_col(self.data)

            # Add the reference date to the DataFrame
            self.data["reference_date"] = self.reference_date

            # Select and reorder columns
            self.data = self.data[["date", "reference_date", "CPI"]]

            # Validate and parse the DataFrame
            self.data = CPI_SCHEMA.validate(self.data)

        else:
            print("No data to parse. Please run the 'download' method first.")
            return None

    def read(self, path: str = None):
        if path is None:
            path = "./data/peru_cpi.csv"
        self.data = pd.read_csv(path)
        return self.data


if __name__ == "__main__":
    # Example Usage:
    # Instantiate the class
    parser = PeruCPIParser()

    # Download data
    parser.download()

    # Parse and display the transformed data
    parsed_data = parser.parse()
    print(parsed_data)
