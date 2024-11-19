import qrcode
from base64 import urlsafe_b64encode
from io import BytesIO
from app.minio_setup import minio_client
from settings.config import settings

def generate_qr_code(data: str) -> BytesIO:
    """
    Generates a QR code as a PNG image.
    """
    qr = qrcode.make(data)
    img_stream = BytesIO()
    qr.save(img_stream, 'PNG')
    img_stream.seek(0)
    return img_stream

def generate_qr_data(nickname: str, invite_code: str) -> str:
    """
    Generates the URL that the QR code should point to. The URL includes the base64-encoded nickname and invite code.
    """
    base64_nickname = urlsafe_b64encode(nickname.encode('utf-8')).decode('utf-8')
    redirect_url = f"{settings.server_base_url}accept?nickname={base64_nickname}&invite_code={invite_code}"
    return redirect_url

def store_qr_code_in_minio(user_id: int, nickname: str, invite_code: str, img_stream: BytesIO):
    """
    Stores the generated QR code in Minio and returns the file URL.
    """
    try:
        file_name = f"invite_{invite_code}.png"
        bucket_name = settings.minio_bucket
        if not bucket_name:
            raise ValueError("MINIO_BUCKET is not set.")

        qr_data = generate_qr_data(nickname, invite_code)

        img_stream = generate_qr_code(qr_data)

        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=file_name,
            data=img_stream,
            length=len(img_stream.getvalue())
        )

        return {
            "file_name": file_name,
            "url": f"http://localhost:9000/{bucket_name}/{file_name}"
        }
    except Exception as e:
        print(f"Error storing QR code in Minio: {e}")
        raise
