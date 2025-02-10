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

# Function to get the list of changed files (both staged and unstaged)
def get_changed_files():
    # Get unstaged changes (working directory vs. HEAD)
    changed_files = subprocess.check_output(["git", "diff", "--name-only", "HEAD"]).decode("utf-8").splitlines()
    
    # Get staged changes (index vs. HEAD)
    staged_files = subprocess.check_output(["git", "diff", "--name-only", "--cached", "HEAD"]).decode("utf-8").splitlines()
    
    # Combine unstaged and staged files
    return list(set(changed_files + staged_files))

# Get the list of changed files in the GitHub repository
try:
    changed_files = get_changed_files()
    
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
