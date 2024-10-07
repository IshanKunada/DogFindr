import os
import boto3
from dotenv import load_dotenv

load_dotenv() 

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key'),
    region_name='us-east-2'
)

BUCKET_NAME = 'dogfindr'

# List objects in your S3 bucket
objects = s3.list_objects_v2(Bucket=BUCKET_NAME)['Contents']

# Generate pre-signed URLs or use the S3 URLs directly
image_urls = {
  obj['Key']: s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': obj['Key']}) for obj in objects
}