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

def generate_invite_code(user_id: int) -> str:
    invite_code = base64.urlsafe_b64encode(str(user_id).encode('utf-8')).decode('utf-8')
    return invite_code

def store_qr_code_in_minio(user_id: int, img_stream: BytesIO):
    invite_code = generate_invite_code(user_id)
    file_name = f"invite_{invite_code}.png"
    minio_client.put_object(
        bucket_name=os.getenv("MINIO_BUCKET"),
        object_name=file_name,
        data=img_stream,
        length=len(img_stream.getvalue())
    )
    return file_name