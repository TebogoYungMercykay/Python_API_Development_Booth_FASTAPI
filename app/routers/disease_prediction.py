from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func, and_
from .. import models, schemas, utils, oauth2
from ..database import get_db
import warnings
import joblib as jb

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

trained_model = jb.load('trained_model')

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

@router.get('/checkdisease/{id}/{disease_id}', response_model=schemas.DiseaseOut)
def checkdisease(id: int, disease_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to perform this action.")
        
    disease = db.query(models.DiseaseInfo).filter(and_(models.DiseaseInfo.patient_id == current_user.id, models.DiseaseInfo.id == disease_id)).first()
    
    if not disease:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Disease with id: {disease_id} not found.")
    return disease


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
    
    testingsymptoms = []
    for x in range(0, len(symptomslist)):
                testingsymptoms.append(0)    
    
    for k in range(0, len(symptomslist)):
        for z in symptoms:
            if (z == symptomslist[k]):
                testingsymptoms[k] = 1

    # for k, symptom in enumerate(symptomslist):
    #     if symptom in symptoms:
    #         testingsymptoms[k] = 1

    inputtest = [testingsymptoms]
    predict = trained_model.predict(inputtest)
    confidencescore = trained_model.predict_proba(inputtest)
    confidence = confidencescore.max() * 100
    predicted_disease = predict[0]
    consultdoctor = utils.map_disease_to_doctor(predicted_disease)
    
    store_disease = models.DiseaseInfo(patient_id=current_user.id, diseasename=predicted_disease, no_of_symp=num_symptoms, symptoms=symptoms, confidence=confidence, consultdoctor=consultdoctor)
    db.add(store_disease)
    db.commit()
    db.refresh(store_disease)
    
    return store_disease


