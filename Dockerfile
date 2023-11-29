FROM python:3.9 AS base
WORKDIR /cpi_latam
COPY pyproject.toml ./
ADD /cpilatam ./cpilatam
ENV PATH="/root/.local/bin:$PATH"
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi
# Test image
FROM base as tester
COPY tests ./tests
RUN pip install pytest
RUN pytest -s -vvv -m "not scrapping"
# Publish image
FROM base AS publisher
ARG PYPI_TOKEN
RUN poetry build
RUN poetry config pypi-token.pypi ${PYPI_TOKEN}
RUN poetry publish
