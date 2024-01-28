from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import JSONResponse

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."

router = APIRouter(
    prefix="/chats",
    tags=['Chats & Feedback']
)

@router.post('/chat_messages/{id}', response_model=schemas.JSONChatList)
def chat_messages(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    chats = db.query(models.Chat).filter(models.Chat.consultation_id == id).all()
    if not chats:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Chat for Consultation with id {id} not found"
        }
        return JSONResponse(content=error_response, status_code=404)
    
    consultation = db.query(models.Consultation).filter(models.Consultation.id == id).first()
    
    response_obj = schemas.ChatList(consultation_id=consultation.id, status=consultation.status, chats=chats)
    return schemas.JSONChatList(status="success", id=current_user.id, data=response_obj)


@router.post('/create_chat/{id}', response_model=schemas.JSONChatOut)
def create_message(id: int, message: schemas.Chat, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), sender_id: int = None):
    consultation = db.query(models.Consultation).filter(models.Consultation.id == id).first()
    if not consultation:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Consultation with id {id} not found"
        }
        return JSONResponse(content=error_response, status_code=404)
    
    if sender_id is not None:
        sender_id = current_user.id
    
    if consultation.status == "closed":
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Consultation with id {id} is closed"
        }
        return JSONResponse(content=error_response, status_code=404)
    
    new_message = models.Chat(sender_id=sender_id, consultation_id=id, **message.model_dump())

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return schemas.JSONChatOut(status="success", id=current_user.id, data=new_message)


@router.post('/post_feedback/{id}', response_model=schemas.JSONFeedbackOutput)
def post_feedback(id: int, message: schemas.FeedbackCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == id).first()
    if not doctor:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Doctor with id {id} not found"
        }
        return JSONResponse(content=error_response, status_code=404)
    
    new_feedback = models.Feedback(sender_id=current_user.id, receiver_id=id, **message.model_dump())

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    
    return schemas.JSONFeedbackOutput(status="success", id=current_user.id, data=new_feedback)


@router.post('/user_feedback/{id}', response_model=schemas.JSONFeedbackResponse)
def get_feedback(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == id).first()
    if not doctor:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"There is Currently no Feedback from Doctors for user, id: {id}"
        }
        return JSONResponse(content=error_response, status_code=404)
        
    reviews = db.query(models.Feedback).filter(models.Feedback.receiver_id == id).all()

    if not reviews:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"There is Currently no Feedback with id: {id}"
        }
        return JSONResponse(content=error_response, status_code=404)
    
    list_feedback = []
    for single_feedback in reviews:
        feedback_sender = db.query(models.Patient).filter(models.Patient.patient_id == single_feedback.sender_id).first()

        if not feedback_sender:
            error_response = {
                "status": "error",
                "id": -1,
                "data": f"Feedback Sender with id {single_feedback.sender_id} not found"
            }
            return JSONResponse(content=error_response, status_code=404)
        
        list_feedback.append(schemas.FeedbackOut(created_at=single_feedback.created_at, feedback=single_feedback.feedback, sender=feedback_sender))
    
    response_obj = schemas.FeedbackResponse(doctor_id=id, FeedBacks=list_feedback)
    return schemas.JSONFeedbackResponse(status="success", id=current_user.id, data=response_obj)


@router.post('/whatsapp')
def whatsapp():
    return { "status":"pending", "id": -1, "data": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/meeting')
def meeting():
    return { "status":"pending", "id": -1, "data": MESSAGE_UNDER_CONSTRUCTION }

