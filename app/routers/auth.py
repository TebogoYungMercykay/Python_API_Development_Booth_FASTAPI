from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user_query = db.query(models.User).filter(models.User.email == user_credentials.username)
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    user_query.update({ "is_active": True, "last_login": utils.get_current_time() })
    db.commit()

    return { "access_token": access_token, "token_type": "bearer" }

@router.post('/logout/{id}')
def logout(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to perform this action.")
        
    logout_query = db.query(models.User).filter(models.User.id == current_user.id)
    logout = logout_query.first()
    if not logout:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    logout_query.update({ "is_active": False })
    db.commit()
    
    return { "status":"success", "message": "User Successfully Logged Out." }

