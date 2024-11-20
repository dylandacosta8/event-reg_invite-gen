import pytest
from app.services.invite_service import InviteService
import uuid

@pytest.mark.asyncio
async def test_delete_invite_success(db_session, verified_user, email_service):
    invitation = await InviteService.create_invitation(
        db_session,
        invitee_email=f"pytest@example.com",
        user_id=verified_user.id,
        nickname=verified_user.nickname,
        email_service=email_service
        )
    deleted = await InviteService.delete_invitation(db_session, invitation.id, verified_user.id)
    assert deleted is True

@pytest.mark.asyncio
async def test_delete_invite_failure(db_session, verified_user, email_service):
    invitation = await InviteService.create_invitation(
        db_session,
        invitee_email=f"pytest@example.com",
        user_id=verified_user.id,
        nickname=verified_user.nickname,
        email_service=email_service
        )
    deleted = await InviteService.delete_invitation(db_session, invitation.id, uuid.uuid4())
    assert deleted is False