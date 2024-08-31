import requests
import os
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

def get_currency_categories(slug):
    url = f"{BASE_URL}/v1/cryptocurrency/categories?slug={slug}"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    response = requests.get(url, headers=headers)
    return response.json()