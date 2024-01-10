from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

from pydantic.types import conint


# POSTS: Schemas and Pedantic Models

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class DoctorOut(BaseModel):
    name: str
    surname: str
    specialization: str
    class Config:
        from_attributes = True


class PatientOut(BaseModel):
    name: str
    surname: str
    dob: datetime
    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class Replies(BaseModel):
    post_id: int
    content: str


class RepliesOut(BaseModel):
    post_id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        

class RepliesData(BaseModel):
    reply: RepliesOut
    doctor: DoctorOut
    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class AllPostOut(BaseModel):
    Post: Post
    votes: int
    replies: List[RepliesOut]

    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


# USERS: Schemas and Pedantic Models


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class PatientCreate(UserCreate):
    name: str
    surname: str
    dob: datetime
    address: str 
    mobile_no: int
    gender: str


class DoctorCreate(PatientCreate):
    qualification: str
    registration_no: str
    year_of_registration: datetime
    state_medical_council: str
    specialization: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str
    surname: str
    address: str 
    mobile_no: int


class DetailsOut(UserOut):
    name: str
    surname: str
    address: str
    mobile_no: int

    class Config:
        from_attributes = True


class UserData(BaseModel):
    user: UserOut
    details: DetailsOut

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# Rating and Reviews


class RatingCreate(BaseModel):
    rating: float
    review: str
    doctor_id: int


class RatingOut(BaseModel):
    rating: float
    review: str

    class Config:
        from_attributes = True


class RatingResponse(BaseModel):
    doctor_id: int
    average_rating: float
    Ratings: List[RatingOut]

    class Config:
        from_attributes = True


# Disease Information


class DiseaseCreate(BaseModel):
    no_of_symptoms: int
    symptoms: List[str]
    

class DiseaseOut(BaseModel):
    diseasename: str
    confidence: float
    consultdoctor: str
    
    class Config:
        from_attributes = True


# Consultations

 
class ConsultationCreate(BaseModel):
    doctor_id: int
    diseaseinfo_id: int
    consultation_date: datetime
    status: str


class ConsultationOut(BaseModel):
    id: int
    consultation_date: datetime
    status: str
    
    class Config:
        from_attributes = True


class ConsultationResponse(BaseModel):
    count: int
    Consultations: List[ConsultationOut]
    
    class Config:
        from_attributes = True
        

class PatientConsultationOut(BaseModel):
    patient_id: int
    consultation_date: datetime
    status: str
    doctor: DoctorOut
    diseaseinfo: DiseaseOut
    
    class Config:
        from_attributes = True
       
       
class PatientConsultationResponse(BaseModel):
    count: int
    Consultations: List[PatientConsultationOut]
    
    class Config:
        from_attributes = True    
        

class DoctorConsultationOut(BaseModel):
    doctor_id: int
    consultation_date: datetime
    status: str
    patient: PatientOut
    diseaseinfo: DiseaseOut
    
    class Config:
        from_attributes = True
        
        
class DoctorConsultationResponse(BaseModel):
    count: int
    Consultations: List[DoctorConsultationOut]
    
    class Config:
        from_attributes = True 


# CHATS: The Chatting System
        

class Chats(BaseModel):
    message: str


class ChatOut(BaseModel):
    consultation_id: int
    created_at: datetime
    message: str
    sender_id: int
    class Config:
        from_attributes = True
  

class ChatList(BaseModel):
    consultation_id: int
    chats: list[ChatOut]
    class Config:
        from_attributes = True


class FeedbackCreate(BaseModel):
    created_at: datetime
    feedback: str


class FeedbackOutput(BaseModel):
    id: int
    created_at: datetime
    feedback: str
    
    class Config:
        from_attributes = True


class Sender(BaseModel):
    name: str
    surname: str
    
    class Config:
        from_attributes = True

class FeedbackOut(FeedbackCreate):
    sender: Sender
    
    class Config:
        from_attributes = True


class FeedbackResponse(BaseModel):
    doctor_id: int
    FeedBacks: List[FeedbackOut]

    
    class Config:
        from_attributes = True

