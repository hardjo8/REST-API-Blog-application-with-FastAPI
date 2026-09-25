from fastapi import Response, status,HTTPException,Depends,APIRouter
from app import models,schemas,utils,oauth2
from sqlalchemy.orm import session
from app.database import  get_db
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=[["posts"]]
)

@router.get("/",response_model=List[schemas.PostRespone])
def get_posts(db:session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code= status.HTTP_201_CREATED,response_model=schemas.PostRespone)
def create_posts(post:schemas.PostCreate,db:session = Depends(get_db),current_user= Depends(oauth2.get_current_user)):
    posts= models.Post(**post.dict())
    print(current_user)
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts


@router.get("/{id}",response_model=schemas.PostRespone) 
def get_specific_id_post(id:int,db:session = Depends(get_db)):
    post_id= db.query(models.Post).filter(models.Post.id == id).first()

    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    return post_id



@router.delete(("/{id}"),status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    post_id= db.query(models.Post).filter(models.Post.id == id)
    
    if post_id.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_id.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}",response_model=schemas.PostRespone)
def update_post(id:int, post:schemas.PostCreate,db:session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    post_id= db.query(models.Post).filter(models.Post.id == id)
    posts = post_id.first()

    if posts == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} does not exist")
    post_id.update(post.dict(), synchronize_session = False)
    db.commit()
    return post_id.first()

