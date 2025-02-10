import boto3
import os

LOCAL_MODE = os.getenv("LOCAL_MODE", "false").lower() == "true"

# MinIO Configuration
MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "admin"  # Replace with your MinIO access key
MINIO_SECRET_KEY = "password"  # Replace with your MinIO secret key

if LOCAL_MODE:
    # Use MinIO as a local alternative to Google Cloud Storage
    s3_client = boto3.client(
        's3',
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        region_name="us-east-1"  # You can change the region if needed
    )

    # Specify your MinIO bucket name here
    bucket_name = "my-bucket"  # The bucket you created in MinIO WebUI
    
    # Upload file to MinIO bucket
    file_name = "your-file.txt"  # Replace with your file's name
    s3_client.upload_file(file_name, bucket_name, file_name)
    print(f"File {file_name} uploaded successfully to MinIO bucket {bucket_name}!")

else:
    # Use actual Google Cloud Storage for production
    from google.cloud import storage

    # Actual Google Cloud Storage logic
    storage_client = storage.Client()
    bucket = storage_client.bucket("your-gcs-bucket")

    # Upload file to GCS bucket
    blob = bucket.blob("your-file.txt")
    blob.upload_from_filename("your-file.txt")
    print("File uploaded successfully to GCS!")
