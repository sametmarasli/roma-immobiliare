from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from dotenv import load_dotenv
import os

load_dotenv()
BUCKET_NAME = os.getenv('BUCKET_NAME')

bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("roma-gcp-credentials"),
    bucket=BUCKET_NAME,  # insert your  GCS bucket name
)

bucket_block.save("roma-gcs", overwrite=True)