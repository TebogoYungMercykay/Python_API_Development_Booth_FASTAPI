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
    post: Post
    votes: int

    class Config:
        from_attributes = True


class AllPostOut(BaseModel):
    post: Post
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
    rating: int
    review: str
    doctor_id: int


class RatingOut(BaseModel):
    rating: int
    review: str

    class Config:
        from_attributes = True

   
# Disease Information and Consultations

class DiseaseCreate(BaseModel):
    diseasename: str
    no_of_symptoms: int
    symptoms: List[str]
    confidence: float
    consultdoctor: str
    

class DiseaseOut(BaseModel):
    diseasename: str
    confidence: float
    consultdoctor: str
    
    class Config:
        from_attributes = True

        
class ConsultationCreate(BaseModel):
    doctor_id: int
    diseaseinfo_id: int
    consultation_date: datetime
    status: str


class ConsultationOut(BaseModel):
    patient_id: int
    Consultations: List[ConsultationCreate]
    
    class Config:
        from_attributes = True
        
        
class Chats(BaseModel):
    consultation_id: int
    created_at: datetime
    message: str
    

class ChatsOut(BaseModel):
    consultation_id: int
    created_at: datetime
    message: str
    sender_id: int


class FeedbackCreate(BaseModel):
    created_at: datetime
    feedback: str


class FeedbackOut(FeedbackCreate):
    sender_id: int


class FeedbackResponse(BaseModel):
    user_id: int
    FeedBacks: List[FeedbackOut]

    
    class Config:
        from_attributes = True
        
