from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Currency, Pricing, Category

engine = create_engine('sqlite:///cryptos.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_or_update_category(category_data):
    category = session.query(Category).filter_by(slug=category_data['slug']).first()
    if not category:
        category = Category(
            id=category_data['id'],
            name=category_data['name'],
            description=category_data.get('description', ''),
            slug=category_data['slug']
        )
        session.add(category)
        session.flush()
    return category

def add_or_update_currency(currency_data, category_id):
    currency = session.query(Currency).filter_by(coinmarketcap_id=currency_data['coinmarketcap_id']).first()

    if currency:
        currency.name = currency_data['name']
        currency.symbol = currency_data['symbol']
        currency.slug = currency_data['slug']
        currency.date_added = currency_data['date_added']
        currency.category_id = category_id
    else:
        currency = Currency(
            coinmarketcap_id=currency_data['coinmarketcap_id'],
            name=currency_data['name'],
            symbol=currency_data['symbol'],
            slug=currency_data['slug'],
            date_added=currency_data['date_added'],
            category_id=category_id
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
        pricing.last_updated = pricing_data['last_updated']
    else:
        pricing = Pricing(
            currency_id=currency_id,
            price=pricing_data['price'],
            volume_24h=pricing_data['volume_24h'],
            market_cap=pricing_data['market_cap'],
            last_updated=pricing_data['last_updated']
        )
        session.add(pricing)
    session.commit()

def add_or_update_data(currency_data, pricing_data, category_data):
    category = add_or_update_category(category_data)
    currency = add_or_update_currency(currency_data, category.id)
    add_or_update_pricing(pricing_data, currency.id)