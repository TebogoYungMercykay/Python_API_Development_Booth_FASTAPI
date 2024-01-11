from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import JSONResponse

from sqlalchemy import func, and_
from .. import models, schemas, utils, oauth2
from ..database import get_db
import warnings
import joblib as jb

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

trained_model = jb.load('trained_model')

MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."
MESSAGE_UNAUTHORIZED = "You are not authorized to perform this action."

router = APIRouter(
    prefix="/disease_prediction",
    tags=['Disease Prediction Model']
)

@router.post('/{id}', response_model=schemas.JSONListDiseaseOut)
def get_disease(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_UNAUTHORIZED
        }
        return JSONResponse(content=error_response, status_code=401)
        
    diseases = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.patient_id == current_user.id).all()
    
    return schemas.JSONListDiseaseOut(status="success", id=current_user.id, data=diseases)


@router.post('/check_disease/{id}/{disease_id}', response_model=schemas.JSONDiseaseOut)
def check_disease(id: int, disease_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_UNAUTHORIZED
        }
        return JSONResponse(content=error_response, status_code=401)
        
    disease = db.query(models.DiseaseInfo).filter(and_(models.DiseaseInfo.patient_id == current_user.id, models.DiseaseInfo.id == disease_id)).first()
    
    if not disease:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Disease with id: {disease_id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)

    return schemas.JSONDiseaseOut(status="success", id=current_user.id, data=disease)


@router.post('/create_disease/{id}', response_model=schemas.JSONDiseaseOut)
def create_disease(id: int, disease_info: schemas.DiseaseCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_UNAUTHORIZED
        }
        return JSONResponse(content=error_response, status_code=404)

    elif len(disease_info.symptoms) < 1:
        error_response = {
            "status": "error",
            "id": -1,
            "data": "Number of symptoms cannot be less than 1."
        }
        return JSONResponse(content=error_response, status_code=400)
    
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
    
    return schemas.JSONDiseaseOut(status="success", id=store_disease.id, data=store_disease)

