from fastapi import FastAPI, Response, status,HTTPException,Depends
from pydantic import BaseModel
import psycopg2
import time
from . import models,schemas,utils
from .database import engine, get_db
from sqlalchemy.orm import session
from typing import List
from sqlalchemy.exc import IntegrityError


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



def root():
    return {"message": "Welcome to my API"} 




@app.get("/posts",response_model=List[schemas.PostRespone])
def get_posts(db:session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code= status.HTTP_201_CREATED,response_model=schemas.PostRespone)
def create_posts(post:schemas.PostCreate,db:session = Depends(get_db)):
    posts= models.Post(**post.dict())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts


@app.get("/posts/{id}",response_model=schemas.PostRespone) 
def get_specific_id_post(id:int,db:session = Depends(get_db)):
    post_id= db.query(models.Post).filter(models.Post.id == id).first()

    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    return post_id



@app.delete(("/posts/{id}"),status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:session = Depends(get_db)):
    post_id= db.query(models.Post).filter(models.Post.id == id)
    
    if post_id.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_id.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}",response_model=schemas.PostRespone)
def update_post(id:int, post:schemas.PostCreate,db:session = Depends(get_db)):
    post_id= db.query(models.Post).filter(models.Post.id == id)
    posts = post_id.first()

    if posts == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} does not exist")
    post_id.update(post.dict(), synchronize_session = False)
    db.commit()
    return post_id.first()



@app.post("/users", status_code= status.HTTP_201_CREATED,response_model=schemas.CreatedUser)
def CreateUser(user:schemas.UserCreate, db:session = Depends(get_db),):
    #has the password - user.passowrd
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    try:
        new_user = models.User(email=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)       
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists")

