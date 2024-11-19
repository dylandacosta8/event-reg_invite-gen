import uuid
from sqlalchemy import ForeignKey, Column, Boolean, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database import Base

class Invitation(Base):
    __tablename__ = 'invitations'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    invitee_email: Mapped[str] = Column(String(255), unique=True, nullable=False, index=True)
    invite_code: Mapped[str] = Column(String, unique=True, index=True)
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    used: Mapped[bool] = Column(Boolean, default=False)
    used_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    nickname: Mapped[str] = Column(String, nullable=False)
