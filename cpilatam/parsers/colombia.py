# -*- coding: utf-8 -*-
"""This module contains a parser for the Colombian CPI data."""

import pandas as pd


class ColombiaCPIParser:
    def __init__(self):
        # URL of the Excel file
        self.url = "https://www.dane.gov.co/files/operaciones/IPC/oct23/IPC_Indices.xlsx"
        self.data = None
        self.local_path = "data/colombia_cpi.csv"

    def read(self):
        # Read the Excel file into a pandas DataFrame
        self.data = pd.read_excel(self.local_path)

    def download(self):
        # Read the Excel file into a pandas DataFrame
        self.data = pd.read_excel(self.url)

    def parse(self):
        if self.data is not None:
            cleaned_data = self.data.iloc[8:19, 0:22]
            cleaned_data = cleaned_data.dropna(how="all", axis=0).dropna(how="all", axis=1)

            # Extract the relevant data
            parsed_data = cleaned_data.rename(columns=cleaned_data.iloc[0]).iloc[1:, 1:]

            # Convert the "Mes" column to datetime format
            parsed_data["Mes"] = pd.to_datetime(parsed_data["Mes"], format="%B", errors="coerce")

            # Pivot the DataFrame to obtain a flattened time series
            flattened_data = parsed_data.melt(id_vars=["Mes"], var_name="Año", value_name="CPI")

            return flattened_data

        else:
            print("No data to parse. Please run the 'download' method first.")
            return None


if __name__ == "__main__":
    parser = ColombiaCPIParser()
    # parser.download()
    parser.read()
    data = parser.parse()
    print(data)
