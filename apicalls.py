import requests
import os
import time
from requests.exceptions import RequestException
import logging
from requests.exceptions import HTTPError
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
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise ValueError(f"HTTP Error {response.status_code}: {response.text}")

    except RequestException as req_err:
        logging.error(f"Error fetching cryptocurrency information:  {req_err}")
        return None


def get_currency_categories(slug, max_retries=5, wait_time=60):
    url = f"{BASE_URL}/v1/cryptocurrency/categories?slug={slug}"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    attempt = 0

    while attempt < max_retries:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() 
            data = response.json()
            if response.status_code == 200:
                return data
            else:
                logging.error(f"Unexpected response status: {response.status_code}")
                return None
        except HTTPError as http_err:
            if response.status_code == 429:
                logging.error(f"Rate limit exceeded: {response.json()}")
                attempt += 1
                if attempt < max_retries:
                    logging.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logging.error("Max retries exceeded.")
                    raise
            else:
                logging.error(f"HTTP error occurred: {http_err}")
                raise
        except Exception as err:
            logging.error(f"Other error occurred: {err}")
            raise
