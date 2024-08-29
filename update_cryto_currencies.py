import requests
import os
import requests
from datetime import datetime
from database import add_or_update_data
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://pro-api.coinmarketcap.com'


def get_currency_information():
    url = f"{BASE_URL}/v1/cryptocurrency/listings/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_currency_categories():
    url = f"{BASE_URL}/v1/cryptocurrency/categories"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    response = requests.get(url, headers=headers)
    return response.json()

def preprocess_data(currency_data, category_map):
    for currency in currency_data['data']:
        currency_data = {
            'coinmarketcap_id': currency['id'],
            'name': currency['name'],
            'symbol': currency['symbol'],
            'slug': currency['slug'],
            'date_added': datetime.fromisoformat(currency['date_added'].replace('Z', '+00:00'))
        }
        pricing_data = {
            'price': currency['quote']['USD']['price'],
            'volume_24h': currency['quote']['USD']['volume_24h'],
            'market_cap': currency['quote']['USD']['market_cap'],
            'last_updated': datetime.fromisoformat(currency['quote']['USD']['last_updated'].replace('Z', '+00:00'))
        }
        category_id = currency.get('category_id')
        category_data = category_map.get(category_id, {'id': None, 'name': 'Unknown', 'slug': 'unknown'})
        add_or_update_data(currency_data, pricing_data, category_data)

def main():

    currency_data = get_currency_information()
    categories_data = get_currency_categories()

    category_map = {cat['id']: cat for cat in categories_data['data']}
    preprocess_data(currency_data, category_map)
    

if __name__ == '__main__':
    main()