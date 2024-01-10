from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func, and_
from .. import models, schemas, oauth2, utils
from ..database import get_db

MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."

router = APIRouter(
    prefix="/consultations",
    tags=['Consultations']
)

@router.get('/all_consultations/{id}', response_model=schemas.ConsultationResponse)
def consult_a_doctor(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You cannot view other people's consultations.")
    
    consultations = db.query(models.Consultation).filter(models.Consultation.patient_id == id).all()
    if not consultations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Consultations for Patient/Doctor with id: {id} not found.")

    return schemas.ConsultationResponse(count=len(consultations), Consultations=consultations)


@router.post('/make_consultation', response_model=schemas.PatientConsultationOut)
def make_consultation(details: schemas.ConsultationCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == details.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Doctor with id: {details.doctor_id} not found.")
        
    diseaseinfo = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.id == details.diseaseinfo_id).first()
    if not diseaseinfo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Disease with id: {details.diseaseinfo_id} not found.")
        
    datetime = utils.get_current_time()
    consultation = models.Consultation(patient_id=current_user.id, **details.dict())
    db.add(consultation)
    db.commit()
    
    return schemas.PatientConsultationOut(patient_id=current_user.id, consultation_date=datetime, status=details.status, doctor=doctor, diseaseinfo=diseaseinfo)


@router.get('/consultation_view_patient/{id}', response_model=schemas.PatientConsultationOut)
def consultation_view_patient(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    consultation = db.query(models.Consultation).filter(and_(models.Consultation.patient_id == current_user.id, models.Consultation.id == id)).first()

    if not consultation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Consultations for Patient with id: {current_user.id} not found.")
        
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == consultation.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Doctor with id: {consultation.doctor_id} not found.")
    
    diseaseinfo = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.id == consultation.diseaseinfo_id).first()
    if not diseaseinfo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Disease with id: {consultation.diseaseinfo_id} not found.")
    
    consultation_details = schemas.PatientConsultationOut(patient_id=current_user.id, consultation_date=consultation.consultation_date, status=consultation.status, doctor=doctor, diseaseinfo=diseaseinfo)

    return consultation_details


@router.get('/consultation_view_doctor/{id}', response_model=schemas.DoctorConsultationOut)
def consultation_view_doctor(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    consultation = db.query(models.Consultation).filter(and_(models.Consultation.doctor_id == current_user.id, models.Consultation.id == id)).first()
    
    if not consultation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Consultations for Doctor with id: {current_user.id} not found.")
        
    patient = db.query(models.Patient).filter(models.Patient.patient_id == consultation.patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Patient with id: {consultation.patient_id} not found.")
    diseaseinfo = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.id == consultation.diseaseinfo_id).first()
    if not diseaseinfo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Disease with id: {consultation.diseaseinfo_id} not found.")
    
    consultation_details = schemas.DoctorConsultationOut(doctor_id=current_user.id, consultation_date=consultation.consultation_date, status=consultation.status, patient=patient, diseaseinfo=diseaseinfo)

    return consultation_details


@router.get('/consultation_history_patient', response_model=schemas.PatientConsultationResponse)
def consultation_history_patient(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    consultations = db.query(models.Consultation).filter(models.Consultation.patient_id == current_user.id).all()
    if not consultations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Consultations for Patient with id: {current_user.id} not found.")
        
    list_consultations = []
    for consultation in consultations:
        doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == consultation.doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Doctor with id: {consultation.doctor_id} not found.")
    
        diseaseinfo = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.id == consultation.diseaseinfo_id).first()
        if not diseaseinfo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Disease with id: {consultation.diseaseinfo_id} not found.")
        
        consultation_details = schemas.PatientConsultationOut(patient_id=current_user.id, consultation_date=consultation.consultation_date, status=consultation.status, doctor=doctor, diseaseinfo=diseaseinfo)
        list_consultations.append(consultation_details)

    return schemas.PatientConsultationResponse(count=len(list_consultations), Consultations=list_consultations)


@router.get('/consultation_history_doctor', response_model=schemas.DoctorConsultationResponse)
def consultation_history_doctor(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    consultations = db.query(models.Consultation).filter(models.Consultation.doctor_id == current_user.id).all()
    if not consultations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Consultations for Doctor with id: {current_user.id} not found.")
        
    list_consultations = []
    for consultation in consultations:
        patient = db.query(models.Patient).filter(models.Patient.patient_id == consultation.patient_id).first()
        if not patient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Patient with id: {consultation.patient_id} not found.")
    
        diseaseinfo = db.query(models.DiseaseInfo).filter(models.DiseaseInfo.id == consultation.diseaseinfo_id).first()
        if not diseaseinfo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Disease with id: {consultation.diseaseinfo_id} not found.")
    
        consultation_details = schemas.DoctorConsultationOut(doctor_id=current_user.id, consultation_date=consultation.consultation_date, status=consultation.status, patient=patient, diseaseinfo=diseaseinfo)
        list_consultations.append(consultation_details)

    return schemas.DoctorConsultationResponse(count=len(list_consultations), Consultations=list_consultations)


@router.post('/close_consultation/{id}', response_model=schemas.ConsultationOut)
def close_consultation(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    consultation_query = db.query(models.Consultation).filter(models.Consultation.id == id)
    consultation = consultation_query.first()
    if not consultation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Consultation with id: {id} not found.")
        
    if consultation.doctor_id != current_user.id and consultation.patient_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to perform this action.")
    
    consultation_query.update({"status": "closed"}, synchronize_session=False)
    db.commit()
    
    return  consultation_query.first()


@router.post('/create_review/{id}', response_model=schemas.RatingOut)
def create_review(id: int, review_details: schemas.RatingCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You cannot rate/review yourself.")
    
    doctor = db.query(models.User).filter(models.User.id == id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Doctor with id: {id} not found.")
    
    if doctor.id != review_details.doctor_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Doctor id does not Match the One in Request.")
        
    review = models.RatingReview(patient_id=current_user.id, **review_details.dict())
    db.add(review)
    db.commit()
    
    return review_details.dict()


@router.get('/get_reviews', response_model=List[schemas.RatingResponse])
def get_reviews(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    reviews = db.query(models.RatingReview).all()
    
    if not reviews:
        raise HTTPException(status_code=404, detail="There are Currently no Reviews")

    reviews_by_doctor = utils.group_reviews_by_doctor(reviews)
    result = []

    for doctor_id, reviews in reviews_by_doctor.items():
        average_rating = utils.calculate_average_rating(reviews)
        rating_response = schemas.RatingResponse(doctor_id=doctor_id, average_rating=average_rating, Ratings=reviews)
        result.append(rating_response)

    return result


@router.get('/get_reviews/{id}', response_model=schemas.RatingResponse)
def get_review(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    reviews = db.query(models.RatingReview).filter(models.RatingReview.doctor_id == id).all()
    
    if not reviews:
        raise HTTPException(status_code=404, detail="Reviews for Doctor with id: {id} not found")
    
    average_rating = utils.calculate_average_rating(reviews)
    result = schemas.RatingResponse(doctor_id=id, average_rating=average_rating, Ratings=reviews)
    
    return result

