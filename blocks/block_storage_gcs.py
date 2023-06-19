from prefect.filesystems import GCS
from dotenv import load_dotenv
import os

load_dotenv()
BUCKET_NAME = os.getenv('BUCKET_NAME')
PROJECT_ID = os.getenv('PROJECT_ID')
PROJECT_ID = os.getenv('PROJECT_ID')
GCP_SERVICE_ACCOUNT_PATH = os.getenv('GCP_SERVICE_ACCOUNT_PATH')

with open(GCP_SERVICE_ACCOUNT_PATH) as f:
    service_account = f.read()

block = GCS(
    bucket_path=f"{BUCKET_NAME}/dev/",
    service_account_info=service_account,
    project=PROJECT_ID
)

block.save("roma-storage-gcs", overwrite=True)