from google.cloud import storage
import os
from google.auth import exceptions

LOCAL_MODE = os.getenv("LOCAL_MODE", "false").lower() == "true"

# MinIO Configuration
MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "admin"  # Replace with your MinIO access key
MINIO_SECRET_KEY = "password"  # Replace with your MinIO secret key

if LOCAL_MODE:
    # Use MinIO as a local alternative to Google Cloud Storage
    storage_client = storage.Client(
        credentials=None,  # MinIO does not need Google credentials
        project="local-project",  # Placeholder project
        _http=None  # We’ll manually configure the API URL
    )
    
    # Manually set the endpoint for MinIO (this simulates Google Cloud Storage)
    storage_client._http = storage_client._http.with_options(
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )
    
    # Specify your MinIO bucket name here
    bucket_name = "my-bucket"  # The bucket you created in MinIO WebUI
    bucket = storage_client.bucket(bucket_name)

else:
    # Use actual Google Cloud Storage (for production)
    storage_client = storage.Client()
    bucket = storage_client.bucket("my-bucket")

# Upload file to MinIO or GCS bucket
blob = bucket.blob("your-file.txt")
blob.upload_from_filename("your-file.txt")

print("File uploaded successfully!")
