from prefect.deployments import Deployment
from prefect.server.schemas.schedules import RRuleSchedule
# from prefect.filesystems import GCS

from flows.trigger_ingest_data import trigger_ingest_data

# storage = GCS.load("dev")

deployment = Deployment.build_from_flow(
    flow=trigger_ingest_data,
    name="deployment-trigger_ingest_data",
    version=1,
    work_queue_name="main",
    # schedule=RRuleSchedule(rrule="RRULE:FREQ=DAILY"),
    # storage=storage,
    parameters={
        "model": {
            "minimum_price": 10_000,
            "maximum_price": 15_000,
            "ingestion_directory" : './data'
        }
    },
)

deployment.apply()