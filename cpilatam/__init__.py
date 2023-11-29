# -*- coding: utf-8 -*-
"""Top level package for recursiveseriation"""

import pandas as pd

from cpilatam.logger import configure_logging
from cpilatam.names import Countries, CPIColumns
from cpilatam.settings import init_settings

__app_name__ = "cpilatam"
__version__ = "2023.11.1"

SETTINGS = init_settings()
logger = configure_logging(__app_name__ + " - v" + __version__, SETTINGS, kidnap_loggers=True)

# TODO: Add border case at the init if the file doesn't exist

DF_CPI_PERU = pd.read_csv(SETTINGS.PERU_LOCAL_PATH.as_posix())
DF_CPI_COLOMBIA = pd.read_csv(SETTINGS.COLOMBIA_LOCAL_PATH.as_posix())

DF_CPI = {Countries.PERU.value: DF_CPI_PERU, Countries.COLOMBIA.value: DF_CPI_COLOMBIA}

for key, item in DF_CPI.items():
    if item[CPIColumns.DATE.value].max() <= pd.to_datetime("today").strftime("%Y-%m-%d"):
        logger.warn(f"The data is not up to date in the {key} country. Please run the update script.")


def update(countries: list = None):
    from cpilatam.parsers import __parsers__

    if countries is None:
        countries = DF_CPI.keys()
    for parser in __parsers__:
        if parser.country in countries:
            parser.update()
