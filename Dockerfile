FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

ENV PYTHONPATH="/var/task/formula_1_etl"

COPY pyproject.toml poetry.lock ./

RUN python3 -m pip install poetry
RUN poetry install --only main

COPY formula_1_etl/ ./formula_1_etl/
