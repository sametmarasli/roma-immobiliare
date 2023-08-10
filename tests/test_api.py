from src.api.pagination import ApiPagination
from src.models import ApiParameters

import tests
import pytest
import json 

@pytest.fixture
def setup_parameters():
    # '''call some data to '''
    parameters = ApiParameters(prezzoMinimo=300_000,prezzoMassimo=300_050)
    print('setup')
    yield parameters
    print('teardown')

def test_get_all_paginated_results(setup_parameters):
    api = ApiPagination()
    results, min_max_price_parameters = api.get_all_paginated_results(setup_parameters)
    print(f"LOG: Total records: {len(results)} with min-max values {min_max_price_parameters}")
    
def test_serialize_paginated_results(setup_parameters):
    api = ApiPagination()
    json_results, json_file_name = api.serialize_paginated_results(setup_parameters)
    print(json_results)
    print(f"File name is {json_file_name}")
    