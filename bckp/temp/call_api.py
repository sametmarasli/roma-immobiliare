from src.immobiliare_api import ImmobiliareApi
import pandas as pd
import argparse
        
def main(params):
    
    minimum_price = params.minimum_price
    maximum_price = params.maximum_price
    contract_type = params.contract_type
    advert_type = params.advert_type
    province = params.province
    page_number = params.page_number

    call_api = ImmobiliareApi(
        minimum_price=minimum_price,
        maximum_price=maximum_price,
        contract_type=contract_type,
        advert_type=advert_type,
        province=province
    )

    # report = call_api.call_report()    
    data = call_api.single_page_call(page_number=page_number)
    print(data)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('--minimum_price', required=True, help='...')
    parser.add_argument('--maximum_price', required=True, help='...')
    parser.add_argument('--page_number', required=False, help='...',default=1)
    parser.add_argument('--contract_type', required=False, help='...',default=1)
    parser.add_argument('--advert_type', required=False, help='...',default=1)
    parser.add_argument('--province', required=False, help='...',default='RM')

    args = parser.parse_args()
    main(args)