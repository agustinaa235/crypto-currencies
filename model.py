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
    date_added = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    pricing = relationship("Pricing", back_populates="currency")
    category = relationship("Category", back_populates="currencies")

class Pricing(Base):
    __tablename__ = 'pricing'
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_id = Column(Integer, ForeignKey('currency.id'))
    price = Column(Float, nullable=False)
    volume_24h = Column(Float, nullable=False)
    market_cap = Column(Float, nullable=False)
    last_updated = Column(DateTime, nullable=False)
    currency = relationship("Currency", back_populates="pricing")

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    slug = Column(String, nullable=False, unique=True)
    currencies = relationship("Currency", back_populates="category")
