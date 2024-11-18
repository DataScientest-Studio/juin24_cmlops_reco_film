import hashlib
from typing import Annotated


from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import datetime


from src.models.predict_model import make_predictions
from src.models.train_model import train_and_register_model


# API
api = FastAPI(
    title="Film Recommender API",
    description="An API that provides personalized movie recommendations based on user preferences and viewing history.",
    version="0.1.0",
    contact={
        "name": "Your Name",
        "url": "http://yourwebsite.com/contact",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "test",
            "description": "test API is running",
        },
        {
            "name": "inference",
            "description": "Endpoints related to generating movie recommendations.",
        },
        {
            "name": "training",
            "description": "Endpoint for training the model (admin only).",
        },
    ],
)

# Security
security = HTTPBasic()

# User DB
# - username: (user_id, md5(mdp))
USER_DB: dict[str, tuple[int, str]] = {
    "alice": (1, "9dd4e461268c8034f5c8564e155c67a6"),
    "bob": (2, "9dd4e461268c8034f5c8564e155c67a6"),
    "admin": (0, "9dd4e461268c8034f5c8564e155c67a6", "admin"),
}


class BadCredentialException(Exception):
    def __init__(self, name: str, date: str, message: str):
        self.name = name
        self.date = date
        self.message = message


@api.exception_handler(BadCredentialException)
def QCMExceptionHandler(request: Request, exception: BadCredentialException):
    """
    Handle authentication errors.

    **Returns:**
    - JSON response with error details and a 418 status code.
    """
        status_code=418,
        content={
            "url": str(request.url),
            "name": exception.name,
            "message": exception.message,
            "date": exception.date,
        },
        movie_matrix_filename="data/processed/movie_matrix.csv",
        n_recommendations=3,
        log_file="predictions_log.csv",
    )


# Utils
def manage_authentication(credentials) -> tuple:
    """
    Authenticate the user based on provided credentials.

    **Parameters:**
    - `credentials` (HTTPBasicCredentials): The authentication credentials.

    **Returns:**
    - Tuple containing `user_id`, `username`, and `role`.

    **Raises:**
    - `BadCredentialException` if authentication fails.
    """
    # Compute hash password from the API
    str_clean = credentials.password
    hash_password = hashlib.md5(str_clean.encode()).hexdigest()

    # Retrieve user in DB and compare API hash to user hash password in DB
    user_record = USER_DB.get(credentials.username)
    if (user_record is None) or (user_record[1] != hash_password):
        raise BadCredentialException(
            name="bad_creds",
            message="Incorrect username or password.",
            date=str(datetime.datetime.now()),
        )
    user_id, _, role = user_record
    return user_id, credentials.username, role


# Routes
# - Hello
@api.get("/hello", name="Hello", tags=["test"])
from pydantic import BaseModel
from typing import List

class RecommendationsResponse(BaseModel):
    user_name: str
    recommendations: List[str]
    error_metric: float
    model_name: str
    model_version: str
    timestamp: str

@api.get("/hello", name="Hello", tags=["test"])
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> dict:
    """
    Greet the authenticated user.

    **Returns:**
    - `message` (str): A greeting message with the user's name.
    """
    return {"message": f"Hello {username}!"}


# - Train model
@api.post("/train", name="Train the model", tags=["training"])
def train_model_route(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> dict:
    """Endpoint to initiate model training. Accessible only to admin users."""
    user_id, username, role = manage_authentication(credentials=credentials)
    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action.",
        )

    # Start model training
    train_and_register_model()

    return {
        "message": "Model training initiated successfully.",
        "user_name": username,
        "timestamp": str(datetime.datetime.now()),
    }
@api.get("/recommend", name="Recommend a list of movies", tags=["inference"])
@api.get(
    "/recommend",
    name="Recommend a list of movies",
    tags=["inference"],
    response_model=RecommendationsResponse,
    response_description="A list of recommended movies and model details."
)
def get_recommend_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> dict:
    """
    Provide movie recommendations for the authenticated user.

    **Returns:**
    - `user_name` (str): Username of the authenticated user.
    - `recommendations` (List[str]): List of recommended movie titles.
    - `error_metric` (float): Error metric associated with the recommendations.
    - `model_name` (str): Name of the recommendation model used.
    - `model_version` (str): Version of the model.
    - `timestamp` (str): Time when the recommendations were generated.
    """
    user_id, username, role = manage_authentication(credentials=credentials)
    predictions = make_predictions(
        user_ids=[
            user_id,
        ],
        model_name="KNN_Recommendation_Model",  # Name of the registered model in MLflow
        user_matrix_filename="data/processed/user_matrix.csv",
    )
    return {
        "user_name": username,
        "recommendations": predictions.loc[0, 'recommendations'],
        "error_metric": predictions.loc[0, 'error_metric'],
        "model_name": predictions.loc[0, 'model_name'],
        "model_version": predictions.loc[0, 'model_version'],
        "timestamp": str(predictions.loc[0, 'timestamp']),
    }
