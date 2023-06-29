from prefect.deployments import Deployment
from prefect.infrastructure import DockerContainer, Process
from prefect_gcp.cloud_run import CloudRunJob
from prefect.filesystems import GCS, LocalFileSystem, GitHub
from flows.trigger_ingest_data import trigger_ingest_data

# storage_block = LocalFileSystem.load('roma-storage-local')
# infra_block = Process.load('roma-infra-local')
storage_block = GitHub.load('roma-storage-github')
# infra_block = DockerContainer.load("roma-infra-docker")
infra_block = CloudRunJob.load("roma-infra-cloudrun")


deployment = Deployment.build_from_flow(
    flow=trigger_ingest_data,
    name="deployment-infra-cloudrun-storage-github-trigger_ingest_data",
    version=1,
    infrastructure=infra_block,
    storage=storage_block,
    work_queue_name="main",
    parameters={
        "model": {
            "minimum_price": 10_000,
            "maximum_price": 15_000,
            "ingestion_directory" : './data'
        }
    },
)

deployment.apply()