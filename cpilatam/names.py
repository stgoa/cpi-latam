from enum import Enum


class CPIColumns(Enum):
    """Enum for the CPI columns."""

    DATE = "date"
    CPI = "cpi"
    REFERENCE_DATE = "reference_date"


class Countries(Enum):
    """Enum for the Countries columns."""

    PERU = "peru"
    COLOMBIA = "colombia"
