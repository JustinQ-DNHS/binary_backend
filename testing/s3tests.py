import boto3

# vars
bucket_name = 'kasmv2-bucket'
local_file_path = '/Users/rachitjaiswal/Desktop/Github/kasmv2_flask/testing/testuserdata.txt'
s3_file_path = 'users/rachit/testuserdata.txt'  # This is where you specify the location in S3
directory = 'users/rachit/'
local_file_path = '/Users/rachitjaiswal/Desktop/Github/kasmv2_flask/testing/testuserdata.txt'  # Path to save on your local machine



# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-east-2'
)

def list_buckets():
    response = s3_client.list_buckets()
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')

# list_buckets()

def upload_file(file_name, bucket, s3_file_path):
    try:
        s3_client.upload_file(file_name, bucket, s3_file_path)
        print(f'File {file_name} uploaded to {bucket}/{s3_file_path}')
    except Exception as e:
        print(f'Error: {e}')

# Usage
# upload_file(local_file_path, bucket_name, s3_file_path)

def list_objects_in_directory(bucket, directory):
    if not directory.endswith('/'):
        directory += '/'
    
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket, Prefix=directory)
        
        print(f'Objects in directory "{directory}":')
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    print(f'  {obj["Key"]}')
            else:
                print('Directory is empty or does not exist.')
    except Exception as e:
        print(f'Error: {e}')
# Usage
# list_objects_in_directory(bucket_name, directory)

def download_file(bucket, s3_file_path, local_file_path):
    try:
        s3_client.download_file(bucket, s3_file_path, local_file_path)
        print(f'File {s3_file_path} downloaded to {local_file_path}')
    except Exception as e:
        print(f'Error: {e}')

# Usage
download_file(bucket_name, s3_file_path, local_file_path)