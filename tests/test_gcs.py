from src.storage.gcs import StorageGCS
from src.storage.local import StorageLocal
from src.api.pagination import ApiPagination
from src.models import ApiParameters
import tests

import pytest
import json 

@pytest.fixture
def delete_gcs_bucket():
    print('LOG: Setup ...')
    gcs = StorageGCS(tests.GCP_SERVICE_ACCOUNT_PATH)
    yield 
    print('LOG: Teardown...')
    gcs.delete_bucket(bucket_name=tests.GCS_BUCKET_NAME, force=True)

@pytest.fixture
def setup_gcs_bucket():
    print('LOG: Setup ...')
    gcs = StorageGCS(tests.GCP_SERVICE_ACCOUNT_PATH)
    try: 
        gcs.create_bucket(bucket_name=tests.GCS_BUCKET_NAME, location=tests.REGION)
    except:
        print('Bucket already exists')
        pass
    yield 
    print('LOG: Teardown...')
    gcs.delete_bucket(bucket_name=tests.GCS_BUCKET_NAME, force=True)

@pytest.fixture
def setup_data_on_memory():
    print('LOG: Setup ...')
    parameters = ApiParameters(prezzoMinimo=100_000,prezzoMassimo=100_050)
    api = ApiPagination()
    json_results, json_file_name = api.serialize_paginated_results(parameters)
    yield json_results, json_file_name
    print('LOG: Teardown...')
    

def test_create_bucket(delete_gcs_bucket):
    '''test creating a new bucket
    '''
    print('LOG: Creating a new bucked named: ',tests.GCS_BUCKET_NAME)
    print(tests.GCP_SERVICE_ACCOUNT_PATH)
    gcs = StorageGCS(tests.GCP_SERVICE_ACCOUNT_PATH)
    gcs.create_bucket(bucket_name=tests.GCS_BUCKET_NAME, location=tests.REGION)
    print('LOG: check if the bucket is in the list of created buckets')
    buckets_list = gcs.list_buckets()
    assert tests.GCS_BUCKET_NAME in buckets_list


def test_upload_blob_from_memory(setup_gcs_bucket, setup_data_on_memory):
    '''test ingesting data from memory to a bucket
    '''
    gcs = StorageGCS(tests.GCP_SERVICE_ACCOUNT_PATH)
    gcs.upload_blob_from_memory(
        bucket_name=tests.GCS_BUCKET_NAME,
        contents=setup_data_on_memory[0],
        destination_blob_name=f'test/{setup_data_on_memory[1]}')
    
    print('LOG: data is ingested from memory to bucket')
    