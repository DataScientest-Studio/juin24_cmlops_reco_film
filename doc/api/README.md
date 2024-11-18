# API

This document provides an exhaustive documentation about the API.

## Run the API
* In a terminal:
```
docker compose up api
```

* See API Documentation:
    * `http://172.19.0.5:8000/docs`
    * `http://172.19.0.5:8000/redoc`

* Test API is running:
``` 
curl -X GET -i http://172.19.0.5:8000/
```

* Kill API:
```
docker container stop reco_api
docker container rm reco_api
```

## Technical documentation
Our API calls are implemented using the Python framework FastAPI. The implementation can be found in the `api.py` file.

### Security

The API uses token-based authentication to secure endpoints. Users must provide valid credentials to obtain an authentication token, which is then used to access protected resources.

## CI/CD and Testing

This project uses several tools to ensure quality and continuous integration:

### CI/CD and Testing

This project uses several tools to ensure quality and continuous integration:

### MLflow

MLflow is used for tracking experiments, packaging code into reproducible runs, and sharing and deploying models. It helps in managing the machine learning lifecycle, including experimentation, reproducibility, and deployment.

MLflow is used for tracking experiments, packaging code into reproducible runs, and sharing and deploying models. It helps in managing the machine learning lifecycle, including experimentation, reproducibility, and deployment.

### Pytest

Pytest is used for writing and running tests. It is a mature testing framework that supports simple unit tests as well as complex functional testing. To run the tests, use the following command:

```
poetry run pytest -s
```

### GitHub Actions

GitHub Actions is used for automating workflows, including running tests and deploying the application. It helps in setting up a CI/CD pipeline to ensure that the code is always in a deployable state.
