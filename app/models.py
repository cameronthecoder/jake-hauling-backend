from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import Boolean, Date, Float, Text
from .dependencies import Base
from sqlalchemy import Column, Enum, ForeignKey, Integer, String, CHAR
import datetime, aiohttp

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String(150), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date, default=datetime.datetime.now())
    updated_at = Column(Date, onupdate=datetime.datetime.now())
    intuit_access_token = Column(String)
    intuit_state_token = Column(String)
    intuit_realm_id = Column(Integer)
    intuit_refresh_token = Column(String)

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    to_from = Column(String(150), nullable=False)
    street = Column(String(150))
    city = Column(String(150), index=True)
    state = Column(CHAR(2))
    zip = Column(CHAR(5))

    # add to_coordinates function

    def __str__(self) -> str:
        if not self.city or not self.street or not self.state or not self.zip:
            return self.to_from
        return f"{self.street}, {self.city}, {self.state}, {self.zip}"


    async def to_coordinates(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://maps.googleapis.com/maps/api/geocode/outputFormat?key={key}&address=${self.to_string}', params=params) as resp:
                self.questions = await resp.json()


    

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    address = relationship('Address', backref=backref('companies', lazy=True))
    phone_number = Column(String(20))
    contact_email = Column(String(150))


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(Integer)
    batch_number = Column(Integer)
    estimated_ready_date = Column(Date)
    created_at = Column(Date, default=datetime.datetime.now())
    updated_at = Column(Date, onupdate=datetime.datetime.now())
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship('Company', backref=backref('orders', lazy=True))
    type = Column(Enum("Pending", "Loaded", "Delivered", name="StatusTypes"), default="Pending")
    products = relationship('Product', back_populates='order')
    attachments = relationship('Attachment', back_populates='order')
    delivery_address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    delivery_address = relationship('Address', backref=backref('orders', lazy=True))
    notes = Column(Text)
    quote_price = Column(Float)

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    address = relationship('Address', backref=backref('locations', lazy=True))

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    pickup_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    pickup_location = relationship('Location', backref=backref('products', lazy=True))
    product_number = Column(Integer)
    notes = Column(Text)
    quantity = Column(Integer, default=1, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship('Order', back_populates='products')
    delivery_type = Column(Enum("Curbside", "In-Home", name="DeliveryTypes"))

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(Text, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship('Order', back_populates='attachments')


