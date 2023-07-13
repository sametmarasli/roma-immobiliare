from src.api.pagination import ApiPagination
from src.models import ApiParameters
from src.storage.local import StorageLocal
from src.storage.gcs import StorageGcs
from src.storage.bigquery import StorageBigQuery
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path='./config/.env')
local_path = os.getenv('LOCAL_PATH')
bucket_name = os.getenv('GCS_BUCKET_NAME')
gcs_uri = os.getenv('GCS_BUCKET_URI')
dataset_id = os.getenv('BQ_DATASET_ID')
table_id = os.getenv('BQ_TABLE_ID')


def main(prezzoMinimo=500_000,prezzoMassimo=500_010):
    
    
    # Instantiate necessary objects
    params = ApiParameters(prezzoMinimo=prezzoMinimo,prezzoMassimo=prezzoMassimo)
    api_pagination = ApiPagination()
    storage_local = StorageLocal()
    storage_gcs = StorageGcs(
        bucket_name=bucket_name)
    storage_bigquery = StorageBigQuery(
        dataset_id = dataset_id,
        table_id = table_id)
    
    # fetch data
    results = api_pagination.get_all_paginated_results(params)
    file_path = storage_local.serialize_api_results(path_to_serialize=local_path, parameters=params, results=results)
    storage_gcs.upload_blob(local_path=Path(local_path).joinpath(file_path), gcs_path=file_path)
    print(file_path)
    # storage_bigquery.ingest_data_to_bigquery(gcs_uri = gcs_uri, file_path=file_path)

    
    print('Finished')

if __name__=="__main__":
    main()



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
