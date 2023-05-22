
import json
import requests

class ImmobiliareApi:
    '''
    page_number : number of the page, max 80, 25 advert for each (2000 total)
    minimum_price - maximum_price : the range of the price
    province : RM
    contract_type : 
        - 1: Vendita,
        - 2: Affitto, 
        - 14: Asta 
    advert_type:
        - 1: Case - Appartamenti
        - 6: Nuove costruzioni
        - 4: Terreni
    '''

    def __init__(self, 
                minimum_price,
                maximum_price,
                contract_type=1 ,
                advert_type=1,
                province='RM'):
        
        # self.page_number = str(page_number)
        self.minimum_price = str(int(minimum_price))
        self.maximum_price = str(int(maximum_price))
        self.province = str(province)
        self.contract_type = str(int(contract_type))
        self.advert_type = str(advert_type)
        
    def single_page_call(self, page_number):
        
        assert (int(page_number)>0) & (int(page_number)<81)

        page_number = str(page_number)
        
        url = f"https://www.immobiliare.it/api-next/search-list/real-estates/?path= &idContratto={self.contract_type}&criterio=rilevanza&pag={page_number}&prezzoMinimo={self.minimum_price}&prezzoMassimo={self.maximum_price}&idProvincia={self.province}&idCategoria={self.advert_type}"
        
        response = requests.request("GET", url, headers={}, data={})
        
        data = json.loads(response.text)

        index_name = '_'.join([
                self.province, \
                self.minimum_price, \
                self.maximum_price, \
                page_number, \
                self.contract_type, \
                self.advert_type, \
                ])

        data['index_name'] = index_name
        
        return data
    
    def write_to_folder(self):
        pass
    
    def call_report(self):
        
        tmp_call = self.single_page_call(page_number=1)
        # print( tmp_call)
        print(
            '\n# API Call Report', \
            '\n\n## Parameters', \
            '\nprovince :' , self.province, \
            '\nminimum_price :' , self.minimum_price, \
            '\nmaximum_price :' , self.maximum_price, \
            '\ncontract_type :' , self.contract_type, \
            '\nadvert_type : ', self.advert_type, \
            '\n\n## Statistics', \
            '\nTotal ads :', tmp_call['totalAds'], \
            '\nMax pages :', tmp_call['maxPages'], \
        )
