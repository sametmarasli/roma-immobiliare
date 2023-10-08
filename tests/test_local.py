# from src.storage.local import StorageLocal
# from src.api.pagination import ApiPagination
# from src.models import ApiParameters
# import pytest

# @pytest.fixture
# def provide_serialized_paginated_results():
#     # '''call some data to '''
#     parameters = ApiParameters(prezzoMinimo=101_000,prezzoMassimo=101_050)
#     json_results, json_file_name = ApiPagination().serialize_paginated_results(parameters)
#     print('setup')
#     yield json_results, json_file_name
#     print('teardown')


# def test_store_serialized_data_to_local_storage(provide_serialized_paginated_results):
#     ''''''
#     new_file_name = StorageLocal().store_local(
#         local_path='./tests/data/',
#         serialized_paginated_results=provide_serialized_paginated_results
#     )
#     print(new_file_name)



