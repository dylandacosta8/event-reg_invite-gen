import pytest
from app.services.invite_service import InviteService

@pytest.mark.asyncio
async def test_create_invitation(db_session, verified_user, email_service):
    # Simulate the verified user creating the invitation
    invitation = await InviteService.create_invitation(
        db_session,
        invitee_email="pytest@example.com",
        user_id=verified_user.id,
        nickname=verified_user.nickname,
        email_service=email_service
    )
    assert invitation is not None
