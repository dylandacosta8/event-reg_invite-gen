from minio import Minio
from minio.error import S3Error
from settings.config import settings
import logging
import os

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Minio client using the configuration from settings
minio_client = Minio(
    settings.minio_url,
    access_key=os.environ.get("MINIO_ROOT_USER"),
    secret_key=os.environ.get("MINIO_ROOT_PASSWORD"),
    secure=False
)

def create_minio_bucket():
    
    # Define the bucket name from settings
    bucket_name = settings.minio_bucket

    policy = """
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::qr-codes/*"
            ]
        }
    ]
}
"""
    
    try:
        # Check if the bucket already exists
        if not minio_client.bucket_exists(bucket_name):
            # If the bucket does not exist, create it
            minio_client.make_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' created successfully!")
            minio_client.set_bucket_policy(bucket_name, policy)
        else:
            logger.info(f"Bucket '{bucket_name}' already exists.")
            minio_client.set_bucket_policy(bucket_name, policy)
    
    except S3Error as e:
        logger.error(f"Error creating bucket: {e}")
        raise Exception(f"Error creating Minio bucket: {e}")

# This will be executed only if the script is run directly
if __name__ == "__main__":
    create_minio_bucket()
