from datetime import date
from prefect import flow, task
import src.logger as log
from src import pipeline_manager 
                
@task()
def bulk_call_api_and_extract_data_to_gcs(
    ingestion_date:str,
    minimum_price:int,
    maxium_price:int,
    gcs_bucket_name:str,
    service_account:str,
    ) -> None:
    pipeline_manager.bulk_call_api_and_extract_data_to_gcs(ingestion_date=ingestion_date, gcs_bucket_name=gcs_bucket_name,service_account=service_account,minimum_price=minimum_price,maxium_price=maxium_price)

@task()
def ingest_data_from_gcs_to_bq_by_date(
    ingestion_date :str,
    service_account :str,
    gcs_bucket_name :str,
    location :str,
    project_id :str,
    dataset_id :str,
    table_id :str,
    bq_schema :str,
    ) -> None:
    """
    Ingests data from Google Cloud Storage (GCS) to BigQuery (BQ) for a specific date.

    Args:
        ingestion_date (str): The date for data ingestion.
    """
    pipeline_manager.ingest_data_from_gcs_to_bq_by_date(ingestion_date=ingestion_date, service_account=service_account, gcs_bucket_name=gcs_bucket_name, location=location, project_id=project_id, dataset_id=dataset_id, table_id=table_id, bq_schema=bq_schema)

@task()
def run_dbt() -> None:
    """
    Runs a dbt (data build tool) job.
    """
    pipeline_manager.run_dbt()


@task()
def remove_temporary_raw_bigquery_table(
    service_account:str,
    project_id:str,
    dataset_id:str,
    table_id:str,
    ) -> None:
    pipeline_manager.remove_temporary_raw_bigquery_table(service_account=service_account, project_id=project_id, dataset_id=dataset_id, table_id=table_id)


@flow()
def trigger_pipeline(
    ingestion_date,
    minimum_price,
    maxium_price,
    service_account,
    project_id,
    location,
    gcs_bucket_name,
    dataset_id,
    table_id,
    bq_schema,) -> None:
    """
    Triggers a data pipeline for data extraction, ingestion, and transformation.

    Args:
        ingestion_date (str): The date for data ingestion.
        minimum_price (int): The minimum price filter.
        maxium_price (int): The maximum price filter.
    """
    log.info("Triggering pipeline")
    bulk_call_api_and_extract_data_to_gcs(ingestion_date=ingestion_date, gcs_bucket_name=gcs_bucket_name,service_account=service_account,minimum_price=minimum_price,maxium_price=maxium_price)
    ingest_data_from_gcs_to_bq_by_date(ingestion_date=ingestion_date, service_account=service_account, gcs_bucket_name=gcs_bucket_name, location=location, project_id=project_id, dataset_id=dataset_id, table_id=table_id, bq_schema=bq_schema)
    run_dbt()
    remove_temporary_raw_bigquery_table(service_account=service_account, project_id=project_id, dataset_id=dataset_id, table_id=table_id)

# if __name__ == '__main__':
#     log.info("Starting the main script")
#     import os 
#     from dotenv import load_dotenv

#     load_dotenv(dotenv_path='config/.env.test')

#     ENV_NAME = os.environ['ENV_NAME']
#     GCS_BUCKET_NAME = os.environ['GCS_BUCKET_NAME']
#     GCP_SERVICE_ACCOUNT_PATH = os.environ['GCP_SERVICE_ACCOUNT_PATH']
#     PROJECT_ID = os.environ['PROJECT_ID']
#     REGION = os.environ['REGION']
#     BQ_RAW_DATASET_ID = os.environ['BQ_RAW_DATASET_ID']
#     BQ_RAW_TABLE_ID = os.environ['BQ_RAW_TABLE_ID']
#     BQ_DBT_DATASET_ID = os.environ['BQ_DBT_DATASET_ID']
#     BQ_RAW_SCHEMA = os.environ['BQ_RAW_SCHEMA']


#     log.info(f"Environment: {ENV_NAME}")

#     trigger_pipeline(
#         ingestion_date=str(date.today()), 
#         minimum_price=200_000,
#         maxium_price=204_000,
#         service_account=GCP_SERVICE_ACCOUNT_PATH,
#         project_id=PROJECT_ID,
#         location=REGION,
#         gcs_bucket_name=GCS_BUCKET_NAME,
#         dataset_id=BQ_RAW_DATASET_ID,
#         table_id=BQ_RAW_TABLE_ID,
#         bq_schema=BQ_RAW_SCHEMA)
    
#     log.info("Script execution completed")















