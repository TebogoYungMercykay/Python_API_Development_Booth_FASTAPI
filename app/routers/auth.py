from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

MESSAGE_INVALID = "Invalid user Credentials."

@router.post('/login', response_model=schemas.JSONToken)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db), type: str = 'patient'):
    user_query = db.query(models.User).filter(models.User.email == user_credentials.username)
    user = user_query.first()
    names = 'Admin User'
    if not user:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_INVALID
        }
        return JSONResponse(content=error_response, status_code=403)

    else:
        if type == 'admin':
            if user.is_superuser != True:
                error_response = {
                    "status": "error",
                    "id": -1,
                    "data": MESSAGE_INVALID
                }
                return JSONResponse(content=error_response, status_code=403)
        elif type == 'doctor':
            doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == user.id).first()
            if not doctor:
                error_response = {
                    "status": "error",
                    "id": -1,
                    "data": MESSAGE_INVALID
                }
                return JSONResponse(content=error_response, status_code=403)
            
            else:
                names = 'Dr ' + doctor.surname
    
        else:
            patient = db.query(models.Patient).filter(models.Patient.patient_id == user.id).first()
            if not patient:
                error_response = {
                    "status": "error",
                    "id": -1,
                    "data": MESSAGE_INVALID
                }
                return JSONResponse(content=error_response, status_code=403)

            else:
                names = 'Mr ' + patient.surname if patient.gender == 'male' else 'Ms ' + patient.surname
    
    if not utils.verify(user_credentials.password, user.password):
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_INVALID
        }
        return JSONResponse(content=error_response, status_code=403)
    
    # Generate JWT Token
        
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    user_query.update({ "is_active": True, "last_login": utils.get_current_time() })
    db.commit()

    response_obj = { "access_token": access_token, "token_type": "bearer" }
    return schemas.JSONToken(status="success", id=user.id, name=names, data=response_obj)


@router.post('/logout/{id}')
def logout(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": "You are not authorized to perform this action."
        }
        return JSONResponse(content=error_response, status_code=401)
        
    logout_query = db.query(models.User).filter(models.User.id == current_user.id)
    logout = logout_query.first()

    if not logout:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_INVALID
        }
        return JSONResponse(content=error_response, status_code=403)

    logout_query.update({ "is_active": False })
    db.commit()
    
    response_obj = { "status":"success", "id": current_user.id, "data": "User Successfully Logged Out." }
    return response_obj

