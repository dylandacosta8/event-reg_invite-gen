from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class InviteCreate(BaseModel):
    invitee_email: EmailStr = Field(..., example="invitee@example.com")
    nickname: str = Field(..., example="JohnDoe123")

class InviteUpdate(BaseModel):
    invitee_email: Optional[EmailStr] = Field(None, example="invitee@example.com")

class InviteResponse(BaseModel):
    id: UUID
    invitee_email: str
    invite_code: str
    nickname: str
    user_id: Optional[UUID]
    created_at: datetime
    used: bool
    used_at: Optional[datetime]

    class Config:
        from_attributes = True

class InviteListResponse(BaseModel):
    items: List[InviteResponse] = Field(..., example=[
        {
            "id": 1,
            "invitee_email": "invitee@example.com",
            "invite_code": "ABC123XYZ",
            "nickname": "JohnDoe123",
            "user_id": "a12b34c5-d67e-890f-1234-567890abcdef",
            "created_at": "2024-11-18T12:00:00Z",
            "used": False,
            "used_at": None
        }
    ])
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
