from pandera import Check, Column, DataFrameSchema, DateTime, Float

from cpilatam.names import CPIColumns

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
