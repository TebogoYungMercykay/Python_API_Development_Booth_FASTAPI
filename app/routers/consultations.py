from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import JSONResponse

from sqlalchemy import func, and_
from .. import models, schemas, oauth2, utils
from ..database import get_db

MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."

router = APIRouter(
    prefix="/consultations",
    tags=['Consultations']
)

@router.post('/all_consultations/{id}', response_model=schemas.JSONConsultationResponse)
def consult_a_doctor(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Chat with id {id} not found"
        }
        return JSONResponse(content=error_response, status_code=400)
    
    consultations = db.query(models.Consultation).filter(models.Consultation.patient_id == id).all()
    if not consultations:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Consultations for Patient/Doctor with id: {id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)

    response_obj = schemas.ConsultationResponse(count=len(consultations), Consultations=consultations)
    return schemas.JSONConsultationResponse(status="success", id=current_user.id, data=response_obj)


@router.post('/make_consultation', response_model=schemas.JSONPatientConsultationOut)
def make_consultation(details: schemas.ConsultationCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == details.doctor_id).first()
    if not doctor:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Doctor with id: {details.doctor_id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)
    
    patient = db.query(models.Patient).filter(models.Patient.patient_id == current_user.id).first()
    if not patient:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Patient with id: {current_user.id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)

    diseaseinfo = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.id == details.diseaseinfo_id).first()
    if not diseaseinfo:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Disease with id: {details.diseaseinfo_id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)

    consultation = models.Consultation(patient_id=current_user.id, **details.model_dump())
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    
    message = schemas.Chat(message=f"Welcome to our consultation chat. I'm Dr. {doctor.surname} {doctor.name} and I'm here to assist you. It's great to connect with you! When you have some questions, concerns, or if there's anything you'd like to discuss, feel free to let me know. Your health is my priority.")
    new_message = models.Chat(sender_id=details.doctor_id, consultation_id=consultation.id, **message.model_dump())
    db.add(new_message)
    db.commit()
    
    response_obj = schemas.PatientConsultationOut(consultation_id=consultation.id, consultation_date=consultation.consultation_date, status=consultation.status, patient=patient, doctor=doctor, diseaseinfo=diseaseinfo)
    return schemas.JSONPatientConsultationOut(status="success", id=current_user.id, data=response_obj)


@router.post('/consultation_view_patient/{id}', response_model=schemas.JSONPatientConsultationOut)
def consultation_view_patient(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    consultation = db.query(models.Consultation).filter(and_(models.Consultation.patient_id == current_user.id, models.Consultation.id == id)).first()

    if not consultation:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Consultations for Patient with id: {current_user.id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)

    patient = db.query(models.Patient).filter(models.Patient.patient_id == consultation.patient_id).first()
    if not patient:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Patient with id: {consultation.patient_id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)
    
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == consultation.doctor_id).first()
    if not doctor:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Doctor with id: {consultation.doctor_id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)
    
    diseaseinfo = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.id == consultation.diseaseinfo_id).first()
    if not diseaseinfo:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Disease with id: {consultation.diseaseinfo_id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)
    
    consultation_details = schemas.PatientConsultationOut(consultation_id=consultation.id, consultation_date=consultation.consultation_date, status=consultation.status, patient=patient, doctor=doctor, diseaseinfo=diseaseinfo)
    return schemas.JSONPatientConsultationOut(status="success", id=current_user.id, data=consultation_details)


@router.post('/consultation_view_doctor/{id}', response_model=schemas.JSONDoctorConsultationOut)
def consultation_view_doctor(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    consultation = db.query(models.Consultation).filter(and_(models.Consultation.doctor_id == current_user.id, models.Consultation.id == id)).first()
    
    if not consultation:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Consultations for Doctor with id: {current_user.id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)
        
    patient = db.query(models.Patient).filter(models.Patient.patient_id == consultation.patient_id).first()
    if not patient:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Patient with id: {consultation.patient_id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)

    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == consultation.doctor_id).first()
    if not doctor:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Doctor with id: {consultation.doctor_id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)

    diseaseinfo = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.id == consultation.diseaseinfo_id).first()
    if not diseaseinfo:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Disease with id: {consultation.diseaseinfo_id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)
    
    consultation_details = schemas.DoctorConsultationOut(consultation_id=consultation.id, consultation_date=consultation.consultation_date, status=consultation.status, patient=patient, doctor=doctor, diseaseinfo=diseaseinfo)
    return schemas.JSONDoctorConsultationOut(status="success", id=current_user.id, data=consultation_details)


