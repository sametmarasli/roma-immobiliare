from prefect.infrastructure import Process
from dotenv import load_dotenv
import os

load_dotenv()
PROJECT_PATH = os.getenv('PROJECT_PATH')

block = Process(
    working_dir=PROJECT_PATH
)

block.save("roma-infra-local", overwrite=True)