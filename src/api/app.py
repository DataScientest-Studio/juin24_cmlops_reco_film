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
        {"name": "bd", "description": "bd functions"},
        {
            "name": "other",
            "description": "functions that are used to deal with items",
        },
    ],
)


# Return a welcome message
# - Route: GET /
# - Test: curl -X GET -i http://127.0.0.1:8000/
@api.get("/", name="Hello World", tags=["other"])
def get_welcome() -> str:
    """Welcome message

    Returns:
        str: welcome message
    """
    return "*** Welcome to RecoFilm API! ***"
