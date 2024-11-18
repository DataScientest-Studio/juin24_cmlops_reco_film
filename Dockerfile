####################################################################
# Base image
####################################################################
FROM python:3.10 as base

# Set the working directory in the container
WORKDIR /opt/workspace

# Install dependencies
COPY ./pyproject.toml ./pyproject.toml
RUN python -m pip install --upgrade pip
RUN python -m pip install poetry
RUN poetry config virtualenvs.create false

# Copy sources needed for API
COPY ./models ./models
COPY ./src ./src
COPY ./api.py ./app.py
COPY README.md README.md

####################################################################
# API image
####################################################################
FROM base as api

# Set the working directory in the container
WORKDIR /opt/workspace

# Install python packages for development
RUN poetry install
RUN poetry add fastapi httptools uvloop uvicorn

# Expose port 8000 for the API service
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8000", "--reload"]

####################################################################
# Dev image
####################################################################
FROM base as dev

# Install python packages
RUN poetry install
RUN poetry add fastapi httptools uvloop uvicorn


####################################################################
# python exporter for prometheus image
####################################################################
# Stage for CSV Exporter
FROM base AS csv_exporter

COPY csv_exporter.py ./csv_exporter.py
RUN pip install prometheus_client

CMD ["python", "csv_exporter.py"]
