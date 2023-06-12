import json
from src.immobiliare_api import ImmobiliareApi
import numpy as np
from datetime import date
from pathlib import Path
from tqdm import tqdm
import json 


class IngestData:
    '''
    Ingests data by using ImmobiliareApi
    minimum_price : min boudary for search criteria ex: 100_000
    maximum_price : max boudary for search criteria ex: 100_000
    ingestion_directory : directory where data will be ingested
    increment : mini batch increment value, should be selected by considering max page is not greater than 80 (ex:2_500)
    '''
    def __init__(self,
                minimum_price,
                maximum_price,
                ingestion_directory,
                increment = 2500,
            ):
        
        assert Path(ingestion_directory).is_dir(), "Ingestion directory does not exist. Please enter a valid directory"

        self.minimum_price = int(minimum_price)
        self.maximum_price = int(maximum_price)
        self.increment = int(increment)
        self.ingestion_directory = ingestion_directory


    def check_increment_parameter(self):
        '''
        check if the increment parameter satisfy the condition of max 80 pages for each price min-max bucket
        if no decrease the increment parameter
        '''
        pass
    
    def daily_ingest(self):
        '''
        crawl data and ingest to json format by batches of page numbers
        '''    
        
        # print('LOGGING: daily ingesting data for parameters ')
        # print(f'LOGGING: minimum_price: {self.minimum_price} ')
        # print(f'LOGGING: maximum_price: {self.maximum_price} ')
        # print(f'LOGGING: increment: {self.increment} ')

        # YY/mm/dd
        today = date.today().strftime("%Y%m%d")

        # create the file structure
        print(Path(self.ingestion_directory))
        data_path = Path(self.ingestion_directory) \
            .joinpath(today)
    
        data_path.mkdir(parents=True, exist_ok=True)

        # calculate the number of itearations for the loop
        num_iterations = int(np.ceil((self.maximum_price - self.minimum_price)/self.increment))

        for K in tqdm(range(num_iterations)):
            
            # print('LOGGING: self.increment no:', K+1)
            # initialize the parameters for api and initialize the class
            minimum_price_i = self.minimum_price + K * self.increment
            maximum_price_i = minimum_price_i + self.increment
            immo_api = ImmobiliareApi(minimum_price = minimum_price_i, maximum_price = maximum_price_i)
            
            # make first requets as a report to find how many pages to crawl
            report = immo_api.call_report()

            for PAGE_NUMBER in range(1, report['max_pages']+1):
                
                # print('LOGGING: page number no:', PAGE_NUMBER, 'of ', report['max_pages'])
                # crawl data by page number
                # save as json under the date folder
                data = immo_api.single_page_call(page_number = PAGE_NUMBER)
                file_name = f"{minimum_price_i}_{maximum_price_i}_{PAGE_NUMBER}.json"
                filepath = data_path.joinpath(file_name)
                with filepath.open("w", encoding="UTF-8") as target: 
                    json.dump(data, target)
        
        return data_path