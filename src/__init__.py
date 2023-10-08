import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

LOCAL_PATH = os.getenv('LOCAL_PATH')
PROJECT_ID = os.getenv('PROJECT_ID')
REGION = os.getenv('REGION')
GCP_SERVICE_ACCOUNT_PATH = os.getenv('GCP_SERVICE_ACCOUNT_PATH')
# 
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
GCS_BUCKET_URI = os.getenv('GCS_BUCKET_URI')
#
BQ_DATASET_ID = os.getenv('BQ_DATASET_ID')
BQ_TABLE_ID = os.getenv('BQ_TABLE_ID')
BQ_SCHEMA = os.getenv('BQ_SCHEMA')
LOG_PATH = '../log.txt'