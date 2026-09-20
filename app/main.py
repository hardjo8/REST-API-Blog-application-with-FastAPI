from fastapi import FastAPI, Response, status,HTTPException,Depends
from pydantic import BaseModel
import psycopg2
import time
from . import models,schemas
from .database import engine, get_db
from sqlalchemy.orm import session


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







my_posts = [{
    "title":"first dict",
    "content":"im bored af",
    "id":1
},
{
    "title":"fav foods",
    "content":"pizza",
    "id":2
}]
def find_post(ids):
    for p in my_posts:
        if p["id"] == ids:
            return p
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
def root():
    return {"message": "Welcome to my API"} 




@app.get("/posts")
def get_posts(db:session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post:schemas.PostCreate,db:session = Depends(get_db)):
    posts= models.Post(**post.dict())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return {"data":posts}


@app.get("/posts/{id}") 
def get_specific_id_post(id:int,db:session = Depends(get_db)):
    id_n = find_post(id)
    post_id= db.query(models.Post).filter(models.Post.id == id).first()

    if not id_n:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    return {"post_detail":post_id}



@app.delete(("/posts/{id}"),status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:session = Depends(get_db)):
    post_id= db.query(models.Post).filter(models.Post.id == id)
    
    if post_id.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_id.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}")
def update_post(id:int, post:schemas.PostCreate,db:session = Depends(get_db)):
    post_id= db.query(models.Post).filter(models.Post.id == id)
    posts = post_id.first()

    if posts == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} does not exist")
    post_id.update(post.dict(), synchronize_session = False)
    db.commit()
    return{"message":post_id.first()}

