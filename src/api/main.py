from datetime import timedelta
from typing import Optional
from src.core.logging_config import logger

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from prometheus_fastapi_instrumentator import Instrumentator

from src.api.schema import IncidentIn, IncidentOut, LoginResponse
from src.api.jwt_utils import (
    hash_password,
    verify_password,
    create_access_token,
    decode_username_from_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from src.db.setup import create_schema
from src.db.queries import (
    create_user,
    get_user_by_username,
    insert_incident,
    get_incidents,
)
from src.ml.predict import predict_category


# Ensure DB tables exist on startup
create_schema()

app = FastAPI(title="Smart Incident Insights API")

# Attach Prometheus middleware *before* startup
instrumentator = Instrumentator().instrument(app)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    username = decode_username_from_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid/expired token"
        )
    return username


@app.on_event("startup")
async def startup_event():
    """Expose Prometheus metrics at /metrics after app starts"""
    instrumentator.expose(app)
    logger.info("🚀 Application started with Prometheus metrics enabled")


@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to Smart Incident Insights API"}


@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


# ----- Auth -----
@app.post("/auth/register", response_model=dict)
def register(username: str, password: str):
    logger.info(f"Attempt to register new user: {username}")
    existing = get_user_by_username(username)
    if existing:
        logger.warning(f"Registration failed, username already exists: {username}")
        raise HTTPException(status_code=400, detail="Username already exists")
    ph = hash_password(password)
    user = create_user(username, ph)
    logger.info(f"User registered: {username}")
    return {"msg": "registered", "username": user["username"]}


@app.post("/auth/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Login attempt for user: {form_data.username}")
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        logger.warning(f"Invalid login attempt for {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    logger.info(f"User logged in: {form_data.username}")
    return {"access_token": token, "token_type": "bearer"}


# ----- Incidents -----
@app.post("/incidents", response_model=IncidentOut)
def create_incident(payload: IncidentIn, username: str = Depends(get_current_username)):
    logger.info(f"User {username} creating incident: {payload.incident_id}")

    category = payload.category
    if not category:
        category = predict_category(payload.description)
        logger.debug(f"Predicted category for incident {payload.incident_id}: {category}")

    row = insert_incident(payload.incident_id, payload.description, category)
    logger.info(f"Incident created with ID {row['id']}")

    return {
        "id": row["id"],
        "incident_id": row["incident_id"],
        "description": row["description"],
        "category": row["category"],
        "received_at": row["received_at"].isoformat(),
    }


@app.get("/incidents", response_model=list[IncidentOut])
def list_incidents(limit: int = 100, offset: int = 0, username: str = Depends(get_current_username)):
    logger.info(f"User {username} fetching incidents limit={limit}, offset={offset}")
    rows = get_incidents(limit=limit, offset=offset)

    return [
        {
            "id": r["id"],
            "incident_id": r["incident_id"],
            "description": r["description"],
            "category": r["category"],
            "received_at": r["received_at"].isoformat(),
        }
        for r in rows
    ]
