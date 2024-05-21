from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
from routes.plant import app_plant
from routes.user import app_user,ACCESS_TOKEN_EXPIRE_MINUTES
from mysqlapp.database import Base , engine, get_db
from mysqlapp.schemas import Token
from mysqlapp.authenticate import authenticate_user,create_access_token
app=FastAPI()
app.include_router(app_plant)
app.include_router(app_user)
Base.metadata.create_all(bind=engine)

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

app.mount("/assets", StaticFiles(directory="FASTAPI/junglegarden/assets"), name="assets")


if __name__ == '__main__':
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
