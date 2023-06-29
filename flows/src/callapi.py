import requests
from dataclasses import asdict

from src.models import ApiParameters, ApiResponse

BASE_URL = f"https://www.immobiliare.it/api-next/search-list/real-estates/?path= "

def get_endpoint(params: ApiParameters) -> ApiResponse:
    """"""
    response = requests.get(url=BASE_URL, params=asdict(params))
    response.raise_for_status()
    response =  ApiResponse.from_dict(response.json())
    
    return response

if __name__ == "__main__":
    params = ApiParameters(prezzoMinimo=90_000,prezzoMassimo=100_000, pag=1)
    response = get_endpoint(params)
    print(f"response {response}")
    