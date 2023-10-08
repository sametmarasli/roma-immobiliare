import requests
from dataclasses import asdict
from datetime import datetime

from src.immobiliare_api.models import ApiParameters, ApiResponse


class ImmobiliareApi:

    BASE_URL = f"https://www.immobiliare.it/api-next/search-list/real-estates/?path= "
    
    def __init__(self):
        pass
    
    def get_endpoint(self, params: ApiParameters) -> ApiResponse:
        """
        Returns the response from immobiliare api call for given parameters
        """
        response = requests.get(url=self.BASE_URL, params=asdict(params))
        response.raise_for_status()
        
        response =  ApiResponse.from_dict(response.json())
        
        return response


if __name__ == "__main__":
    params = ApiParameters(prezzoMinimo=90_000,prezzoMassimo=91_000, pag=11)
    response = ImmobiliareApi().get_endpoint(params)
    print(f"response {response}")
