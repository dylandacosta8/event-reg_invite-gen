import pytest
from app.services.invite_service import InviteService

@pytest.mark.asyncio
async def test_update_invitation(db_session, verified_user, email_service):
    invitation = await InviteService.create_invitation(
        db_session,
        invitee_email=f"pytest@example.com",
        user_id=verified_user.id,
        nickname=verified_user.nickname,
        email_service=email_service
        )
    updated_data = {"invitee_email": "test2@example.com"}
    updated_invitation = await InviteService.update_invite(db_session, invitation.id, verified_user.id, updated_data)
    assert updated_invitation.invitee_email == updated_data["invitee_email"]
