import uuid
from sqlalchemy import (ForeignKey, Column, Boolean, Integer, String)
from sqlalchemy.orm import Mapped
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Invitation(Base):
    __tablename__ = 'invitations'

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    invite_code: Mapped[str] = Column(String, unique=True, index=True)
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    used: Mapped[bool] = Column(Boolean, default=False)