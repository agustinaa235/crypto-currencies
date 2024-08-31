from database import add_or_update_data
from preprocess import preprocess_currency, preprocess_pricing, preprocess_categories
from apicalls import get_currency_information
import logging

logging.basicConfig(filename='automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def has_necessary_categories(currency):
    return currency.get('name') and currency.get('slug') and currency.get('quote', {}).get('USD')

def preprocess_data(currency_data):
    for currency in currency_data['data']:
        if not has_necessary_categories(currency):
            logging.info(f"Currency data missing: {currency}")
            continue

        categories_data = preprocess_categories(currency['slug'])
        currency_info = preprocess_currency(currency, currency['slug']) 
        pricing_info = preprocess_pricing(currency)

        add_or_update_data(currency_info, pricing_info, categories_data)
        logging.info(f"Processed currency: {currency['slug']}")

def main():
    try:
        logging.info("Starting data processing")
        currency_data = get_currency_information()
        preprocess_data(currency_data)
        logging.info("Data processing completed")
    except Exception as e:
        logging.error(f"Error during processing: {e}")

if __name__ == '__main__':
    main()