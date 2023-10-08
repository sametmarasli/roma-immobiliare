import os
from google.cloud import bigquery
import json 
import src.logger as log
from google.api_core.exceptions import Conflict, NotFound

class StorageBigQuery:

    def __init__(self,service_account):
        self.service_account = service_account        
        
    
    def create_dataset(self, project_id, dataset_id: str, location) -> None:

        try:
            # Construct a BigQuery client object.
            client = bigquery.Client().from_service_account_json(self.service_account)
            dataset_ref = f"{project_id}.{dataset_id}"

            # Construct a full Dataset object to send to the API.
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = location

            dataset = client.create_dataset(dataset)  # Make an API request.
            log.info("Created dataset {}.{}".format(client.project, dataset.dataset_id))
            
        except Conflict as e:
            # Handle the Conflict exception (409 status code) when the bucket already exists
            log.info(f"Dataset '{dataset_id}' already exists. Skipping creation.")
        except Exception as e:
            # Handle other exceptions as needed
            log.info(f"An error occurred: {str(e)}")


    def delete_dataset(self, project_id, dataset_id: str) -> None:

        try:
            # Construct a BigQuery client object.
            client = bigquery.Client().from_service_account_json(self.service_account)
            dataset_ref = f"{project_id}.{dataset_id}"

            # Use the delete_contents parameter to delete a dataset and its contents.
            # Use the not_found_ok parameter to not receive an error if the dataset has already been deleted.
            client.delete_dataset(dataset_ref, delete_contents=True, not_found_ok=False)  # Make an API request.
            log.info("Deleted dataset '{}'.".format(dataset_id))
        
        except NotFound as e:
            # Handle the NotFound exception (404 status code) when the bucket does not exist
            log.info(f"Dataset '{dataset_id}' does not exist. Skipping deletion.")
        except Exception as e:
            # Handle other exceptions as needed
            log.info(f"An error occurred: {str(e)}")



    def create_table(self, project_id, dataset_id, table_id: str, bq_schema=None) -> None:
        
        try:
            client = bigquery.Client().from_service_account_json(self.service_account)
            table_ref = f"{project_id}.{dataset_id}.{table_id}"

            if bq_schema:
                log.info('Schema is provided')
                with open(bq_schema, "r") as schema_file:
                    schema = json.load(schema_file)
                table = bigquery.Table(table_ref, schema=schema)
            else:
                log.info('Schema is not provided')
                table = bigquery.Table(table_ref)

            table = client.create_table(table)  # Make an API request.
            log.info("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))
            
        except Conflict as e:
            # Handle the Conflict exception (409 status code) when the bucket already exists
            log.info(f"Table '{table}' already exists. Skipping creation.")
        except Exception as e:
            # Handle other exceptions as needed
            log.info(f"An error occurred: {str(e)}")


    def delete_table(self, project_id, dataset_id, table_id: str,) -> None:
        try:
            client = bigquery.Client().from_service_account_json(self.service_account)
            table_ref = f"{project_id}.{dataset_id}.{table_id}"
            # If the table does not exist, delete_table raises
            # google.api_core.exceptions.NotFound unless not_found_ok is True.
            client.delete_table(table_ref, not_found_ok=False)  # Make an API request.
            log.info("Deleted table '{}'.".format(table_id))

        except NotFound as e:
            # Handle the NotFound exception (404 status code) when the bucket does not exist
            log.info(f"Table '{table_id}' does not exist. Skipping deletion.")
        except Exception as e:
            # Handle other exceptions as needed
            log.info(f"An error occurred: {str(e)}")


    def check_table_exists(self,project_id, dataset_id, table_id):
        client = bigquery.Client().from_service_account_json(self.service_account)
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        log.info(f'Checking if the table {table_ref} exists')
        client.get_table(table_ref)
        return  # The dataset exists
        

    def ingest_data_to_bigquery_from_gcs(self, 
                                project_id,
                                dataset_id, 
                                table_id,
                                gcs_bucket_name, 
                                blob_path, 
                                bq_schema,
                                location,
                                ):
        
        try:
            self.check_table_exists(project_id, dataset_id, table_id)
        except Exception as e:
            log.error(f'BigQuery table {table_id} does not exist')
            return 
        
        client = bigquery.Client().from_service_account_json(self.service_account)
        table_ref = f"{project_id}.{dataset_id}.{table_id}"

        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        with open(bq_schema, "r") as schema_file:
            schema = json.load(schema_file)
        job_config.schema = schema
        job_config.autodetect = False
        
        uri = f"gs://{gcs_bucket_name}/{blob_path}"

        load_job = client.load_table_from_uri(
            source_uris=uri,
            location=location,
            destination=table_ref,
            job_config=job_config,
        )

        load_job.result()  # Wait for the job to complete

        # table = client.get_table(table_ref)
        log.info(f"Ingestion completed from GCS {uri} to {table_id}")
        
    
    @staticmethod
    def _serialize_json_schema(schema):
        serialized_schema = [field.to_api_repr() for field in schema]
        return json.dumps(serialized_schema)
    
    def extract_table_schema(self,
                            project_id,
                            dataset_id, 
                            table_id,
                             ):
        client = bigquery.Client().from_service_account_json(self.service_account)
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        table = client.get_table(table_ref)
        return StorageBigQuery._serialize_json_schema(table.schema)
    

    def run_query(self,sql_query):
        log.info(f'Run query of {sql_query}')
        client = bigquery.Client().from_service_account_json(self.service_account)
        return client.query(sql_query)