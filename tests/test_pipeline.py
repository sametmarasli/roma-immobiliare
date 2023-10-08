from src.pipeline_manager import bulk_call_api_and_extract_data_to_gcs
from datetime import date
from src.gcp_manager import setup_gcs_bucket, remove_gcs_bucket 
import src.logger as log 
import pytest 

@pytest.fixture
def setup_teardown_gcs():
    log.info('Setup ... setup_gcs_bucket')
    setup_gcs_bucket()
    yield
    log.info('Teardown ... remove_gcs_bucket')
    remove_gcs_bucket()


def test_bulk_call_api_and_extract_data_to_gcs(setup_teardown_gcs):
    bulk_call_api_and_extract_data_to_gcs(
        str(date.today()), 
        minimum_price=310_000, 
        maxium_price=315_000)