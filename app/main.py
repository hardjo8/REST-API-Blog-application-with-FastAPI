from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users,post,authentication
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_user :str = "postgres"
    database_password :str = "localhost"
    database_secret_key :str = "l2hco2eih2ofcuh2fo2ifh02"

settings = Settings()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)




app.include_router(post.router)
app.include_router(users.router)
app.include_router(authentication.router)




    
    