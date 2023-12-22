from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."

router = APIRouter(
    prefix="/consultations",
    tags=['Consultations']
)

@router.get('/')
def consult_a_doctor():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/make_consultation')
def make_consultation():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }


@router.get('/consultation_history')
def consultation_history():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }


@router.get('/consultation_view')
def consultation_view():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/close_consultation')
def close_consultation():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/rate_review')
def rate_review():
    return { "message": MESSAGE_UNDER_CONSTRUCTION }

