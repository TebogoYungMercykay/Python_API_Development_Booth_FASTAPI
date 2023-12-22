from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."

router = APIRouter(
    prefix="/chats",
    tags=['Chats']
)

@router.get('/')
def chat_messages():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }


@router.get('/get_feedback')
def get_feedback():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/post_feedback')
def post_feedback():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/whatsapp')
def whatsapp():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/meeting')
def meeting():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }

