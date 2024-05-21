from mysqlapp import crud,schemas,models,authenticate
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from typing import List
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import  timedelta


app_user=APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404:{'description':'Utilisateur non Trouvé'}}
)



ACCESS_TOKEN_EXPIRE_MINUTES = 30







@app_user.get('/get-user/{id}',response_model=schemas.User)
async def get_user(id:int,db:Session=Depends(get_db)):
    return crud.get_user(id,db)

@app_user.get('/get-user/by-email/{email}',response_model=schemas.User)
async def get_user(email:str,db:Session=Depends(get_db)):
    return crud.get_user_by_email(email,db)

@app_user.get('/get-users',response_model=list[schemas.User])
async def get_users(db:Session=Depends(get_db)):
    return crud.get_users(db)


@app_user.get('/count-users')
async def count_users(db:Session=Depends(get_db)):
    return crud.get_count_users(db)

@app_user.post('/create-user',response_model=schemas.User)
async def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    return crud.create_user(user,db)

@app_user.put('/update-user/{id}',response_model=schemas.User)
def update_user(id:int,user:schemas.UserUpdate,db:Session=Depends(get_db)):
    return crud.update_user(id,user,db)

@app_user.delete('/delete-user/{id}',response_model=schemas.User)
def delete_user(id:int,db:Session=Depends(get_db)):
    return crud.delete_user(id,db)


@app_user.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(authenticate.get_current_user)):
    return current_user
