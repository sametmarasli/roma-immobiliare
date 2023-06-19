from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from dotenv import load_dotenv
import os

load_dotenv()
BUCKET_NAME = os.getenv('BUCKET_NAME')

block = GcsBucket(
    gcp_credentials=GcpCredentials.load("roma-credentials-gcp"),
    bucket=BUCKET_NAME,
)

block.save("roma-filesystem-gcs", overwrite=True)