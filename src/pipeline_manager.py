from src import GCP_SERVICE_ACCOUNT_PATH, GCS_BUCKET_NAME, PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID, BQ_SCHEMA, REGION
import numpy as np
from tqdm import tqdm
from src.immobiliare_api.pagination import ApiPagination
from src.immobiliare_api.models import ApiParameters
from src.storage.gcs import StorageGCS
from src.storage.bigquery import StorageBigQuery
from dbt.cli.main import dbtRunner, dbtRunnerResult
import  src.logger as log

def bulk_call_api_and_extract_data_to_gcs(
        ingestion_date,
        gcs_bucket_name,
        service_account,
        minimum_price,
        maxium_price ,
        step = 1000
        ):
    """
    Calls an API and extracts data to Google Cloud Storage (GCS).

    Args:
        ingestion_date (str): The date for data ingestion.
        prezzoMinimo (int): The original minimum price argument.
        prezzoMassimo (int): The original max price argument.
    """

    gcs = StorageGCS(service_account)
    api = ApiPagination()
    
    price_ranges = np.arange(minimum_price,maxium_price,step)

    for price_range_minimum in tqdm(price_ranges):
        price_range_upper = price_range_minimum+step-1    
        parameters = ApiParameters(prezzoMinimo=price_range_minimum, prezzoMassimo=price_range_upper)
        log.info(f'Calling the api with price range {price_range_minimum}-{price_range_upper}')
        json_results, json_file_name = api.serialize_paginated_results(parameters)
        gcs.upload_blob_from_memory(
                            bucket_name=gcs_bucket_name,
                            contents=json_results,
                            destination_blob_name=f'{ingestion_date}/{json_file_name}')
        log.info(f'Finished uploading data {json_file_name} to gcs bucket {gcs_bucket_name}')


def ingest_data_from_gcs_to_bq_by_date(
        ingestion_date,
        service_account,
        location,
        project_id,
        gcs_bucket_name,
        dataset_id,
        table_id,
        bq_schema,
        ):
    

    '''
    '''
    
    big_query = StorageBigQuery(service_account)
    log.info(f'Creating table {table_id} to ingest data from GCS')
    big_query.create_table(project_id, dataset_id, table_id, bq_schema)

    # log.info(f'LOG: Removing data from BQ of date: {ingestion_date} if exists')

    # sql_query = f'''
    #     DELETE FROM `roma-immobiliare-395210.{dataset_id}.{table_id}` 
    #     WHERE DATE(ingestion_date) = DATE(ingestion_date);
    #     '''
    # big_query.run_query(sql_query)

    log.info(f'Ingest data from gcs to BQ of date: {ingestion_date}')
    big_query.ingest_data_to_bigquery_from_gcs(
                                project_id = project_id,
                                dataset_id = dataset_id, 
                                table_id = table_id,
                                gcs_bucket_name = gcs_bucket_name, 
                                blob_path = f'{ingestion_date}/*', 
                                bq_schema = bq_schema,
                                location=location
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

def remove_temporary_raw_bigquery_table(
        service_account,
        project_id,
        dataset_id,
        table_id
        ):
    big_query = StorageBigQuery(service_account)
    log.info(f'Removing table {table_id} to ingest data from GCS')
    big_query.delete_table(project_id, dataset_id, table_id)

