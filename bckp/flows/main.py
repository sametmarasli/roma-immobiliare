from typing import List

from src.immobiliare_api import get_endpoint
from src.models import ApiParameters, ApiResponse, AdvertSchema


ENDPOINT = "character"


def get_all_paginated_results(pages: int, params: ApiParameters) -> List[AdvertSchema]:
    results = []
    for page in range(1, pages + 1):
        params.pag = page
        print(f"Calling page {page}")
        response = get_endpoint(params)
        results.extend(response.results)
    return results


if __name__ == "__main__":
    params = ApiParameters(prezzoMinimo=90_000,prezzoMassimo=100_000)
    response = get_endpoint(params)
    results = get_all_paginated_results(response.maxPages, params)
    print(f"Total records: {len(results)}")
