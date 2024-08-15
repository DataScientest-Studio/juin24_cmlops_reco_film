from typing import Optional

from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import datetime

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
