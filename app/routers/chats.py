from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."

router = APIRouter(
    prefix="/chats",
    tags=['Chats & Feedback']
)

@router.post('/chat_messages/{id}', response_model=schemas.ChatList)
def chat_messages(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    chats = db.query(models.Chat).filter(models.Chat.consultation_id == id).all()
    if not chats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Chat with id {id} not found")
    
    return schemas.ChatList(consultation_id=id, chats=chats)


@router.post('/create_chat/{id}', response_model=schemas.ChatOut)
def create_message(id: int, message: schemas.Chat, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    consultation = db.query(models.Consultation).filter(models.Consultation.id == id).first()
    if not consultation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Consultation with id {id} not found")
        
    new_message = models.Chat(sender_id=current_user.id, consultation_id=id, **message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return new_message


@router.post('/user_feedback/{id}', response_model=schemas.FeedbackResponse)
def get_feedback(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is Currently no Feedback from Doctors for user, id: {id}")
        
    reviews = db.query(models.Feedback).filter(models.Feedback.receiver_id == id).all()
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is Currently no Feedback with id: {id}")
    
    list_feedback = []
    for single_feedback in reviews:
        feedback_sender = db.query(models.Patient).filter(models.Patient.patient_id == single_feedback.sender_id).first()
        if not feedback_sender:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Feedback Sender with id {single_feedback.sender_id} not found")
        
        list_feedback.append(schemas.FeedbackOut(created_at=single_feedback.created_at, feedback=single_feedback.feedback, sender=feedback_sender))
        
    return schemas.FeedbackResponse(doctor_id=id, FeedBacks=list_feedback)


@router.post('/post_feedback/{id}', response_model=schemas.FeedbackOutput)
def post_feedback(id: int, message: schemas.FeedbackCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Doctor with id {id} not found")
    
    new_feedback = models.Feedback(sender_id=current_user.id, receiver_id=id, **message.dict())

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    
    return new_feedback


@router.post('/whatsapp')
def whatsapp():
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/meeting')
def meeting():
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }

