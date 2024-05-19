from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field
from .models import Category

class PlantBase(BaseModel):
    name: str = Field(..., example='tournesol')
    category: Category = Field(..., example='exterieur')
    light: int = Field(..., example=1)
    water: int = Field(..., example=2)
    price: Decimal = Field(..., example=Decimal('15.00'))  # Utilisation du type Decimal pour le prix
    cover: str=Field(..., example='image.jpg')

class PlantUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[Category] = None
    light: Optional[int] = None
    water: Optional[int] = None
    price: Optional[Decimal] = None  # Utilisation du type Decimal pour le prix
    cover: Optional[str]=None

class PlantCreate(PlantBase):
    pass

class Plant(PlantBase):
    id: int
    date_created: date
    date_updated: date

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username:Optional[str]=None
    email: Optional[str]=None
    password: Optional[str]=None

class User(UserCreate):
    id:int
    class config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
