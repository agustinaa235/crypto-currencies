from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True, autoincrement=True)
    coinmarketcap_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    circulating_supply = Column(Integer, nullable=False)
    date_added = Column(DateTime, nullable=False)
    last_updated = Column(DateTime, nullable=False)
    pricing = relationship("Pricing", back_populates="currency")
    categories = relationship("Category", back_populates="currency")

class Pricing(Base):
    __tablename__ = 'pricing'
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_id = Column(Integer, ForeignKey('currency.id'))
    price = Column(Float, nullable=False)
    volume_24h = Column(Float, nullable=False)
    percent_change_24h = Column(Float, nullable=False)
    market_cap = Column(Float, nullable=False)
    last_updated = Column(DateTime, nullable=False)
    currency = relationship("Currency", back_populates="pricing")

class Category(Base):
    __tablename__ = 'category'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    title = Column(String)
    description = Column(String)
    num_tokens = Column(Integer)
    avg_price_change = Column(Float)
    market_cap = Column(Float)
    market_cap_change = Column(Float)
    volume = Column(Float)
    volume_change = Column(Float)
    last_updated = Column(DateTime, nullable=False)
    currency_id = Column(Integer, ForeignKey('currency.id'))
    currency = relationship("Currency", back_populates="categories")