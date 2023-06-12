from prefect_gcp import GcpCredentials
from dotenv import load_dotenv
import os

load_dotenv()
PROJECT_ID = os.getenv('PROJECT_ID')
SERVICE_ACCOUNT = os.getenv('SERVICE_ACCOUNT')

with open(SERVICE_ACCOUNT) as f:
    service_account = f.read()

block = GcpCredentials(
    service_account_info=service_account,
    project=PROJECT_ID
)

block.save("roma-gcp-credentials", overwrite=True)