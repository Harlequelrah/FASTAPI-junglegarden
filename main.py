from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from routes.plant import app_plant
from mysqlapp.database import Base , engine
app=FastAPI()
app.include_router(app_plant)
Base.metadata.create_all(bind=engine)
app.mount("/assets", StaticFiles(directory="FASTAPI/junglegarden/assets"), name="assets")


if __name__ == '__main__':
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
