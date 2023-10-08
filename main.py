import src.logger as log
from src import pipeline_manager 
from src import gcp_manager
from datetime import date
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


if __name__ ==  "__main__": 
    log.info(f"Environment: {ENV_NAME}")

    # gcp_manager.teardown_data_infrastructure(  
    #     service_account=GCP_SERVICE_ACCOUNT_PATH,
    #     project_id=PROJECT_ID,
    #     gcs_bucket_name=GCS_BUCKET_NAME,
    #     bq_raw_dataset_id=BQ_RAW_DATASET_ID,
    #     bq_dbt_dataset_id=BQ_DBT_DATASET_ID
    #     )

    # gcp_manager.setup_data_infrastructure( 
    #     service_account=GCP_SERVICE_ACCOUNT_PATH,
    #     location=REGION,
    #     project_id=PROJECT_ID,
    #     gcs_bucket_name=GCS_BUCKET_NAME,
    #     bq_raw_dataset_id=BQ_RAW_DATASET_ID,
    #     bq_dbt_dataset_id=BQ_DBT_DATASET_ID
    #     )

    # immobiliare_data_ingestion.trigger_pipeline(
    #     ingestion_date=str(date.today()), 
    #     minimum_price=200_000,
    #     maxium_price=222_000,
    #     service_account=GCP_SERVICE_ACCOUNT_PATH,
    #     project_id=PROJECT_ID,
    #     location=REGION,
    #     gcs_bucket_name=GCS_BUCKET_NAME,
    #     dataset_id=BQ_RAW_DATASET_ID,
    #     table_id=BQ_RAW_TABLE_ID,
    #     bq_schema=BQ_RAW_SCHEMA
    #     )
    
    
    # pipeline_manager.bulk_call_api_and_extract_data_to_gcs(
    #                     gcs_bucket_name=GCS_BUCKET_NAME,
    #                     service_account=GCP_SERVICE_ACCOUNT_PATH,
    #                     ingestion_date=str(date.today()),
    #                     minimum_price=220_000,
    #                     maxium_price= 222_000
    #                     )



    pipeline_manager.ingest_data_from_gcs_to_bq_by_date(
            ingestion_date='2023-10-05',
            service_account=GCP_SERVICE_ACCOUNT_PATH,
            gcs_bucket_name=GCS_BUCKET_NAME,
            location=REGION,
            project_id=PROJECT_ID,
            dataset_id=BQ_RAW_DATASET_ID,
            table_id=BQ_RAW_TABLE_ID,
            bq_schema=BQ_RAW_SCHEMA,
            )



    pipeline_manager.run_dbt()

    # pipeline_manager.remove_temporary_raw_bigquery_table(
    #     service_account=GCP_SERVICE_ACCOUNT_PATH,
    #     project_id=PROJECT_ID,
    #     dataset_id=BQ_RAW_DATASET_ID,
    #     table_id=BQ_RAW_TABLE_ID
    # )