from sqlalchemy import DECIMAL, Column, DateTime,Integer,String,Date,Enum
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from .event_listeners import *
import enum
from fastapi import HTTPException,status
import bcrypt


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(40), unique=True, index=True)
    password = Column(String(40))
    email = Column(String(40), unique=True, index=True)
    def set_password(self,password: str):
        self.password= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return self.password

    def check_password(self,password:str) -> bool:
        if self.password==bcrypt.checkpw(password.encode('utf-8')):return True
        else:raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid  password",
        headers={"WWW-Authenticate": "Bearer"},
    )





class Category(enum.Enum):
    CLASSIQUE='classique'
    EXTERIEUR='exterieur'
    PLANTE_GRASSE='plante_grasse'


class Plant(Base):
    __tablename__='plants'
    id = Column(Integer, primary_key=True,index=True)
    name=Column(String(20),nullable=False,index=True)
    category=Column(Enum(Category),nullable=False)
    light=Column(Integer,nullable=False)
    water=Column(Integer,nullable=False)
    price = Column(DECIMAL(precision=8, scale=2), nullable=False)
    cover=Column(String(30),nullable=False)
    date_created = Column(Date, nullable=False, default=func.now())  # Utilisation de func.now()
    date_updated = Column(Date, nullable=False, default=func.now(), onupdate=func.now())  # Utilisation de func.now() et onupdate

    @validates('light', 'water')
    def validate_light_water(self, key, value):
        if key == 'light':
            if value not in {1, 2, 3}:
                raise ValueError('Light must be 1, 2, or 3')
        elif key == 'water':
            if value not in {1, 2, 3}:
                raise ValueError('Water must be 1, 2, or 3')
        return value




register_listeners()
