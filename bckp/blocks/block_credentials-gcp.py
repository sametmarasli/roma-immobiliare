from prefect_gcp import GcpCredentials
from dotenv import load_dotenv
import os

load_dotenv()
PROJECT_ID = os.getenv('PROJECT_ID')
GCP_SERVICE_ACCOUNT_PATH = os.getenv('GCP_SERVICE_ACCOUNT_PATH')

with open(GCP_SERVICE_ACCOUNT_PATH) as f:
    service_account = f.read()

block = GcpCredentials(
    service_account_info=service_account,
    project=PROJECT_ID
)

block.save("roma-credentials-gcp", overwrite=True)