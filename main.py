from datetime import date
from prefect import flow, task
import logging

from src import (
                bulk_call_api_and_extract_data_to_gcs,
                ingest_data_from_gcs_to_bq_by_date,
                run_dbt
                )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@task()
def task_bulk_call_api_and_extract_data_to_gcs(ingestion_date: str, minimum_price: int, maxium_price: int) -> None:
    """
    Calls an API and extracts data to Google Cloud Storage (GCS).

    Args:
        ingestion_date (str): The date for data ingestion.
        minimum_price (int): The minimum price filter.
        maxium_price (int): The maximum price filter.
    """
    logger.info("Running task_bulk_call_api_and_extract_data_to_gcs")
    bulk_call_api_and_extract_data_to_gcs(ingestion_date, minimum_price, maxium_price)

@task()
def task_ingest_data_from_gcs_to_bq_by_date(ingestion_date: str) -> None:
    """
    Ingests data from Google Cloud Storage (GCS) to BigQuery (BQ) for a specific date.

    Args:
        ingestion_date (str): The date for data ingestion.
    """
    logger.info("Running task_ingest_data_from_gcs_to_bq_by_date")
    ingest_data_from_gcs_to_bq_by_date(ingestion_date)

@task()
def task_run_dbt() -> None:
    """
    Runs a dbt (data build tool) job.
    """
    logger.info("Running task_run_dbt")
    run_dbt()

@flow()
def trigger_pipeline(ingestion_date: str, minimum_price: int, maxium_price: int) -> None:
    """
    Triggers a data pipeline for data extraction, ingestion, and transformation.

    Args:
        ingestion_date (str): The date for data ingestion.
        minimum_price (int): The minimum price filter.
        maxium_price (int): The maximum price filter.
    """
    logger.info("Triggering pipeline")
    task_bulk_call_api_and_extract_data_to_gcs(ingestion_date, minimum_price, maxium_price)
    task_ingest_data_from_gcs_to_bq_by_date(ingestion_date)
    task_run_dbt()

if __name__ == '__main__':
    logger.info("Starting the main script")
    trigger_pipeline(ingestion_date=str(date.today()), minimum_price=390_000, maxium_price=400_000)
    logger.info("Script execution completed")