from prefect.filesystems import GitHub
from dotenv import load_dotenv
import os

load_dotenv()
REPOSITORY = os.getenv('REPOSITORY')

block = GitHub(
    repository=REPOSITORY
)

block.save("roma-storage-github", overwrite=True)