from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Accounts']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/signup_patient", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def signup_patient(user: schemas.PatientCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Accessing the ID assigned to new_user
    new_patient = models.Patient(patient_id = new_user.id, **user.dict(exclude={'email', 'password'}))
    db.add(new_patient)
    db.commit()

    return new_user

@router.post("/signup_doctor", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def signup_doctor(user: schemas.DoctorCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Accessing the ID assigned to new_user
    new_doctor = models.Doctor(doctor_id = new_user.id, **user.dict(exclude={'email', 'password'}))
    db.add(new_doctor)
    db.commit()

    return new_user

@router.get('/{id}', response_model=schemas.DetailsOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
        
    user_details = db.query(models.User, models.Patient, models.Doctor).\
        outerjoin(models.Patient, models.Patient.patient_id == models.User.id).\
        outerjoin(models.Doctor, models.Doctor.doctor_id == models.User.id).\
        filter(models.User.id == id).first()
        
    user, patient, doctor = user_details
    details = patient or doctor
        
    if not details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Details for User with id: {id} does not exist")
    return {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at,
            "name": details.name,
            "surname": details.surname,
            "address": details.address,
            "mobile_no": details.mobile_no,
        }


@router.put('/savedata/{id}')
def savedata(id: int, update_user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    print(id)
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to perform this action.")
    
    patient_query = db.query(models.Patient).filter(models.Patient.patient_id == id).first()
    doctor_query = db.query(models.Doctor).filter(models.Doctor.doctor_id == id).first()

    if not patient_query and not doctor_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")

    update_data = update_user.dict(exclude_unset=True)

    if patient_query:
        db.query(models.Patient).filter(models.Patient.patient_id == id).update(update_data, synchronize_session=False)
    elif doctor_query:
        db.query(models.Doctor).filter(models.Doctor.doctor_id == id).update(update_data, synchronize_session=False)

    db.commit()

    return { "status": "success", "message": "User Data Successfully Updated." }

