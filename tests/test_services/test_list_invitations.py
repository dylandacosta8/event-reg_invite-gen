import pytest
from app.services.invite_service import InviteService

@pytest.mark.asyncio
async def test_get_invitations_paginated(db_session, verified_user, email_service):
    for i in range(0,5):
        invitation = await InviteService.create_invitation(
        db_session,
        invitee_email=f"pytest{i}@example.com",
        user_id=verified_user.id,
        nickname=verified_user.nickname,
        email_service=email_service
        )
    invites, total = await InviteService.list_invitations_for_user(db_session, verified_user.id, skip=0, limit=10)
    assert len(invites) == 5