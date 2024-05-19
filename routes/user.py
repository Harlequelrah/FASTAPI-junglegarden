from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from typing import List
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import  timedelta
import secrets

app_user=APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404:{'description':'Utilisateur non Trouvé'}}
)


SECRET_KEY = str(secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




@app_user.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


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


@app_user.get("/users/me/", response_model=schemas.UserCreate)
async def read_users_me(current_user: models.User = Depends(crud.get_current_user)):
    return current_user
