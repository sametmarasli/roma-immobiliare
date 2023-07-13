import os
from google.cloud import bigquery
from google.cloud import storage
from dotenv import load_dotenv
from pathlib import Path
import json 

# Load environment variables from .env file
load_dotenv('./config/.env')
service_account = os.getenv('GCP_SERVICE_ACCOUNT_PATH')

class StorageBigQuery:

    def __init__(self,service_account):
        self.service_account = service_account        
        
    

    def create_dataset(self, project_id, dataset_id: str, location) -> None:

        # Construct a BigQuery client object.
        client = bigquery.Client().from_service_account_json(service_account)
        dataset_ref = f"{project_id}.{dataset_id}"

        client.delete_dataset(dataset_ref, delete_contents=True, not_found_ok=True)

        # Construct a full Dataset object to send to the API.
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location

        dataset = client.create_dataset(dataset)  # Make an API request.
        print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
        
    
    def delete_dataset(self, project_id, dataset_id: str) -> None:

        # Construct a BigQuery client object.
        client = bigquery.Client().from_service_account_json(service_account)
        dataset_ref = f"{project_id}.{dataset_id}"

        # Use the delete_contents parameter to delete a dataset and its contents.
        # Use the not_found_ok parameter to not receive an error if the dataset has already been deleted.
        client.delete_dataset(
            dataset_ref, delete_contents=True, not_found_ok=True
        )  # Make an API request.

        print("Deleted dataset '{}'.".format(dataset_id))

    def create_table(
                self,
                project_id,
                dataset_id,
                table_id: str,
                bq_schema) -> None:
            
        client = bigquery.Client().from_service_account_json(service_account)
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        
        with open(bq_schema, "r") as schema_file:
            schema = json.load(schema_file)
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)  # Make an API request.
        print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))
        
    def delete_table(
                self,
                project_id,
                dataset_id,
                table_id: str,) -> None:

        client = bigquery.Client().from_service_account_json(service_account)
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        # If the table does not exist, delete_table raises
        # google.api_core.exceptions.NotFound unless not_found_ok is True.
        client.delete_table(table_ref, not_found_ok=True)  # Make an API request.
        print("Deleted table '{}'.".format(table_id))

    def ingest_data_to_bigquery_from_gcs(self, 
                                project_id,
                                dataset_id, 
                                table_id,
                                gcs_bucket_uri, 
                                blob_path, 
                                bq_schema,
                                location,
                                ):



        client = bigquery.Client().from_service_account_json(service_account)
        table_ref = f"{project_id}.{dataset_id}.{table_id}"

        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        with open(bq_schema, "r") as schema_file:
            schema = json.load(schema_file)
        job_config.schema = schema
        job_config.autodetect = False
        
        uri = f"{gcs_bucket_uri}{blob_path}"

        load_job = client.load_table_from_uri(
            source_uris=uri,
            location=location,
            destination=table_ref,
            job_config=job_config
        )

        load_job.result()  # Wait for the job to complete

        table = client.get_table(table_ref)
        print(f"LOG: File from GCS {uri} rows into {table_id}")
 
    
    @staticmethod
    def _serialize_json_schema(schema):
        serialized_schema = [field.to_api_repr() for field in schema]
        return json.dumps(serialized_schema)
    
    def extract_table_schema(self,
                            project_id,
                            dataset_id, 
                            table_id,
                             ):
        client = bigquery.Client().from_service_account_json(service_account)
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        table = client.get_table(table_ref)
        return StorageBigQuery._serialize_json_schema(table.schema)
    



if __name__=="__main__":

    big_query = StorageBigQuery(
    dataset_id = 'dwh_prova_0923',
    table_id = 'table_prova_0923_tmp')
    
    big_query.ingest_data_to_bigquery(gcs_uri = 'gs://bucket_prova_0923/',
                                     file_path='20230712/*')
    print('data_ingested')

    # table_schema = big_query.extract_table_schema()
    # print(table_schema)
