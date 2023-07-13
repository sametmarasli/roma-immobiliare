from prefect_gcp.cloud_storage import GcsBucket
from src.immobiliare_api import ImmobiliareApi
import json 
import pickle

# api_call = ImmobiliareApi(minimum_price=1e5, maximum_price=2e5)
# data = api_call.single_page_call(page_number=1)
# print(data)
bucket = GcsBucket.load("roma-gcs")

# bucket.write_path(path='test.json',content=json.dumps(data).encode('utf-8'))
# bucket.write_path(path='bucket_folder2/test.pickle',content=pickle.dumps(data))
bucket.upload_from_folder(from_folder='data',to_folder='data')