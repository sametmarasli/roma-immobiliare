from prefect.deployments import Deployment
from prefect.infrastructure import DockerContainer, Process
# from prefect_gcp.cloud_run import CloudRunJob
from prefect.filesystems import GCS, LocalFileSystem, GitHub
from src.immobiliare_data_ingestion import trigger_pipeline
from datetime import date

storage_block = LocalFileSystem.load('roma-storage-local')
infra_block = Process.load('roma-infra-local')
# storage_block = GitHub.load('roma-storage-github')
# infra_block = DockerContainer.load("roma-infra-docker")
# infra_block = CloudRunJob.load("roma-infra-cloudrun")

import os 
from dotenv import load_dotenv
# from dag import immobiliare_data_ingestion
load_dotenv(dotenv_path='config/.env.test')
# export $(cat config/.env.test|xargs)

ENV_NAME = os.environ['ENV_NAME']
GCS_BUCKET_NAME = os.environ['GCS_BUCKET_NAME']
GCP_SERVICE_ACCOUNT_PATH = os.environ['GCP_SERVICE_ACCOUNT_PATH']
PROJECT_ID = os.environ['PROJECT_ID']
REGION = os.environ['REGION']
BQ_RAW_DATASET_ID = os.environ['BQ_RAW_DATASET_ID']
BQ_RAW_TABLE_ID = os.environ['BQ_RAW_TABLE_ID']
BQ_DBT_DATASET_ID = os.environ['BQ_DBT_DATASET_ID']
BQ_RAW_SCHEMA = os.environ['BQ_RAW_SCHEMA']

deployment = Deployment.build_from_flow(
    flow=trigger_pipeline,
    name="deployment-infra-local-storage-local-trigger_pipeline",
    version=1,
    infrastructure=infra_block,
    storage=storage_block,
    work_queue_name="main",
    parameters={
            "ingestion_date": str(date.today()),
            "minimum_price": 200_000,
            "maxium_price": 204_000,
            "service_account": GCP_SERVICE_ACCOUNT_PATH,
            "project_id": PROJECT_ID,
            "location": REGION,
            "gcs_bucket_name": GCS_BUCKET_NAME,
            "dataset_id": BQ_RAW_DATASET_ID,
            "table_id": BQ_RAW_TABLE_ID,
            "bq_schema": BQ_RAW_SCHEMA,
        }
)
deployment.apply()