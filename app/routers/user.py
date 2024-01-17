from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas, utils, oauth2
from ..database import get_db
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/users",
    tags=['Accounts']
)

MESSAGE_UNAUTHORIZED = "You are not authorized to perform this action."
MESSAGE_EMAIL = "Your email address already exists in our database."

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password

#     new_user = models.User(**user.model_dump())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user

@router.post("/signup_patient", status_code=status.HTTP_201_CREATED, response_model=schemas.JSONUserOut)
def signup_patient(user: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_EMAIL
        }
        return JSONResponse(content=error_response, status_code=400)
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Accessing the ID assigned to new_user
    new_patient = models.Patient(patient_id=new_user.id, **user.dict(exclude={'email', 'password'}))
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    
    return schemas.JSONUserOut(status="success", id=new_patient.patient_id, data=new_user)


@router.post("/signup_doctor", status_code=status.HTTP_201_CREATED, response_model=schemas.JSONUserOut)
def signup_doctor(user: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_EMAIL
        }
        return JSONResponse(content=error_response, status_code=400)
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Accessing the ID assigned to new_user
    new_doctor = models.Doctor(doctor_id=new_user.id, **user.dict(exclude={'email', 'password'}))
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    
    return schemas.JSONUserOut(status="success", id=new_doctor.doctor_id, data=new_user)


@router.post('/doctors', response_model=schemas.JSONListDoctorOut)
def get_doctors(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    doctors = db.query(models.Doctor).all()
    
    if not doctors:
        error_response = {
            "status": "error",
            "id": -1,
            "data": "No doctors found"
        }
        return JSONResponse(content=error_response, status_code=404)
        
    return schemas.JSONListDoctorOut(status="success", id=current_user.id, data=doctors)


@router.post('/{id}', response_model=schemas.JSONUserData)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_UNAUTHORIZED
        }
        return JSONResponse(content=error_response, status_code=401)
    
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == id).first()
    patient = db.query(models.Patient).filter(models.Patient.patient_id == id).first()

    if not doctor and not patient:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Details for User with id: {id} does not exist"
        }
        return JSONResponse(content=error_response, status_code=404)
    
    details = doctor
    if patient:
        details = patient
        
    if not details:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Details for User with id: {id} does not exist"
        }
        return JSONResponse(content=error_response, status_code=404)

    response_obj = schemas.UserData(user=current_user, details=details)

    return schemas.JSONUserData(status="success", id=current_user.id, data=response_obj)


@router.put('/savedata/{id}')
def savedata(id: int, update_user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_UNAUTHORIZED
        }
        return JSONResponse(content=error_response, status_code=401)
    
    patient_query = db.query(models.Patient).filter(models.Patient.patient_id == id)
    doctor_query = db.query(models.Doctor).filter(models.Doctor.doctor_id == id)

    patient = patient_query.first()
    doctor = doctor_query.first()
    
    if not patient and not doctor:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"user with id: {id} does not exist"
        }
        return JSONResponse(content=error_response, status_code=404)

    update_data = update_user.dict(exclude_unset=True)

    if patient:
        patient_query.update(update_data, synchronize_session=False)

    else:
        doctor_query.update(update_data, synchronize_session=False)

    db.commit()
    
    return { "status": "success", "id": -1, "data": "User Data Successfully Updated." }


@router.post('/patient_profile/{id}', response_model=schemas.JSONPatientProfile)
def patient_profile(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    patient = db.query(models.Patient).filter(models.Patient.patient_id == id).first()

    if not patient:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Details for Patient Profile with id: {id} does not exist"
        }
        
        return JSONResponse(content=error_response, status_code=404)

    return schemas.JSONPatientProfile(status="success", id=patient.patient_id, data=patient)


@router.post('/doctor_profile/{id}', response_model=schemas.JSONDoctorProfile)
def doctor_profile(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == id).first()

    if not doctor:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Details for Doctor Profile with id: {id} does not exist"
        }
        
        return JSONResponse(content=error_response, status_code=404)
        
    return schemas.JSONDoctorProfile(status="success", id=doctor.doctor_id, data=doctor)
