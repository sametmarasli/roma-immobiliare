from src.storage.bigquery import StorageBigQuery
from src.storage.gcs import StorageGCS
from src.storage.local import StorageLocal
from src.api.pagination import ApiPagination
from src.models import ApiParameters

from pathlib import Path
import os 
import pytest 
import tests


@pytest.fixture
def setup_gcs_bucket():
    print('LOG: Setup ... setup_gcs_bucket')
    gcs = StorageGCS(tests.GCP_SERVICE_ACCOUNT_PATH)
    api = ApiPagination()
    try:
        gcs.delete_bucket(bucket_name=tests.GCS_BUCKET_NAME, force=True)
    except: 
        pass
    gcs.create_bucket(bucket_name=tests.GCS_BUCKET_NAME, location=tests.REGION)

    parameters = ApiParameters(prezzoMinimo=100_000,prezzoMassimo=100_050)
    json_results, json_file_name = api.serialize_paginated_results(parameters)
    gcs.upload_blob_from_memory(
        bucket_name=tests.GCS_BUCKET_NAME,
        contents=json_results,
        destination_blob_name=f'test_bq/{json_file_name}')

    yield 
    print('LOG: Teardown... setup_gcs_bucket')
    gcs.delete_bucket(bucket_name=tests.GCS_BUCKET_NAME, force=True)

@pytest.fixture
def setup_bq_dataset_and_table():
    print('LOG: Setup ... setup_bq_dataset_and_table')
    big_query = StorageBigQuery(tests.GCP_SERVICE_ACCOUNT_PATH)
    big_query.create_dataset(
        project_id=tests.PROJECT_ID,
        dataset_id=tests.BQ_DATASET_ID_TEST,
        location=tests.REGION)
    big_query.create_table(
        project_id=tests.PROJECT_ID,
        dataset_id=tests.BQ_DATASET_ID_TEST,
        table_id=tests.BQ_TABLE_ID_TEST,
        bq_schema=tests.BQ_SCHEMA)
    yield
    print('LOG: Teardown... setup_bq_dataset_and_table')
    big_query.delete_table(
        project_id=tests.PROJECT_ID,
        dataset_id=tests.BQ_DATASET_ID_TEST,
        table_id=tests.BQ_TABLE_ID_TEST,)
    big_query.delete_dataset(
        project_id=tests.PROJECT_ID,
        dataset_id=tests.BQ_DATASET_ID_TEST,)



def test_ingest_json_from_gcs_to_bq(setup_bq_dataset_and_table,setup_gcs_bucket):
    ''' 
    Test if the data can be ingested from gcs to bq with the provided static schema
    '''
    big_query = StorageBigQuery(tests.GCP_SERVICE_ACCOUNT_PATH)
    big_query.ingest_data_to_bigquery_from_gcs(
                                project_id = tests.PROJECT_ID,
                                dataset_id = tests.BQ_DATASET_ID_TEST, 
                                table_id = tests.BQ_TABLE_ID_TEST,
                                gcs_bucket_name = tests.GCS_BUCKET_NAME, 
                                blob_path = 'test_bq/*', 
                                bq_schema = tests.BQ_SCHEMA,
                                location=tests.REGION
                                )
    print('data_ingested')

    