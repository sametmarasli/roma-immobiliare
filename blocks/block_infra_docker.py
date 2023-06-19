from prefect.infrastructure.container import DockerContainer
from dotenv import load_dotenv
import os

load_dotenv()
ARTIFACT_REGISTRY_PATH = os.getenv('ARTIFACT_REGISTRY_PATH')

# alternative to creating DockerContainer block in the UI
docker_block = DockerContainer(
    image=f"{ARTIFACT_REGISTRY_PATH}/prefect:roma",  # insert your image here
    image_pull_policy="ALWAYS",
    auto_remove=True,
)

docker_block.save("roma-infra-docker", overwrite=True)