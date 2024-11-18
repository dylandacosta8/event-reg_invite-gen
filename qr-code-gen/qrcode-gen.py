import qrcode
import base64
import os
from io import BytesIO
from app.minio_setup import minio_client

def generate_qr_code(data: str) -> BytesIO:
    qr = qrcode.make(data)
    img_stream = BytesIO()
    qr.save(img_stream, 'PNG')
    img_stream.seek(0)
    return img_stream

def generate_invite_code(user_id: int, nickname: str) -> str:
    data = f"{user_id}:{nickname}"
    invite_code = base64.urlsafe_b64encode(data.encode('utf-8')).decode('utf-8')
    return invite_code

def store_qr_code_in_minio(user_id: int, nickname: str, img_stream: BytesIO):
    try:
        invite_code = generate_invite_code(user_id, nickname)
        file_name = f"invite_{invite_code}.png"
        bucket_name = os.getenv("MINIO_BUCKET")
        if not bucket_name:
            raise ValueError("MINIO_BUCKET is not set.")
        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=file_name,
            data=img_stream,
            length=len(img_stream.getvalue())
        )
        return {
            "file_name": file_name,
            "url": f"{os.getenv('MINIO_URL')}/{bucket_name}/{file_name}"
        }
    except Exception as e:
        print(f"Error storing QR code in Minio: {e}")
        raise