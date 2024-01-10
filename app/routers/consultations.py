from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2, utils
from ..database import get_db

MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."

router = APIRouter(
    prefix="/consultations",
    tags=['Consultations']
)

@router.get('/')
def consult_a_doctor():
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/make_consultation')
def make_consultation():
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }


@router.get('/consultation_history')
def consultation_history():
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }


@router.get('/consultation_view')
def consultation_view():
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/close_consultation')
def close_consultation():
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/rate_review/{id}', response_model=schemas.RatingOut)
def rate_review(id: int, review_details: schemas.RatingCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
    db.refresh(review)
    
    return review


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


@router.get('/get_review/{id}', response_model=List[schemas.RatingResponse])
def get_review(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    reviews = db.query(models.RatingReview).filter(models.RatingReview.doctor_id == id).all()
    
    if not reviews:
        raise HTTPException(status_code=404, detail="Doctor with id: {id} not found")
    
    average_rating = utils.get_average_rating(reviews)
    result = schemas.RatingResponse(doctor_id=id, average_rating=average_rating, Ratings=reviews)
    
    return result

