# Reco Film

## Description

## Run the project

This project uses a [docker-compose](docker-compose.yml) to provides `services` relatives to our projects.
Here is the list of all our services:
* `api` provides project API 
* `dev` to develop the project using a docker container

### Run API
* Run API:
```
docker compose up api
```

When the API is running, the API documentation is provided here: [http://172.19.0.5:8000/docs](http://172.19.0.5:8000/docs).

* Test API:
```
curl -X GET -i http://172.19.0.5:8000/
```

* Infer using model into API:
```
curl -X 'GET' \
  'http://localhost:8000/recommend/1' \
  -H 'accept: application/json'
```

* Kill API:
```
docker container stop reco_api
```

### Dev

* Run the dev container:
```
docker compose run --rm dev
```

You are now inside the container. 

#### Test code from DataScientest 
NB: to rm after refacto !

* Get data:
```
poetry run python src/data/import_raw_data.py
```

* Construct the dataset:
```
poetry run python src/data/make_dataset.py data/raw data/processed
```

Create folder `data/processed`.

```
poetry run python src/features/build_features.py
```

* Prediction:
```
poetry run python src/models/predict_model.py
```

### Dev API
* Run API:
```
uvicorn api:api --host 0.0.0.0 --port 8000 --reload
```

* See doc here:[http://localhost:8000/docs](http://localhost:8000/docs)

* Test your code:
```
poetry run python test.py
```

## Technical documentation

### Technical choices

* To develop we recommend to use VSCode with extension [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff).

* We choose to use [poetry](https://python-poetry.org/) instead of `requirement.txt` because it *Python packaging and dependency management made easy*.


### Architecture

## References

### Useful
* [project template](https://github.com/DataScientest-Studio/Template_MLOps_movie_recommandation)
* [project board](https://github.com/users/Chrisdml/projects/1)

### Biblio