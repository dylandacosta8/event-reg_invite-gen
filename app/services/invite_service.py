from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from uuid import UUID
from app.models.invite_model import Invitation
from app.schemas.invite_schemas import InviteCreate, InviteUpdate
from app.services.email_service import EmailService
from datetime import datetime, timezone
from typing import Optional, List
import secrets
import logging
from qrcodegen.generation import generate_qr_code, store_qr_code_in_minio

logger = logging.getLogger(__name__)

class InviteService:
    @classmethod
    async def _execute_query(cls, session: AsyncSession, query):
        try:
            result = await session.execute(query)
            await session.commit()
            return result
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            await session.rollback()
            return None

    @classmethod
    async def create_invitation(
        cls, 
        session: AsyncSession, 
        user_id: UUID, 
        invitee_email: str, 
        nickname: str, 
        email_service: EmailService
    ) -> Optional[Invitation]:
        """
        Create an invitation linked to a user with a unique invite code and generate/store a QR code.
        :param session: Database session.
        :param user_id: ID of the user creating the invitation.
        :param invitee_email: Email address of the invitee.
        :param nickname: Nickname for the invitation.
        :param email_service: EmailService instance for sending emails.
        :return: Created Invitation object or None.
        """
        try:
            # Generate a unique invite code
            invite_code = secrets.token_urlsafe(8)
            
            # Create new invitation record
            new_invite = Invitation(
                invitee_email=invitee_email,
                invite_code=invite_code,
                user_id=user_id,
                nickname=nickname,
                created_at=datetime.now(timezone.utc),
                used=False,
            )
            session.add(new_invite)
            await session.commit()

            # Generate QR code and store it in Minio
            img_stream = generate_qr_code(invite_code)
            qr_data = store_qr_code_in_minio(user_id, nickname, invite_code, img_stream)

            # Set QR code URL in the invitation object
            new_invite.qr_code_url = qr_data["url"]
            session.add(new_invite)
            await session.commit()

            # Send invitation email
            await email_service.send_invite_email(new_invite)

            return new_invite
        except Exception as e:
            logger.error(f"Error creating invitation: {e}")
            return None

    @classmethod
    async def get_invitation_by_code(cls, session: AsyncSession, invite_code: str) -> Optional[Invitation]:
        """
        Retrieve an invitation by its unique invite code.
        :param session: Database session.
        :param invite_code: Unique invite code.
        :return: Invitation object or None.
        """
        query = select(Invitation).where(Invitation.invite_code == invite_code)
        result = await cls._execute_query(session, query)
        return result.scalars().first() if result else None

    @classmethod
    async def mark_invitation_as_used(cls, session: AsyncSession, invite_id: int) -> bool:
        """
        Mark an invitation as used and set the used_at timestamp.
        :param session: Database session.
        :param invite_id: ID of the invitation to mark as used.
        :return: True if successful, False otherwise.
        """
        try:
            query = (
                update(Invitation)
                .where(Invitation.id == invite_id)
                .values(used=True, used_at=datetime.now(timezone.utc))
                .execution_options(synchronize_session="fetch")
            )
            await cls._execute_query(session, query)
            return True
        except Exception as e:
            logger.error(f"Error marking invitation as used: {e}")
            return False

    @classmethod
    async def list_invitations_for_user(cls, session: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 10) -> List[Invitation]:
        """
        List all invitations created by a specific user.
        :param session: Database session.
        :param user_id: ID of the user.
        :param skip: Number of records to skip (pagination).
        :param limit: Maximum number of records to return (pagination).
        :return: List of Invitation objects.
        """
        query = select(Invitation).where(Invitation.user_id == user_id).offset(skip).limit(limit)
        result = await cls._execute_query(session, query)
        return result.scalars().all() if result else []

    @classmethod
    async def resend_invitation(cls, session: AsyncSession, invite_id: int, email_service: EmailService) -> bool:
        """
        Resend an existing invitation email.
        :param session: Database session.
        :param invite_id: ID of the invitation to resend.
        :param email_service: EmailService instance for sending emails.
        :return: True if successful, False otherwise.
        """
        invitation = await session.get(Invitation, invite_id)
        if not invitation:
            logger.error(f"Invitation with ID {invite_id} not found.")
            return False

        try:
            await email_service.send_invite_email(invitation)
            return True
        except Exception as e:
            logger.error(f"Error resending invitation: {e}")
            return False
