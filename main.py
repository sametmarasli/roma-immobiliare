import numpy as np
from tqdm import tqdm
from src.api.pagination import ApiPagination
from src.models import ApiParameters
from src.storage.gcs import StorageGCS
from src.storage.bigquery import StorageBigQuery
from src import utils
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path='./config/.env.development')

LOCAL_PATH = os.getenv('LOCAL_PATH')
PROJECT_ID = os.getenv('PROJECT_ID')
REGION = os.getenv('REGION')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
GCS_BUCKET_URI = os.getenv('GCS_BUCKET_URI')
BQ_DATASET_ID = os.getenv('BQ_DATASET_ID')
BQ_TABLE_ID = os.getenv('BQ_TABLE_ID')
BQ_SCHEMA = os.getenv('BQ_SCHEMA')
GCP_SERVICE_ACCOUNT_PATH = os.getenv('GCP_SERVICE_ACCOUNT_PATH')


def setup():

    # Instantiate necessary objects
    gcs = StorageGCS(GCP_SERVICE_ACCOUNT_PATH)
    big_query = StorageBigQuery(GCP_SERVICE_ACCOUNT_PATH)
    
    # setup_storage
    print('LOG: Setting up GCS bucket')
    try:
        gcs.create_bucket(bucket_name=GCS_BUCKET_NAME, location=REGION)    
    except:
        print('LOG: GCS bucket already exists')
    
    print('LOG: Setting up BigQuery dataset')
    big_query.create_dataset(
        project_id=PROJECT_ID,
        dataset_id=BQ_DATASET_ID,
        location=REGION)

    print('LOG: Setting up BigQuery table')
    big_query.create_table(
        project_id=PROJECT_ID,
        dataset_id=BQ_DATASET_ID,
        table_id=BQ_TABLE_ID,
        bq_schema=BQ_SCHEMA)

    
def serialize_api_call_to_gcp(prezzoMinimo,prezzoMassimo):

    print(f'LOG: serialize_paginated_results: {prezzoMinimo}, {prezzoMassimo}')
    # Instantiate necessary objects
    parameters = ApiParameters(prezzoMinimo=prezzoMinimo,prezzoMassimo=prezzoMassimo)
    api = ApiPagination()
    gcs = StorageGCS(GCP_SERVICE_ACCOUNT_PATH)
    
    # fetch data
    json_results, json_file_name = api.serialize_paginated_results(parameters)
    gcs.upload_blob_from_memory(
                    bucket_name=GCS_BUCKET_NAME,
                    contents=json_results,
                    destination_blob_name=f'{utils.today_yyyymmdd()}/{json_file_name}')

def ingest_gcp_to_biqguery():
    big_query = StorageBigQuery(GCP_SERVICE_ACCOUNT_PATH)
    big_query.ingest_data_to_bigquery_from_gcs(
                                project_id = PROJECT_ID,
                                dataset_id = BQ_DATASET_ID, 
                                table_id = BQ_TABLE_ID,
                                gcs_bucket_uri = GCS_BUCKET_URI, 
                                blob_path = f'{utils.today_yyyymmdd()}/*', 
                                bq_schema = BQ_SCHEMA,
                                location=REGION
                                )
    
def bulk_serialize_api_call_to_gcp(price_range_minimum, price_range_maximum):
    
    # calculate the number of itearations for the loop
    increment = 2500
    num_iterations = int(np.ceil((price_range_maximum - price_range_minimum)/increment))

    for K in tqdm(range(num_iterations)):
        
        print(f'LOG: incerement K: {K+1}')
        price_range_minimum_i = price_range_minimum + K * increment
        price_range_maximum_i = price_range_minimum_i + increment

        serialize_api_call_to_gcp(prezzoMinimo=price_range_minimum_i, prezzoMassimo=price_range_maximum_i)
        

if __name__=="__main__":
    print('LOG: Setup started')
    setup()
    print('LOG: Setup Finished')

    price_range_minimum=100_000
    price_range_maximum=150_000
    print(f'LOG: bulk_serialize_api_call_to_gcp: {price_range_minimum}, {price_range_maximum}')
    bulk_serialize_api_call_to_gcp(price_range_minimum=price_range_minimum,price_range_maximum=price_range_maximum)
    print('LOG: bulk_serialize_api_call_to_gcp completed')

    print('LOG: Ingestion to BigQuery started')
    ingest_gcp_to_biqguery()
    print('LOG: Ingestion to Bigquery completed')



# from api.api import APICaller
# from data.data_processor import DataProcessor
# from storage.gcs import GCSUploader
# from dbt.dbt_runner import DBTRunner
# from db.bigquery import BigQueryLoader
# from dashboard.data_studio import DataStudioDashboard


# def main():
#     # Instantiate necessary objects
#     api_caller = APICaller()
#     data_processor = DataProcessor()
#     gcs_uploader = GCSUploader()
#     dbt_runner = DBTRunner()
#     bigquery_loader = BigQueryLoader()
#     data_studio_dashboard = DataStudioDashboard()

#     # Fetch data from the API
#     api_data = api_caller.fetch_data()

#     # Process the API data
#     processed_data = data_processor.process(api_data)

#     # Upload processed data to Google Cloud Storage (GCS)
#     gcs_uploader.upload_data(processed_data)

#     # Run dbt to model the data
#     dbt_runner.run()

#     # Load modeled data into BigQuery
#     bigquery_loader.load_data()

#     # Create a dashboard in Data Studio
#     data_studio_dashboard.create_dashboard()

#     # Add any additional functionality or tasks here

# if __name__ == '__main__':
#     main()
