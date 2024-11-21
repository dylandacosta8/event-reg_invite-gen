import pytest
from minio.error import S3Error
from app.services.invite_service import InviteService
import uuid


@pytest.mark.asyncio
async def test_qr_code_stored_in_minio(db_session, minio_client, verified_user, email_service):
    """
    Test if the QR code is successfully stored in MinIO after creating an invitation.
    """
    bucket_name = 'qr-codes'

    # Create an invitation
    invitation = await InviteService.create_invitation(
        db_session,
        invitee_email="pytest@example.com",
        user_id=verified_user.id,
        nickname=verified_user.nickname,
        email_service=email_service,
    )

    assert invitation is not None, "Invitation creation failed."

    # Extract QR code URL from the created invitation
    qr_code_url = invitation.qr_code_url
    assert qr_code_url is not None, "QR code URL is not set in the invitation."

    # Extract the object name from the URL (e.g., "user_id/nickname/invite_code.png")
    object_name = qr_code_url.split(bucket_name + "/")[-1]

    # Verify the QR code is stored in MinIO
    try:
        # Check if the object exists in the specified bucket
        obj = minio_client.stat_object(bucket_name, object_name)
        assert obj is not None, f"QR code not found in MinIO bucket '{bucket_name}' with object name '{object_name}'."
    except S3Error as e:
        pytest.fail(f"MinIO object lookup failed: {e}")
