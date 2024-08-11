# API

## Run the API
```
poetry run python3 -m uvicorn app:api --reload
```

## Doc API
* `http://localhost:8000/docs`
* `http://localhost:8000/redoc`

## Test API

* Simple GET
``` 
curl -X GET -i http://127.0.0.1:8000/
```