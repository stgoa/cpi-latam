# -*- coding: utf-8 -*-
"""This module contains a parser for the Colombian CPI data."""

import re

import pandas as pd

from cpilatam.parsers.base import CPIColumns


class ColombiaCPIParser:
    def __init__(self):
        # URL of the Excel file
        self.url = "https://www.dane.gov.co/files/operaciones/IPC/oct23/IPC_Indices.xlsx"
        self.data = None
        self.local_path = "data/colombia_cpi.csv"

        self.month_map = {
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

    def read(self):
        # Read the Excel file into a pandas DataFrame
        self.data = pd.read_excel(self.local_path)

    def download(self):
        # Read the Excel file into a pandas DataFrame
        self.data = pd.read_excel(self.url)

    def parse(self):
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
            # TODO: Filter the dates after current date
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

            # Updated self.data and slice
            self.data = flattened_data[
                [CPIColumns.DATE.value, CPIColumns.CPI.value, CPIColumns.REFERENCE_DATE.value]
            ]

            return self.data

        else:
            print("No data to parse. Please run the 'download' method first.")
            return None


if __name__ == "__main__":
    parser = ColombiaCPIParser()
    # parser.download()
    parser.read()
    data = parser.parse()
    print(data)
