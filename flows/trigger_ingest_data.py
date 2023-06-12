from src.ingest_data import IngestData
from prefect_gcp.cloud_storage import GcsBucket
from prefect import flow, task
from pydantic import BaseModel
from pathlib import Path

class Model(BaseModel):
    minimum_price: int
    maximum_price: int
    ingestion_directory : Path

@task(log_prints=True)
def ingest_data(model: Model):        
    '''
    Ingest data to local directory
    '''
    print(f"LOGGING: Sending request with data: min/max: {model.minimum_price}-{model.maximum_price}")
    ingest_data = IngestData(
        minimum_price=model.minimum_price,
        maximum_price=model.maximum_price,
        ingestion_directory=model.ingestion_directory
        )
    ingest_path = ingest_data.daily_ingest()
    return ingest_path


@task(log_prints=True)
def write_gcs(ingestion_directory: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("roma-gcs")
    gcs_block.upload_from_folder(from_folder=ingestion_directory, to_folder=ingestion_directory)
    return


@flow(log_prints=True)
def trigger_ingest_data(model: Model):
    print("LOGGING: Triggering ingest data")
    print("LOGGING: Ingesting and writing to local disk")
    ingest_path = ingest_data(model)
    print(f"LOGGING: Uploading to GCS folder: {ingest_path}")
    write_gcs(ingest_path)
    return

if __name__ == '__main__':
    
    model = Model(
    minimum_price= 10_000,
    maximum_price= 15_000,
    ingestion_directory = './data'
        )
    trigger_ingest_data(model)
