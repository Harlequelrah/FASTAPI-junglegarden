from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from typing import List
from fastapi import APIRouter,Depends
from mysqlapp.authenticate import get_current_user


app_plant=APIRouter(
    prefix='/plants',
    tags=['plants'],
    responses={404:{'description':'Plante non Trouvée'}}
)

@app_plant.get('/get-plant/{id}',response_model=schemas.Plant)
async def get_plant(id:int,db:Session=Depends(get_db)):
    return crud.get_plant(id,db)

@app_plant.get('/get-plants',response_model=list[schemas.Plant])
async def get_plants(db:Session=Depends(get_db)):
    return crud.get_plants(db)

@app_plant.get('/get-plants/category-{category}',response_model=list[schemas.Plant])
async def get_plants_by_category(category:models.Category,db:Session=Depends(get_db)):
    return crud.get_plants_by_category(db,category)

@app_plant.get('/count-plants')
async def count_plants(db:Session=Depends(get_db)):
    return crud.get_count_plants(db)

@app_plant.post('/create-plant',response_model=schemas.Plant)
async def create_plant(plant:schemas.PlantCreate,user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.create_plant(plant,db)

@app_plant.put('/update-plant/{id}',response_model=schemas.Plant)
def update_plant(id:int,plant:schemas.PlantUpdate,db:Session=Depends(get_db)):
    return crud.update_plant(id,plant,db)

@app_plant.delete('/delete-plant/{id}',response_model=schemas.Plant)
def delete_plant(id:int,db:Session=Depends(get_db)):
    return crud.delete_plant(id,db)
