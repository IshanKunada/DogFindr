import boto3

BUCKET_NAME = 'dogfindr' # replace with your bucket name
KEY = '1' # replace with your object key

s3 = boto3.resource('s3')

try:
    s3.Bucket(BUCKET_NAME).download_file(KEY, 'my_local_image.jpg')
except:
    print("Error occurred.")