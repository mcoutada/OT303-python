import boto3
 
 
def uploader_txt_s3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS,s3_output_key,bucket_name, input_file_path):
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS)
    s3 = session.resource('s3')
    # Filename - File to upload
    # Bucket - Bucket to upload to (the top level directory under AWS S3)
    # Key - S3 object name (can contain subdirectories). If not specified then file_name is used
    s3.meta.client.upload_file(Filename=input_file_path, Bucket=bucket_name, Key=s3_output_key)

# VIA https://stackoverflow.com/a/54595494
