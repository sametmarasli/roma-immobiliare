import json
from datetime import date
from pathlib import Path
from typing import List,Union
from dataclasses import asdict
import os 

from src.models import ApiParameters, AdvertSchema



class StorageLocal:
    '''
    '''
    def __init__(self):        
        # assert Path(ingestion_directory).is_dir(), "Ingestion directory does not exist. Please enter a valid directory"
        pass


    def store_local(self, 
                    local_path: Union[str, os.PathLike],
                    serialized_paginated_results:tuple[bytes, str],
                    ) -> Union[str, os.PathLike] :
        '''
        '''    
        json_results, json_file_name = serialized_paginated_results
        
        # create the file structure as YY/mm/dd
        today = date.today().strftime("%Y%m%d")
        local_path_to_serialize = Path(local_path).joinpath(today)
        local_path_to_serialize.mkdir(parents=True, exist_ok=True)
    
        new_file_path = local_path_to_serialize.joinpath(json_file_name)

        # serialize as json
        with open(new_file_path, "w") as target: 
            target.write(json_results)
    
        print(f"LOG: File {json_file_name} serialized to local directory: {new_file_path}")

        return json_file_name

if __name__ == "__main__":
    pass