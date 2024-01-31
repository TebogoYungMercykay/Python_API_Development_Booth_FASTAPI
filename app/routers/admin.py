from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from .. import models, schemas, oauth2 
from ..database import get_db

router = APIRouter(
    prefix="/admin",
    tags=['Administrator']
)

MESSAGE_INVALID = "Some Error Occured. Please try again."

@router.post("/", response_model=schemas.JSONAdminDiseaseIndo)
def get_info(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if not current_user:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_INVALID
        }
        return JSONResponse(content=error_response, status_code=401)
    
    if not current_user.is_superuser:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_INVALID
        }
        return JSONResponse(content=error_response, status_code=401)

    result = db.query(models.DiseaseInfo, models.Consultation.consultation_date, models.Consultation.status)\
        .join(models.Consultation, models.DiseaseInfo.id == models.Consultation.diseaseinfo_id, isouter=True).all()

    if not result:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_INVALID
        }
        return JSONResponse(content=error_response, status_code=404)
    
    return schemas.JSONAdminDiseaseIndo(status="success", id=current_user.id, data=result)
