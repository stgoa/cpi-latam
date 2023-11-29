# -*- coding: utf-8 -*-
"""This module contains a parser for the Colombian CPI data."""

import re

import pandas as pd

from cpilatam import SETTINGS, logger
from cpilatam.names import Countries, CPIColumns
from cpilatam.parsers.base import BaseCPIParser


class ColombiaCPIParser(BaseCPIParser):
    def __init__(self):
        super().__init__(
            local_file_path=SETTINGS.COLOMBIA_LOCAL_PATH.as_posix(),
            url="https://www.dane.gov.co/files/operaciones/IPC/oct23/IPC_Indices.xlsx",
            country=Countries.COLOMBIA.value,
        )

    def download(self) -> None:
        """Downloads the data from the url and stores it in the self.data attribute."""
        logger.info("Downloading data from %s", self.url)
        # Read the Excel file into a pandas DataFrame
        self.data = pd.read_excel(self.url)

    def parse(self) -> None:
        """Parses the source cpi data into a pandas DataFrame with the universal schema."""
        logger.info(f"Parsing the data of {self.country}")
        if self.data is not None:
            # Get the date of obtanining the data
            data_obtain_date = self.data.iloc[6, 21]

            # Use regex to obtain day month year
            pattern = r"(\w+) de (\d{4})"
            matches = re.search(pattern, data_obtain_date)

            if matches:
                month, year = matches.groups()
                month = self.month_map[month]
                obtained_date = pd.to_datetime(f"{year}-{month:02d}")
            else:
                raise Exception("Date not found")

            # Get relevant data from the excel spreadsheet
            cleaned_data = self.data.iloc[7:20, 0:22]

            # Set the seventh row as column headers
            cleaned_data.columns = cleaned_data.iloc[0]

            # Remove the seventh row (it's now the header)
            cleaned_data = cleaned_data[1:]

            # Transform the "Mes" column according to the self.month_map dictionary of the abstract class
            cleaned_data["Mes"] = cleaned_data["Mes"].map(self.month_map)

            # Pivot the DataFrame to obtain a flattened time series
            flattened_data = cleaned_data.melt(id_vars=["Mes"], var_name="Año", value_name=CPIColumns.CPI.value)

            # Convert years to numeric
            flattened_data["Año"] = flattened_data["Año"].astype(int)

            def add_months(row):
                if pd.isnull(row["Año"]) or pd.isnull(row["Mes"]):
                    return pd.NaT  # Return NaT for missing values
                return pd.to_datetime(str(row["Año"]), format="%Y") + pd.DateOffset(months=row["Mes"] - 1)

            # Proceed to sum the year with the month to obtain a datetime object
            flattened_data[CPIColumns.DATE.value] = flattened_data.apply(add_months, axis=1)

            # Add the obtained date
            flattened_data[CPIColumns.REFERENCE_DATE.value] = obtained_date

            # Filter the data beyond the today date
            flattened_data = flattened_data[
                flattened_data[CPIColumns.DATE.value] <= pd.Timestamp.now().normalize()
            ]

            # Filter the non nan data
            first_non_nan = flattened_data[CPIColumns.CPI.value].first_valid_index()
            last_non_nan = flattened_data[CPIColumns.CPI.value].last_valid_index()

            # Slice the dataframe
            flattened_data = flattened_data.loc[first_non_nan:last_non_nan]

            # Fill the NaN values with the previous value in the range (in place)
            flattened_data[CPIColumns.CPI.value].fillna(method="ffill", inplace=True)

            # Updated self.data and slice
            self.data = flattened_data[
                [CPIColumns.DATE.value, CPIColumns.CPI.value, CPIColumns.REFERENCE_DATE.value]
            ]

        else:
            logger.info("No data to parse. Please run the 'download' method first.")
            return None


if __name__ == "__main__":
    parser = ColombiaCPIParser()
    # Download data
    parser.download()

    # Parse and display the transformed data
    parser.parse()
    print(parser.data)
