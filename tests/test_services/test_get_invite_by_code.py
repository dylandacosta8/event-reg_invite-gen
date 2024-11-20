import pytest
from app.services.invite_service import InviteService

@pytest.mark.asyncio
async def test_get_invitation(db_session, verified_user, email_service):
    invitation = await InviteService.create_invitation(
        db_session,
        invitee_email="pytest@example.com",
        user_id=verified_user.id,
        nickname=verified_user.nickname,
        email_service=email_service
    )
    retrieved_invitation = await InviteService.get_invitation_by_code(db_session, invitation.invite_code)
    assert retrieved_invitation is not None
    assert retrieved_invitation.invite_code == invitation.invite_code