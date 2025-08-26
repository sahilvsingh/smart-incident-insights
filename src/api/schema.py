# src/api/schema.py
from pydantic import BaseModel, Field
from typing import Optional

class IncidentIn(BaseModel):
    incident_id: str = Field(..., description="External incident identifier")
    description: str = Field(..., description="Incident description")
    category: Optional[str] = Field(None, description="Optional category override")

class IncidentOut(BaseModel):
    id: int
    incident_id: str
    description: str
    category: Optional[str]
    received_at: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
