from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import datetime


from src.models.predict_model import make_predictions

api = FastAPI(
    title="Film reco",
    description="Todo.",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "test",
            "description": "test API is running",
        },
        {"name": "inference", "description": "todo"},
    ],
)


@api.get("/", name="Hello World", tags=["test"])
def get_hello() -> dict:
    """Hello message

    Returns:
        dict: hello message
    """
    return {"message": "Hello"}


@api.get("/recommend/{user_id:int}", name="Recommend using model", tags=["inference"])
def get_recommend(user_id: int) -> dict:
    """Provides a recommendation using model

    Returns:
        dict: recommendation for a single user
    """
    predictions = make_predictions(
        users_ids=[
            user_id,
        ],
        model_filename="models/model.pkl",
        user_matrix_filename="data/processed/user_matrix.csv",
    )
    return {"recommend": predictions.tolist()}
