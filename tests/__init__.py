from dotenv import load_dotenv
from pathlib import Path
import os 

load_dotenv('./config/.env.test')

ENVNAME = os.getenv('ENVNAME')
print(ENVNAME)
PROJECT_ID = os.getenv('PROJECT_ID')
BQ_DATASET_ID = os.getenv('BQ_DATASET_ID')
BQ_DATASET_TEST_DBT = os.getenv('BQ_DATASET_TEST_DBT')
BQ_TABLE_ID = os.getenv('BQ_TABLE_ID')
BQ_TABLE_ID_TEST_DBT = os.getenv('BQ_TABLE_ID_TEST_DBT')
BQ_SCHEMA = os.getenv('BQ_SCHEMA')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
GCS_BUCKET_URI = os.getenv('GCS_BUCKET_URI')
GCP_SERVICE_ACCOUNT_PATH = os.getenv('GCP_SERVICE_ACCOUNT_PATH')
REGION = os.getenv('REGION')