from fastapi import status,HTTPException,Depends,APIRouter
from app import models,schemas,utils,oauth2
from sqlalchemy.orm import session
from app.database import  get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def user_login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:session = Depends(get_db),):
    user_email =db.query(models.User).filter(models.User.email== user_credentials.username).first()
    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user_email.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail=f"Invalid Credentials")
    jwt_token = oauth2.create_access_token(data= {"user_ID":user_email.id})
    return {"access_token":jwt_token, "token_type": "bearer"}
    
    

