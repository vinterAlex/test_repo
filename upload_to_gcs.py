import os
import subprocess
import boto3

# MinIO Configuration
MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "admin"  # Replace with your MinIO access key
MINIO_SECRET_KEY = "password"  # Replace with your MinIO secret key
bucket_name = "my-bucket"  # MinIO bucket name

# Initialize the MinIO client (boto3)
s3_client = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1"  # Region for MinIO
)

# Get the list of changed files in the GitHub repository
try:
    # Check if there are at least 2 commits (otherwise HEAD~1 won't work)
    result = subprocess.check_output(["git", "rev-list", "--count", "HEAD"])
    commit_count = int(result.decode("utf-8").strip())
    
    if commit_count < 2:
        print("Not enough commits to compare with HEAD~1, skipping file upload.")
    else:
        changed_files = subprocess.check_output(["git", "diff", "--name-only", "HEAD~1", "HEAD"]).decode("utf-8").splitlines()
        
        if not changed_files:
            print("No changed files detected.")
        else:
            for file in changed_files:
                if os.path.isfile(file):  # Ensure it's a valid file (not a directory)
                    print(f"Uploading file: {file}")
                    try:
                        s3_client.upload_file(file, bucket_name, file)
                        print(f"File {file} uploaded successfully to MinIO.")
                    except Exception as e:
                        print(f"Error uploading file {file}: {e}")
except subprocess.CalledProcessError as e:
    print(f"Error executing git command: {e}")
