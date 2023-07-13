from prefect.filesystems import GitHub
from dotenv import load_dotenv
import os

load_dotenv()
REPOSITORY = os.getenv('REPOSITORY')

block = GitHub(
    repository=REPOSITORY,
    include_git_objects=False,
)

block.save("roma-storage-github", overwrite=True)