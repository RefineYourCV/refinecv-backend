import boto3
from core.config import settings
from botocore.exceptions import BotoCoreError, ClientError
import mimetypes


S3_REGION=settings.S3_REGION
S3_ACCESS_KEY_ID=settings.S3_ACCESS_KEY_ID
S3_SECRET_ACCESS_KEY=settings.S3_SECRET_ACCESS_KEY
S3_BUCKET_NAME=settings.S3_BUCKET_NAME

class S3Storage:
    def __init__(self):
        self.bucket_name = S3_BUCKET_NAME
        self.client = boto3.client(
            's3',
            region_name=S3_REGION,
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY
        )
    
    def put_object(self, user_id, content_type, file_name):
        try:
            extension = mimetypes.guess_extension(content_type) or ''
            print("extension",extension)
            key = f"user-uploads/{user_id}/{file_name}{extension}"
            params = {
                'Bucket': self.bucket_name,
                'Key': key,
                'ContentType': content_type
            }
            url = self.client.generate_presigned_url(
                'put_object',
                Params=params,
                ExpiresIn=3600
            )
            return url
        except (BotoCoreError, ClientError) as e:
            print(f"Error generating put presigned URL: {e}")
            raise

    def get_object_url(self, file_name):
        try:
            params = {
                'Bucket': self.bucket_name,
                'Key': file_name  # user-uploads/user_id/slug.content_type
            }
            url = self.client.generate_presigned_url(
                'get_object',
                Params=params,
                ExpiresIn=3600
            )
            return url
        except (BotoCoreError, ClientError) as e:
            print(f"Error generating get presigned URL: {e}")
            raise

    def delete_object(self, file_name):
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
        except (BotoCoreError, ClientError) as e:
            print(f"Error deleting object: {e}")
            raise