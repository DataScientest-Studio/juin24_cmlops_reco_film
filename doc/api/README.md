# API

## Run the API
```
docker compose run --rm api
```

## See API Documentation
* `http://localhost:8000/docs`
* `http://localhost:8000/redoc`

## Test API

* Simple GET
``` 
curl -X GET -i http://172.19.0.5:8000/
```

## Kill API
```
docker container stop reco_api
docker container rm reco_api
```