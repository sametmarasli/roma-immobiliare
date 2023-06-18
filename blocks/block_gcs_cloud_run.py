from prefect_gcp.cloud_run import CloudRunJob
from prefect_gcp import GcpCredentials
from dotenv import load_dotenv
import os

load_dotenv()
PROJECT_ID = os.getenv('PROJECT_ID')
REGION = os.getenv('REGION')
DOCKER_IMAGE_NAME = os.getenv('DOCKER_IMAGE_NAME')
print(DOCKER_IMAGE_NAME)

credentials = GcpCredentials.load("roma-gcp-credentials")

block = CloudRunJob(
    credentials=credentials,
    project=PROJECT_ID,
    image=DOCKER_IMAGE_NAME,
    region=REGION
)

block.save("roma-cloud-run")