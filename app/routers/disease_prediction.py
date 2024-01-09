from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import joblib
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from ..database import get_db

model_path = "../trained_model"
model = joblib.load(model_path)

MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."

router = APIRouter(
    prefix="/disease_prediction",
    tags=['Disease Prediction Model']
)

@router.get('/{id}', response_model=schemas.DiseaseOut)
def checkdisease(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to perform this action.")
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/createdisease/{id}', response_model=schemas.DiseaseOut)
def createdisease(id: int, disease_info: schemas.DiseaseCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to perform this action.")
    elif len(disease_info.symptoms) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Number of symptoms cannot be less than 1.")
    
    disease_info.no_of_symptoms = len(disease_info.symptoms)
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }


# class DiseaseCreate(BaseModel):
#     no_of_symptoms: int
#     symptoms: List[str]
    

# class DiseaseOut(BaseModel):
#     diseasename: str
#     confidence: float
#     consultdoctor: str
    
#     class Config:
#         from_attributes = True

# class DiseaseInfo(Base):
#     __tablename__ = "diseaseinfos"

#     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
#     patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="SET NULL"), nullable=True)
#     diseasename = Column(String(200), nullable=False)
#     no_of_symp = Column(Integer, nullable=False)
#     symptoms = Column(ARRAY(String), nullable=False)
#     confidence = Column(Float, nullable=False)
#     consultdoctor = Column(String(200), nullable=False)