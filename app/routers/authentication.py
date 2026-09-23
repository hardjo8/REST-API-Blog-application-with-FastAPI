from fastapi import status,HTTPException,Depends,APIRouter
from app import models,schemas,utils
from sqlalchemy.orm import session
from app.database import  get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def user_login(user_credentials:schemas.UserLogin,db:session = Depends(get_db),):
    user_email =db.query(models.User).filter(models.User.email== user_credentials.email).first()
    if not user_email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user_email.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Invalid Credentials")
    return {"verification":"example"}
    
    

