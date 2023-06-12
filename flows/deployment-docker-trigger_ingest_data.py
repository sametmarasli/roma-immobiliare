from prefect.deployments import Deployment
from prefect.infrastructure import DockerContainer

from flows.trigger_ingest_data import trigger_ingest_data

docker_block = DockerContainer.load("roma-docker")

deployment = Deployment.build_from_flow(
    flow=trigger_ingest_data,
    name="deployment-docker-trigger_ingest_data",
    version=1,
    infrastructure=docker_block,
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