import numpy as np
from tqdm import tqdm
import os

from src.api.pagination import ApiPagination
from src.models import ApiParameters
from src.storage.gcs import StorageGCS
from src.storage.bigquery import StorageBigQuery
from dbt.cli.main import dbtRunner, dbtRunnerResult

# from dotenv import load_dotenv
# load_dotenv(dotenv_path='./config/.env.test')

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


def setup_gcs_bucket():
    assert GCS_BUCKET_NAME, 'Cannot setup bucket without id, check env variables'
    print(f'LOG: Creating bucket :{GCS_BUCKET_NAME}')
    gcs = StorageGCS(GCP_SERVICE_ACCOUNT_PATH)
    try: 
        gcs.create_bucket(bucket_name=GCS_BUCKET_NAME, location=REGION)
    except:
        print('LOG: Bucket already exists')
        pass

def remove_gcs_bucket():
    print(f'LOG: Deleting bucket {GCS_BUCKET_NAME}')
    gcs = StorageGCS(GCP_SERVICE_ACCOUNT_PATH)
    gcs.delete_bucket(bucket_name=GCS_BUCKET_NAME, force=True)


def setup_bq_dataset_and_table():
    assert BQ_DATASET_ID, 'Cannot setup dataset without id, check env variables'
    assert BQ_TABLE_ID, 'Cannot setup table without id, check env variables'
    big_query = StorageBigQuery(GCP_SERVICE_ACCOUNT_PATH)
    print(f'LOG: Setup ... BQ Dataset: {BQ_DATASET_ID}')
    big_query.create_dataset(
        project_id=PROJECT_ID,
        dataset_id=BQ_DATASET_ID,
        location=REGION)
    print(f'LOG: Setup ... BQ Table: {BQ_TABLE_ID}')
    big_query.create_table(
        project_id=PROJECT_ID,
        dataset_id=BQ_DATASET_ID,
        table_id=BQ_TABLE_ID,
        bq_schema=BQ_SCHEMA)
    

def remove_bq_dataset_and_table():
    assert BQ_DATASET_ID, 'Cannot delete dataset without id, check env variables'
    assert BQ_TABLE_ID, 'Cannot delete table without id, check env variables'
    big_query = StorageBigQuery(GCP_SERVICE_ACCOUNT_PATH)
    print(f'LOG: Deleting ... BQ Table {BQ_TABLE_ID}')
    big_query.delete_table(
        project_id=PROJECT_ID,
        dataset_id=BQ_DATASET_ID,
        table_id=BQ_TABLE_ID,)
    print(f'LOG: Deleting ... BQ Dataset {BQ_DATASET_ID}')
    big_query.delete_dataset(
        project_id=PROJECT_ID,
        dataset_id=BQ_DATASET_ID,)
    

def single_call_api_and_extract_data_to_gcs(ingestion_date, prezzoMinimo, prezzoMassimo):
    gcs = StorageGCS(GCP_SERVICE_ACCOUNT_PATH)
    api = ApiPagination()
    parameters = ApiParameters(prezzoMinimo=prezzoMinimo,prezzoMassimo=prezzoMassimo)
    print(f'LOG: Calling the api with price range {prezzoMinimo}-{prezzoMassimo}')
    json_results, json_file_name = api.serialize_paginated_results(parameters)
    print(f'LOG: Upload data {json_file_name} to gcs bucket {GCS_BUCKET_NAME}')
    gcs.upload_blob_from_memory(bucket_name=GCS_BUCKET_NAME,
                                contents=json_results,
                                destination_blob_name=f'{ingestion_date}/{json_file_name}')

def bulk_call_api_and_extract_data_to_gcs(ingestion_date, minimum_price, maxium_price ,step = 1000):
    price_ranges = np.arange(minimum_price,maxium_price,step)

    for minimum_price in tqdm(price_ranges):
        single_call_api_and_extract_data_to_gcs(ingestion_date, minimum_price, minimum_price+step-1)
        

def ingest_data_from_gcs_to_bq_by_date(ingestion_date='2023-09-04'):
    
    print(f'LOG: Removing data from BQ of date: {ingestion_date} if exists')
    from google.cloud import bigquery
    client = bigquery.Client()

    sql_query = f'''
    DELETE FROM `roma-immobiliare-395210.{BQ_DATASET_ID}.{BQ_TABLE_ID}` 
    WHERE DATE(ingestion_date) = DATE(ingestion_date);
    '''
    client.query(sql_query)


    big_query = StorageBigQuery(GCP_SERVICE_ACCOUNT_PATH)
    # print(f'LOG: Ingest data from gcs to BQ of date: {ingestion_date}')
    big_query.ingest_data_to_bigquery_from_gcs(
                                project_id = PROJECT_ID,
                                dataset_id = BQ_DATASET_ID, 
                                table_id = BQ_TABLE_ID,
                                gcs_bucket_name = GCS_BUCKET_NAME, 
                                blob_path = f'{ingestion_date}/*', 
                                bq_schema = BQ_SCHEMA,
                                location=REGION
                                )



def run_dbt():
    dbt = dbtRunner()

    # create CLI args as a list of strings
    cli_args = ["run"]

    # run the command
    res: dbtRunnerResult = dbt.invoke(cli_args)

    # inspect the results
    for r in res.result:
        print(f"{r.node.name}: {r.status}")
