from prefect.filesystems import LocalFileSystem
from dotenv import load_dotenv
import os

load_dotenv()
PROJECT_PATH = os.getenv('PROJECT_PATH')

block = LocalFileSystem(
    basepath=PROJECT_PATH)

block.save("roma-storage-local", overwrite=True)