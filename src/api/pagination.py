from typing import List
import uuid
from src.api.call import ImmobiliareApi
from src.models import ApiParameters, ApiResponse, AdvertSchema
import json
from dataclasses import asdict

class ApiPagination:

    def __init__(self):
        pass
    
    def _get_maximum_number_of_pages_for_specific_call(self, parameters: ApiParameters) -> int:
        '''
        The Api does not fetch more than 80 pages
        So it is important to know if there are more than 80 pages
        '''
        response = ImmobiliareApi().get_endpoint(parameters)
        return response.maxPages
    
    def get_all_paginated_results(self, 
                                  parameters: ApiParameters
                                  ) -> tuple[List[AdvertSchema], tuple[str,str]]:
        '''
        Get all the responses for all pages
        '''
        results = []
        pages = self._get_maximum_number_of_pages_for_specific_call(parameters)
        for page in range(1, pages + 1):
            parameters.pag = page
            print(f"Calling page {page} for {parameters.prezzoMinimo}-{parameters.prezzoMassimo} out ot {pages}")
            response = ImmobiliareApi().get_endpoint(parameters)
            results.extend(response.results)

        minimum_price = parameters.prezzoMinimo
        maximum_price = parameters.prezzoMassimo
             
        return results, (minimum_price, maximum_price)
    
    def serialize_paginated_results(self, 
                parameters: ApiParameters,
                ) -> bytes :
            '''
            '''    
            results, min_max_price_parameters = self.get_all_paginated_results(parameters)

            json_file_name = f"{min_max_price_parameters[0]}_{min_max_price_parameters[1]}.json"
            
            # serialize as json
            json_results = '\n'.join(
                [ json.dumps({ **asdict(result), ** {"advert_id":str(uuid.uuid4())}}) for result in results]
            )
                
            return json_results, json_file_name

if __name__ == "__main__":
    pass

        