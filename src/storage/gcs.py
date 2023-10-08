import os
from typing import Union
from google.cloud import storage
import src.logger as log
from google.api_core.exceptions import Conflict, NotFound

class StorageGCS:

    def __init__(self, service_account):
        self.service_account = service_account
    
    def create_bucket(self, bucket_name:str,location) -> None:
        """Creates a new bucket."""
        
        try: 
            log.info(f'Creating bucket :{bucket_name}')
            storage_client = storage.Client().from_service_account_json(self.service_account)
            storage_client.create_bucket(bucket_name, location=location)
        except Conflict as e:
            # Handle the Conflict exception (409 status code) when the bucket already exists
            log.error(f"Bucket '{bucket_name}' already exists. Skipping creation.")
        except Exception as e:
            # Handle other exceptions as needed
            log.error(f"An error occurred: {str(e)}")

    def delete_bucket(self, bucket_name:str, force=False) -> None:
        """Deletes a bucket"""
        assert force in (False,True), "force parameter has to be True/False"
        try:
            storage_client = storage.Client().from_service_account_json(self.service_account)
            bucket = storage_client.get_bucket(bucket_name)
            bucket.delete(force=force)
            log.info(f"Bucket {bucket.name} deleted")
        except NotFound as e:
            # Handle the NotFound exception (404 status code) when the bucket does not exist
            log.error(f"Bucket '{bucket_name}' does not exist. Skipping deletion.")
        except Exception as e:
            # Handle other exceptions as needed
            log.error(f"An error occurred: {str(e)}")

    def list_buckets(self) -> list[str]:
        """Lists all buckets."""
        storage_client = storage.Client().from_service_account_json(self.service_account)
        buckets = storage_client.list_buckets()
        return [bucket.name for bucket in buckets]
            
    def upload_blob_from_file(self,
            bucket_name:str,
            local_path:Union[str, os.PathLike], 
            gcs_path:Union[str, os.PathLike]
            ) -> None:
        
        client = storage.Client().from_service_account_json(self.service_account)
        local_file_path = local_path
        gcs_file_path = gcs_path

        bucket = client.bucket(bucket_name)
        blob = bucket.blob(gcs_file_path)
        blob.upload_from_filename(local_file_path)
        log.info(f"File {local_file_path} ingested to GCS: {gcs_file_path}")
        
        return 
    
    def upload_blob_from_memory(
            self,
            bucket_name, 
            contents, 
            destination_blob_name):
        """Uploads a file to the bucket."""
        try:
            storage_client = storage.Client().from_service_account_json(self.service_account)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_string(contents)
            log.info(f"{destination_blob_name} with contents uploaded to {bucket_name}.")

        except NotFound as e:
            # Handle the NotFound exception (404 status code) when the bucket does not exist
            log.error(f"Bucket '{bucket_name}' does not exist. Skipping uploading to bucket.")
        except Exception as e:
            # Handle other exceptions as needed
            log.error(f"An error occurred: {str(e)}")