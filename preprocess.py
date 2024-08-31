from apicalls import get_currency_categories

def preprocess_currency(currency, slug):
    currency_info = {
            'coinmarketcap_id': currency.get('id'),
            'name': currency.get('name', '').strip().title(),
            'symbol': currency.get('symbol', '').strip().upper(), 
            'slug': slug,
            'circulating_supply': float(currency.get('circulating_supply', 0)),
    } 
    return currency_info

def preprocess_categories(slug): 
    categories_data = get_currency_categories(slug)
    category_data_list = categories_data.get('data', [])
    return category_data_list
def preprocess_pricing(currency):
    
    quote_usd = currency.get('quote', {}).get('USD', {})
    pricing_info = {
            'price': float(quote_usd.get('price', 0)),
            'volume_24h': float(quote_usd.get('volume_24h', 0)), 
            'market_cap': float(quote_usd.get('market_cap', 0)),
            'percent_change_24h': float(quote_usd.get('percent_change_24h', 0)),
    }
    return pricing_info


