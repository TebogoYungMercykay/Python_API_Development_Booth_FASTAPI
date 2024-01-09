from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import joblib
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from ..database import get_db

model_path = "../trained_model"
trained_model = joblib.load(model_path)

MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."

router = APIRouter(
    prefix="/disease_prediction",
    tags=['Disease Prediction Model']
)

@router.get('/{id}', response_model=List[schemas.DiseaseOut])
def get_disease(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to perform this action.")
        
    diseases = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.patient_id == current_user.id).all()
    
    all_diseases = []
    for disease in diseases:
        disease_out = schemas.DiseaseOut(**disease.dict())
        all_diseases.append(disease_out)
    
    return all_diseases


@router.post('/createdisease/{id}', response_model=schemas.DiseaseOut)
def create_disease(id: int, disease_info: schemas.DiseaseCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to perform this action.")
    elif len(disease_info.symptoms) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Number of symptoms cannot be less than 1.")
    
    num_symptoms = len(disease_info.symptoms)
    symptoms = disease_info.symptoms
    symptomslist = utils.get_symptoms_list()
    
    testingsymptoms = [0] * len(symptomslist)
    
    # for k in range(0, len(symptomslist)):
    #     for z in symptoms:
    #         if (z == symptomslist[k]):
    #             testingsymptoms[k] = 1

    for k, symptom in enumerate(symptomslist):
        if symptom in symptoms:
            testingsymptoms[k] = 1

    inputtest = [testingsymptoms]
    predict = trained_model.predict(inputtest)
    confidence = trained_model.predict_proba(inputtest).max() * 100
    predicted_disease = predict[0]
    
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