@router.post('/consultation_history_patient', response_model=schemas.JSONPatientConsultationResponse)
def consultation_history_patient(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    consultations = db.query(models.Consultation).filter(models.Consultation.patient_id == current_user.id).all()
    if not consultations:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Consultations for Patient with id: {current_user.id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)
        
    list_consultations = []
    for consultation in consultations:
        diseaseinfo = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.id == consultation.diseaseinfo_id).first()
        if not diseaseinfo:
            error_response = {
                "status": "error",
                "id": -1,
                "data": f"Disease with id: {consultation.diseaseinfo_id} not found."
            }
            return JSONResponse(content=error_response, status_code=404)
        
        consultation_details = schemas.ConsultationHistory(consultation_id=consultation.id, consultation_date=consultation.consultation_date, status=consultation.status, diseaseinfo=diseaseinfo)
        list_consultations.append(consultation_details)

    response_obj = schemas.PatientConsultationResponse(count=len(list_consultations), Consultations=list_consultations)
    return schemas.JSONPatientConsultationResponse(status="success", id=current_user.id, data=response_obj)


@router.post('/consultation_history_doctor', response_model=schemas.JSONDoctorConsultationResponse)
def consultation_history_doctor(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    consultations = db.query(models.Consultation).filter(models.Consultation.doctor_id == current_user.id).all()
    if not consultations:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Consultations for Doctor with id: {current_user.id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)
        
    list_consultations = []
    for consultation in consultations:
        diseaseinfo = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.id == consultation.diseaseinfo_id).first()
        if not diseaseinfo:
            error_response = {
                "status": "error",
                "id": -1,
                "data": f"Disease with id: {consultation.diseaseinfo_id} not found."
            }
            return JSONResponse(content=error_response, status_code=404)
    
        consultation_details = schemas.ConsultationHistory(consultation_id=consultation.id, consultation_date=consultation.consultation_date, status=consultation.status, diseaseinfo=diseaseinfo)
        list_consultations.append(consultation_details)

    response_obj = schemas.DoctorConsultationResponse(count=len(list_consultations), Consultations=list_consultations)
    return schemas.JSONDoctorConsultationResponse(status="success", id=current_user.id, data=response_obj)


@router.post('/close_consultation/{id}', response_model=schemas.JSONConsultationOut)
def close_consultation(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    consultation_query = db.query(models.Consultation).filter(models.Consultation.id == id)
    consultation = consultation_query.first()
    if not consultation:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Consultation with id: {id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)
        
    if consultation.doctor_id != current_user.id and consultation.patient_id != current_user.id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": "You are not authorized to perform this action."
        }
        return JSONResponse(content=error_response, status_code=401)
    
    consultation_query.update({"status": "closed"}, synchronize_session=False)
    db.commit()
    
    return schemas.JSONConsultationOut(status="success", id=current_user.id, data=consultation_query.first())


@router.post('/create_review/{id}', response_model=schemas.JSONRatingOut)
def create_review(id: int, review_details: schemas.RatingCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if id == current_user.id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": "You cannot rate/review yourself."
        }
        return JSONResponse(content=error_response, status_code=400)
    
    doctor = db.query(models.User).filter(models.User.id == id).first()
    if not doctor:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Doctor with id: {id} not found."
        }
        return JSONResponse(content=error_response, status_code=404)
    
    if doctor.id != review_details.doctor_id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": "Doctor id does not Match the One in Request."
        }
        return JSONResponse(content=error_response, status_code=400)
        
    review = models.RatingReview(patient_id=current_user.id, **review_details.model_dump())
    db.add(review)
    db.commit()
    
    return schemas.JSONRatingOut(status="success", id=current_user.id, data=review_details.model_dump())


@router.post('/get_reviews', response_model=schemas.JSONListRatingResponse)
def get_reviews(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    reviews = db.query(models.RatingReview).all()
    
    if not reviews:
        error_response = {
            "status": "error",
            "id": -1,
            "data": "There are Currently no Reviews"
        }
        return JSONResponse(content=error_response, status_code=404)

    reviews_by_doctor = utils.group_reviews_by_doctor(reviews)
    result = []

    for doctor_id, reviews in reviews_by_doctor.items():
        average_rating = utils.calculate_average_rating(reviews)
        rating_response = schemas.RatingResponse(doctor_id=doctor_id, average_rating=average_rating, Ratings=reviews)
        result.append(rating_response)

    return schemas.JSONListRatingResponse(status="success", id=current_user.id, data=result)


@router.post('/get_reviews/{id}', response_model=schemas.JSONRatingResponse)
def get_review(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    reviews = db.query(models.RatingReview).filter(models.RatingReview.doctor_id == id).all()
    
    if not reviews:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Reviews for Doctor with id: {id} not found"
        }
        return JSONResponse(content=error_response, status_code=404)
    
    average_rating = utils.calculate_average_rating(reviews)
    result = schemas.RatingResponse(doctor_id=id, average_rating=average_rating, Ratings=reviews)
    
    return schemas.JSONRatingResponse(status="success", id=current_user.id, data=result)

