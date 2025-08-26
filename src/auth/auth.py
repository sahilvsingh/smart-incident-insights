from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta

from src.api.jwt_utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# Demo user store
_fake_users_db = {
    "admin": {"username": "admin", "password": "admin123", "id": 1},
}

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=LoginResponse)
def login_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = _fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(
        data={"sub": str(user["id"])},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer"}
