import pytest
from app.services.invite_service import InviteService
import uuid

@pytest.mark.asyncio
async def test_accept_invitation(db_session, verified_user, email_service):
    invitation = await InviteService.create_invitation(
        db_session,
        invitee_email="pytest@example.com",
        user_id=verified_user.id,
        nickname=verified_user.nickname,
        email_service=email_service,
    )
    marked = await InviteService.mark_invitation_as_used(db_session, invitation.id)
    assert marked is True