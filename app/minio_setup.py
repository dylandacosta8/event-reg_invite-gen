from minio import Minio
from minio.error import S3Error
from settings.config import settings
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Minio client using the configuration from settings
minio_client = Minio(
    settings.minio_url,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=False  # Set to True if using HTTPS
)

def create_minio_bucket():
    
    # Define the bucket name from settings
    bucket_name = settings.minio_bucket
    
    try:
        # Check if the bucket already exists
        if not minio_client.bucket_exists(bucket_name):
            # If the bucket does not exist, create it
            minio_client.make_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' created successfully!")
        else:
            logger.info(f"Bucket '{bucket_name}' already exists.")
    
    except S3Error as e:
        logger.error(f"Error creating bucket: {e}")
        raise Exception(f"Error creating Minio bucket: {e}")

# This will be executed only if the script is run directly
if __name__ == "__main__":
    create_minio_bucket()
