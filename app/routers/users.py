from fastapi import status,HTTPException,Depends,APIRouter
from app import models,schemas,utils
from sqlalchemy.orm import session
from app.database import  get_db
from sqlalchemy.exc import IntegrityError

router= APIRouter(
    prefix="/users",
    tags=["users"]
)




@router.post("/", status_code= status.HTTP_201_CREATED,response_model=schemas.CreatedUser)
def CreateUser(user:schemas.UserCreate, db:session = Depends(get_db),):
    #hash the password - user.passowrd
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




@router.get("/{id}",response_model=schemas.CreatedUser)
def get_user(id:int, db:session = Depends(get_db),):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    
    return user