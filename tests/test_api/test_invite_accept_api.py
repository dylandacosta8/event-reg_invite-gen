import pytest
from base64 import urlsafe_b64encode
from app.services.invite_service import InviteService
from settings.config import settings


@pytest.mark.asyncio
async def test_accept_invite_endpoint(async_client, db_session, verified_user, email_service):
    """
    Test the /accept endpoint to ensure it validates the invite and redirects correctly.
    """
    # Create an invitation for testing
    nickname = "test_nickname"
    encoded_nickname = urlsafe_b64encode(nickname.encode("utf-8")).decode("utf-8")
    invite_code = "test-invite-code"

    invitation = await InviteService.create_invitation(
        session=db_session,
        invitee_email="pytest@example.com",
        user_id=verified_user.id,
        nickname=nickname,
        email_service=email_service,
    )
    invitation.invite_code = invite_code
    await db_session.commit()

    # Call the /accept endpoint with the valid parameters
    response = await async_client.get(
        f"/accept?nickname={encoded_nickname}&invite_code={invitation.invite_code}"
    )

    # Assertions
    assert response.status_code == 307  # Redirect
    assert "location" in response.headers  # Redirect URL should be present
    assert response.headers["location"] == "settings.redirect_base_url"

    # Verify the invitation is marked as used
    used_invitation = await InviteService.get_invitation_by_code(db_session, invitation.invite_code)
    assert used_invitation.used is True
    assert used_invitation.used_at is not None


@pytest.mark.asyncio
async def test_accept_invite_invalid_code(async_client):
    """
    Test the /accept endpoint with an invalid invite code to ensure it returns an error.
    """
    # Use a fake invite code and nickname
    fake_invite_code = "invalid-code"
    fake_nickname = urlsafe_b64encode("invalid-nickname".encode("utf-8")).decode("utf-8")

    response = await async_client.get(
        f"/accept?nickname={fake_nickname}&invite_code={fake_invite_code}"
    )

    # Assertions
    assert response.status_code == 400  # Bad Request
    assert response.json()["detail"] == "Error processing invitation: 400: Invalid or expired invite code."
