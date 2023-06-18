from prefect.deployments import Deployment
from prefect.infrastructure import DockerContainer
from prefect_gcp.cloud_run import CloudRunJob

from flows.trigger_ingest_data import trigger_ingest_data

# infra_block = DockerContainer.load("roma-docker")
infra_block = CloudRunJob.load("roma-cloud-run")


deployment = Deployment.build_from_flow(
    flow=trigger_ingest_data,
    name="deployment-cloud-trigger_ingest_data",
    version=1,
    infrastructure=infra_block,
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