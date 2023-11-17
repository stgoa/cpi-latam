# -*- coding: utf-8 -*-
"""Top level package for recursiveseriation"""

from cpilatam.logger import configure_logging
from cpilatam.settings import init_settings

__app_name__ = "cpilatam"
__version__ = "2023.11.1"

SETTINGS = init_settings()
logger = configure_logging(__app_name__ + " - v" + __version__, SETTINGS, kidnap_loggers=True)
