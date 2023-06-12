from prefect.infrastructure.container import DockerContainer

# alternative to creating DockerContainer block in the UI
docker_block = DockerContainer(
    image="europe-west8-docker.pkg.dev/zoomcamp-385810/prefect-flows-docker/prefect:roma",  # insert your image here
    image_pull_policy="ALWAYS",
    auto_remove=True,
)

docker_block.save("roma-docker", overwrite=True)