import json
import re

import requests


class CoinMarketCapFetcher:
    def __init__(self):
        self.ROOT = 'https://pro-api.coinmarketcap.com'
        self.MAP_ENDPOINT = '/v1/cryptocurrency/map'
        self.METADATA_ENDPOINT = '/v1/cryptocurrency/info'

        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '13abaa94-5d80-4cc7-bea9-f945380100e0'
        }

        self.endpoint_request_data = {
            'MAP': {
                'url': self.ROOT + self.MAP_ENDPOINT,
                'params': {
                    'start': 1,
                    'limit': 500,
                    'listing_status': 'active'
                }
            },

            'METADATA': {
                'url': self.ROOT + self.METADATA_ENDPOINT,
                'params': {}
            }
        }
    
    def set_request_params(self, endpoint_name, extra_params):
        updated_params = {
            **self.endpoint_request_data[endpoint_name]['params'],
            **extra_params
        }
        self.endpoint_request_data[endpoint_name]['params'] = updated_params

    def _fetch_data(self, endpoint_name, extra_params=None):
        try:
            if extra_params:
                self.set_request_params(endpoint_name, extra_params)

            # Get appropriate data for endpoint request
            request_data = self.endpoint_request_data[endpoint_name]

            res = requests.get(
                request_data['url'],
                params=request_data['params'],
                headers=self.headers
            )
            return res.json()

        except KeyError:
            print('Invalid endpoint name')

    def fetch_metadata(self, ids_or_symbols):
        params = {}

        if ids_or_symbols.replace(',', '').isdigit():
            params['id'] = ids_or_symbols
        else:
            params['symbol'] = ids_or_symbols

        return self._fetch_data('METADATA', params)

    def fetch_map(self):
        return self._fetch_data('MAP')


def save_map_data(res_dict):
    '''
    Save coin data to file after fetching data from
    coinmarketcap map endpoint.
    '''
    # Filter out only coin ids and symbols into list of dict objects.
    filtered_coins = [
        {k: v for (k, v) in coinobj.items() if k in ['id', 'symbol']}
        for coinobj in res_dict['data']
    ]

    # Write to file.
    with open('coins_data.json', 'w') as f:
        json.dump(filtered_coins, f, indent=4)

def save_metadata_data(res_dict):
    with open('coins_metadata.json', 'w') as f:
        json.dump(res_dict, f, indent=4)

def clean_metadata_for_db(res_dict):
    cleaned_metadata = {}

    for k, v in res_dict.items():
        cleaned_metadata[k] = {}
        for k2, v2 in v.items():
            if k2 == 'urls':
                cleaned_metadata[k]['website'] = v[k2]['website'][0] if v[k2]['website'] else None
                cleaned_metadata[k]['repo'] = v[k2]['source_code'][0] if v[k2]['source_code'] else None

            cleaned_metadata[k]['logo'] = v['logo']
            cleaned_metadata[k]['name'] = v['name']
            cleaned_metadata[k]['symbol'] = v['symbol']
            cleaned_metadata[k]['slug'] = v['slug']
            cleaned_metadata[k]['description'] = v['description']
            cleaned_metadata[k]['platform'] = v['platform']['name'] if v['platform'] else None
            cleaned_metadata[k]['category'] = v['category']

    return cleaned_metadata

def save_metadata_for_db(cleaned_metadata):
    with open('db_metadata.json', 'w') as f:
        json.dump(cleaned_metadata, f, indent=4)

# Fetch data from coinmarketcap.
fetcher = CoinMarketCapFetcher()
res = fetcher.fetch_map()

# List of ids
# id_list_str = ','.join([str(coinobj['id']) for coinobj in res['data']])

# List of symbols
symbol_list_str = ','.join(
    [coinobj['symbol'] for coinobj in res['data'] if coinobj['symbol'].isalnum()])

res2 = fetcher.fetch_metadata(symbol_list_str)
db_data = clean_metadata_for_db(res2['data'])
save_metadata_for_db(db_data)




