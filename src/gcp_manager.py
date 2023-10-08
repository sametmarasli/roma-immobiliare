import src.logger as log
from src.storage.gcs import StorageGCS
from src.storage.bigquery import StorageBigQuery


def setup_data_infrastructure(
        service_account,
        location,
        project_id,
        gcs_bucket_name,
        bq_raw_dataset_id,
        bq_dbt_dataset_id,
):
    log.info(f"Building components of data infrastructure")
    gcs = StorageGCS(service_account)
    bq = StorageBigQuery(service_account)
    log.info(f"Create bucket {gcs_bucket_name} for storing api calls")
    gcs.create_bucket(gcs_bucket_name, location)
    log.info(f"create dataset {bq_raw_dataset_id} to ingest raw data to BigQuery")
    bq.create_dataset(project_id, bq_raw_dataset_id, location)
    log.info(f"create dataset {bq_dbt_dataset_id} for transformed tables by dbt")
    bq.create_dataset(project_id, bq_dbt_dataset_id, location)


def teardown_data_infrastructure(
        service_account,
        project_id,
        gcs_bucket_name,
        bq_raw_dataset_id,
        bq_dbt_dataset_id,
):
    log.info(f"Removing components of data infrastructure")
    gcs = StorageGCS(service_account)
    bq = StorageBigQuery(service_account)
    log.info(f"Remove bucket {gcs_bucket_name} for storing api calls")
    gcs.delete_bucket(gcs_bucket_name, force=True)
    log.info(f"Remove dataset {bq_raw_dataset_id} to ingest raw data to BigQuery")
    bq.delete_dataset(project_id, bq_raw_dataset_id)
    log.info(f"Remove dataset {bq_dbt_dataset_id} for transformed tables by dbt")
    bq.delete_dataset(project_id, bq_dbt_dataset_id)

