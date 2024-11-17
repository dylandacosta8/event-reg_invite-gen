import uuid
from sqlalchemy import ForeignKey, Column, Boolean, Integer, String, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.database import Base

class Invitation(Base):
    __tablename__ = 'invitations'

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    invite_code: Mapped[str] = Column(String, unique=True, index=True)
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    used: Mapped[bool] = Column(Boolean, default=False)
    used_at: Mapped[datetime] = Column(DateTime, nullable=True)
    nickname: Mapped[str] = Column(String, nullable=False)
