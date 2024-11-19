# email_service.py
from builtins import ValueError, dict, str
from settings.config import settings
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.models.user_model import User
from app.models.invite_model import Invitation
from base64 import urlsafe_b64encode

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        self.smtp_client = SMTPClient(
            server=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password
        )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type")

        html_content = self.template_manager.render_template(email_type, **user_data)
        self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])

    async def send_verification_email(self, user: User):
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        await self.send_user_email({
            "name": user.first_name,
            "verification_url": verification_url,
            "email": user.email
        }, 'email_verification')

    async def send_invite_email(self, invite: Invitation):
        """
        Sends an invitation email to the invitee with a QR code attached.
        :param invite: Invitation object containing the invite details.
        :return: None
        """
        try:
            # Generate the invite link URL
            base64_nickname = urlsafe_b64encode(invite.nickname.encode('utf-8')).decode('utf-8')
            invite_url = f"{settings.server_base_url}accept?nickname={base64_nickname}&invite_code={invite.invite_code}"

            # The URL for the QR code image already stored in Minio
            qr_code_url = f"http://localhost:9000/{settings.minio_bucket}/invite_{invite.invite_code}.png"
            print(qr_code_url)

            # Prepare the email content using the template
            user_data = {
                "name": invite.nickname,
                "qr_code_url": qr_code_url,  # Pass the QR code URL to the template
                "invite_url": invite_url,
                "email": invite.invitee_email
            }

            html_content = self.template_manager.render_template("invite_email", **user_data)

            # Send the email with the QR code as an embedded image
            self.smtp_client.send_email(
                subject="You're Invited to Join",
                html_content=html_content,
                recipient=invite.invitee_email
            )
            print(f"Invitation email sent to {invite.invitee_email}")
        except Exception as e:
            print(f"Error sending invite email: {e}")
            raise