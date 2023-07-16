import os
from typing import Union
from google.cloud import storage


class StorageGCS:

    def __init__(self, service_account):
        self.service_account = service_account
    
    def create_bucket(self, bucket_name:str,location) -> None:
        """Creates a new bucket."""
        storage_client = storage.Client().from_service_account_json(self.service_account)
        bucket = storage_client.create_bucket(bucket_name, location=location)
        print(f"Bucket {bucket.name} created")
    
    def delete_bucket(self, bucket_name:str, force=False) -> None:
        """Deletes a bucket. The bucket must be empty."""
        storage_client = storage.Client().from_service_account_json(self.service_account)
        bucket = storage_client.get_bucket(bucket_name)
        bucket.delete(force=force)
        print(f"Bucket {bucket.name} deleted")
    
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
        print(f"LOG: File {local_file_path} ingested to GCS: {gcs_file_path}")
        
        return 
    
    def upload_blob_from_memory(
            self,
            bucket_name, 
            contents, 
            destination_blob_name):
        """Uploads a file to the bucket."""
        storage_client = storage.Client().from_service_account_json(self.service_account)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(contents)
        print(f"LOG: {destination_blob_name} with contents uploaded to {bucket_name}.")

if __name__ == "__main__":
    pass