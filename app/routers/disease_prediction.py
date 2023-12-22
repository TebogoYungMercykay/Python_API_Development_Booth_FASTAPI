from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

MESSAGE_UNDER_CONSTRUCTION = "Functionality Under Construction."

router = APIRouter(
    prefix="/disease_prediction",
    tags=['Disease Prediction Model']
)

@router.get('/')
def checkdisease():
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }


@router.post('/checkdisease')
def checkdisease():
    return { "status":"pending", "message": MESSAGE_UNDER_CONSTRUCTION }

