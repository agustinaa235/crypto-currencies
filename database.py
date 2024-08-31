from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from model import Base, Currency, Pricing, Category
from datetime import datetime



engine = create_engine('sqlite:///cryptos.db', echo=True)
inspector = inspect(engine)


if 'currency' not in inspector.get_table_names() or 'pricing' not in inspector.get_table_names() or 'category' not in inspector.get_table_names():
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()



def add_or_update_category(category_data, currency_id):
    for cat_data in category_data:
        category = session.query(Category).filter_by(id=cat_data['id']).first()
        if not category:
            category = Category(
                id=cat_data['id'],
                currency_id=currency_id,
                name=cat_data['name'],
                title=cat_data['title'],
                description=cat_data.get('description', ''),
                num_tokens=cat_data.get('num_tokens', 0),
                avg_price_change=cat_data.get('avg_price_change', 0.0),
                market_cap=cat_data.get('market_cap', 0.0),
                market_cap_change=cat_data.get('market_cap_change', 0.0),
                volume=cat_data.get('volume', 0.0),
                volume_change=cat_data.get('volume_change', 0.0),
                last_updated=datetime.utcnow()
            )
            session.add(category)
        else:
            category.name = cat_data['name']
            category.title = cat_data['title']
            category.description = cat_data.get('description', '')
            category.num_tokens = cat_data.get('num_tokens', 0)
            category.avg_price_change = cat_data.get('avg_price_change', 0.0)
            category.market_cap = cat_data.get('market_cap', 0.0)
            category.market_cap_change = cat_data.get('market_cap_change', 0.0)
            category.volume = cat_data.get('volume', 0.0)
            category.volume_change = cat_data.get('volume_change', 0.0)
            category.last_updated = datetime.utcnow()
    session.commit()

def add_or_update_currency(currency_data):
    currency = session.query(Currency).filter_by(coinmarketcap_id=currency_data['coinmarketcap_id']).first()
    if currency:  
        currency.name = currency_data['name']
        currency.symbol = currency_data['symbol']
        currency.slug = currency_data['slug']
        currency.circulating_supply = currency_data['circulating_supply']
        currency.last_updated = datetime.utcnow()

    else:
        currency = Currency(
            coinmarketcap_id=currency_data['coinmarketcap_id'],
            name=currency_data['name'],
            symbol=currency_data['symbol'],
            slug=currency_data['slug'],
            circulating_supply=currency_data['circulating_supply'],
            date_added=datetime.utcnow(),
            last_updated=datetime.utcnow()
        )
        session.add(currency)
        session.flush()

    return currency

def add_or_update_pricing(pricing_data, currency_id):
    pricing = session.query(Pricing).filter_by(currency_id=currency_id).first()
    if pricing:
        
        pricing.price = pricing_data['price']
        pricing.volume_24h = pricing_data['volume_24h']
        pricing.market_cap = pricing_data['market_cap']
        pricing.percent_change_24h = pricing_data['percent_change_24h']
        pricing.last_updated = datetime.utcnow()
    else:
        pricing = Pricing(
            currency_id=currency_id,
            price=pricing_data['price'],
            volume_24h=pricing_data['volume_24h'],
            market_cap=pricing_data['market_cap'],
            percent_change_24h=pricing_data['percent_change_24h'],
            last_updated=datetime.utcnow()
        )
        session.add(pricing)

    session.commit()

def add_or_update_data(currency_data, pricing_data, category_data):
    currency = add_or_update_currency(currency_data)
    add_or_update_pricing(pricing_data, currency.id)
    add_or_update_category(category_data, currency.id)