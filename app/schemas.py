from enum import Enum
from typing import ForwardRef, List, Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from datetime import date
from .config import settings


class StatusEnum(Enum):
    PENDING = "Pending"
    DELIVERED = "Delivered"

class DeliveryTypeEnum(Enum):
    CURBSIDE = "Curbside"
    IN_HOME = "In-Home"

class CsrfSettings(BaseModel):
  secret_key: str = settings.secret_key

class Address(BaseModel):
    id: Optional[int]
    to_from: str
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]

    @property
    def formatted(self):
        return "{}, {}, {}, {}".format(
            self.street, 
            self.city,
            self.state,
            self.zip)

    class Config:
        orm_mode = True
    #@validator('zip')
    #def valid_zip(cls, v):
    #    if not re.match(r'^[0-9]{5}(?:-[0-9]{4})?$', v):
    #        raise ValueError('ZIP code is not valid')
    #    return v

class Company(BaseModel):
    id: int
    name: str
    phone_number: str
    address: Address
    contact_email: str

    class Config:
        orm_mode = True

class LocationBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class CompanyList(BaseModel):
    companies: List[Company]
    total: int

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    address: Address

class Location(BaseModel):
    id: int
    name: str
    address: Address

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    description: str
    product_number: int
    image_url: Optional[HttpUrl]
    notes: Optional[str]
    quantity: int = 1
    delivery_type: DeliveryTypeEnum

    class Config:
        orm_mode = True

class ProductCreate(ProductBase):
    location_id: int
    order_id: int

class Product(ProductBase):
    id: int
    location: Location
    order: 'Order'

class OrderBase(BaseModel):
    order_number: Optional[int]
    batch_number: Optional[int]
    estimated_ready_date: date
    products: List[Product] = []
    estimated_ready_date: Optional[date]
    estimated_delivery_date: Optional[date]
    status: StatusEnum = StatusEnum.PENDING
    delivery_address = Address
    company: Company
    notes: Optional[str]
    quote_price: Optional[float]

    class Config:
        orm_mode = True

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_at: date
    
Product.update_forward_refs()

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


class UserIn(User):
    password: str


class Users(BaseModel):
    users: List[User]
    total: int

class UserOut(User):
    id: int
    intuit_access_token: Optional[str]
    intuit_state_token: Optional[str]
    intuit_realm_id: Optional[int]
    created_at: date
    updated_at: date
    password: str
    intuit_refresh_token: Optional[str]