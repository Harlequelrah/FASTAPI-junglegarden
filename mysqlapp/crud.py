
from sqlalchemy.sql import func
from fastapi import  HTTPException,status,Depends
from typing import List
from . import models,schemas
from .database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session



def get_count_plants(db:Session):
    return db.query(func.count(models.Plant.id)).scalar()

def get_count_users(db:Session):
    return db.query(func.count(models.User.id)).scalar()



def create_plant(plant:schemas.PlantCreate,db:Session):
    db_plant=models.Plant(
        name=plant.name,
        category=plant.category,
        light=plant.light,
        water=plant.water,
        price=plant.price,
        cover=plant.cover
    )
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant


async def is_email_unique(db,email: str):
    user=db.query(models.User).filter(models.User.email == email).first()
    if user:return True
    else:raise HTTPException(status_code=400, detail="Cet email existe déja")

def create_user(user:schemas.PlantCreate,db:Session):
    if  is_email_unique(user.email):
        db_user=models.User(
            username=user.username,
            email=user.email,
            password=models.User().set_password(user.password)
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(email:str,db:Session):
    db_user=db.query(models.User).filter(models.User.email==email).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_user

def get_user(id:int,db:Session):
    db_user=db.query(models.User).filter(models.User.id==id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_user


def get_plant(id:int,db:Session):
    db_plant=db.query(models.Plant).filter(models.Plant.id==id).first()
    if db_plant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Plante non trouvée")
    return db_plant

def get_plants(db:Session,skip:int=0,limit:int=None):
    limit=get_count_plants(db)
    return db.query(models.Plant).order_by(models.Plant.name).offset(skip).limit(limit).all()

def get_users(db:Session,skip:int=0,limit:int=None):
    limit=get_count_users(db)
    return db.query(models.User).offset(skip).limit(limit).all()

def get_plants_by_category(db:Session,category:models.Category,skip:int=0,limit:int=None):
    limit=get_count_plants(db)
    return db.query(models.Plant).filter(models.Plant.category == category).order_by(models.Plant.name).offset(skip).limit(limit).all()

def delete_plant(id: int, db: Session):
    db_plant = get_plant(id, db)
    if db_plant is None:
        raise HTTPException(status_code=404, detail='Plante non trouvée')

    try:
        db.delete(db_plant)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de la plante: {str(e)}")

    return db_plant

def delete_user(id: int, db: Session):
    db_user = get_user(id, db)
    if db_user is None:
        raise HTTPException(status_code=404)

    try:
        db.delete(db_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de l 'utilisateur: {str(e)}")

    return db_user

def update_plant(id:int,plant:schemas.PlantUpdate,db:Session):
    db_plant=get_plant(id,db)
    if db_plant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Plante non trouvée")
    else:
        if plant.name is not None:
            db_plant.name=plant.name
        if plant.category is not None:
            db_plant.category=plant.category
        if plant.light is not None:
            db_plant.light=plant.light
        if plant.water is not None:
            plant.water=plant.water
        if plant.price is not None:
            db_plant.price=plant.price
        if plant.cover is not None:
            db_plant.cover=plant.cover

        db.commit()
        db.refresh(db_plant)
        return db_plant


def update_user(id:int,user:schemas.UserUpdate,db:Session):
    db_user=get_user(id,db)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if user.name is not None:
            db_user.username=user.username
        if user.email is not None:
            db_user.email=user.email
        if user.password is not None:
            db_user.password=models.User().set_password(user.password)
        db.commit()
        db.refresh(db_user)
        return db_user

