from fastapi import FastAPI,Depends
import psycopg2
import time
from . import models
from .database import engine, get_db
from .routers import users,post,authentication

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

get_db()

while True:


    try:
        conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres',password='AmH*BJ147K')
        cursor = conn.cursor()
        print("Database connection was succesful")
        break
    except Exception as error:
        time.sleep(2)
        print(f"Connecting to database failed, Error {error}")

app.include_router(post.router)
app.include_router(users.router)
app.include_router(authentication.router)




    
    