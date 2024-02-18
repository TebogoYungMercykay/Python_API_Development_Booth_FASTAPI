from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

from pydantic.types import conint

# JSON: Returned Result Structure

class JSONResult(BaseModel):
    status: str
    id: int
    # data: dict
    
    class Config:
        from_attributes = True


# POSTS: Schema

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


class JSONUserOut(JSONResult):
    data: UserOut
    
    class Config:
        from_attributes = True
    

class DoctorOut(BaseModel):
    doctor_id: int
    name: str
    surname: str
    address: str
    gender: str
    qualification: str
    registration_no: str
    year_of_registration: datetime
    state_medical_council: str
    specialization: str
    rating: int
    
    class Config:
        from_attributes = True


class JSONDoctorOut(JSONResult):
    data: DoctorOut
    
    class Config:
        from_attributes = True
    

class JSONListDoctorOut(JSONResult):
    data: List[DoctorOut]
    
    class Config:
        from_attributes = True


class PatientOut(BaseModel):
    name: str
    surname: str
    dob: datetime
    patient_id: int
    address: str
    gender: str
    mobile_no: int
    class Config:
        from_attributes = True


class JSONPatientOut(JSONResult):
    data: PatientOut
    
    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class JSONPost(JSONResult):
    data: Post
    
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
        
class JSONRepliesOut(JSONResult):
    data: RepliesOut
    
    class Config:
        from_attributes = True
        

class RepliesData(BaseModel):
    reply: RepliesOut
    doctor: DoctorOut
    class Config:
        from_attributes = True


class JSONRepliesData(JSONResult):  
    data: RepliesData
    
    class Config:
        from_attributes = True
        

class PostOut(BaseModel):
    Post: Post
    votes: int
    replies: List[RepliesOut]

    class Config:
        from_attributes = True


class JSONPostOut(JSONResult):
    data: PostOut
    
    class Config:
        from_attributes = True


class JSONListPostOut(JSONResult):
    data: List[PostOut]
    
    class Config:
        from_attributes = True


class AllPostOut(BaseModel):
    Post: Post
    votes: int
    replies: List[RepliesOut]

    class Config:
        from_attributes = True


class JSONAllPostOut(JSONResult):
    data: List[AllPostOut]
    
    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: int


class JSONVote(JSONResult):
    data: Vote
    
    class Config:
        from_attributes = True
        

# USERS: Schema


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


class DetailsOut(BaseModel):
    name: str
    surname: str
    address: str
    mobile_no: int
    dob: datetime
    gender: str

    class Config:
        from_attributes = True


class JSONDetailsOut(JSONResult):
    data: DetailsOut
    
    class Config:
        from_attributes = True


class UserData(BaseModel):
    user: UserOut
    details: DetailsOut

    class Config:
        from_attributes = True


class PatientProfile(BaseModel):
    name: str
    surname: str
    dob: datetime
    address: str 
    mobile_no: int
    gender: str
    
    class Config:
        from_attributes = True


class DoctorProfile(PatientProfile):
    qualification: str
    registration_no: str
    year_of_registration: datetime
    state_medical_council: str
    specialization: str

    class Config:
        from_attributes = True


class JSONPatientProfile(JSONResult):
    data: PatientProfile
    
    class Config:
        from_attributes = True
        

class JSONDoctorProfile(JSONResult):
    data: DoctorProfile
    
    class Config:
        from_attributes = True


class JSONUserData(JSONResult):
    data: UserData
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class JSONToken(JSONResult):
    name: str
    data: Token
    
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    id: Optional[str] = None


# REATINGS: Schema


class RatingCreate(BaseModel):
    rating: float
    review: str
    doctor_id: int


class RatingOut(BaseModel):
    rating: float
    review: str

    class Config:
        from_attributes = True


class JSONRatingOut(JSONResult):
    data: RatingOut
    
    class Config:
        from_attributes = True


class RatingResponse(BaseModel):
    doctor_id: int
    average_rating: float
    Ratings: List[RatingOut]

    class Config:
        from_attributes = True


class JSONRatingResponse(JSONResult):
    data: RatingResponse
    
    class Config:
        from_attributes = True


class JSONListRatingResponse(JSONResult):
    data: List[RatingResponse]
    
    class Config:
        from_attributes = True
        

# DISEASE: Schema


class DiseaseCreate(BaseModel):
    no_of_symptoms: int
    symptoms: List[str]
    

class DiseaseOut(BaseModel):
    id: int
    diseasename: str
    confidence: float
    symptoms: List[str]
    consultdoctor: str
    
    class Config:
        from_attributes = True


class JSONDiseaseOut(JSONResult):
    data: DiseaseOut
    
    class Config:
        from_attributes = True
        
class JSONListDiseaseOut(JSONResult):
    data: List[DiseaseOut]
    
    class Config:
        from_attributes = True


# CONSULTATION: Schema

 
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


class JSONConsultationOut(JSONResult):
    data: ConsultationOut
    
    class Config:
        from_attributes = True
        

class ConsultationResponse(BaseModel):
    count: int
    Consultations: List[ConsultationOut]
    
    class Config:
        from_attributes = True
        

class JSONConsultationResponse(JSONResult):
    data: ConsultationResponse
    
    class Config:
        from_attributes = True

class ConsultationHistory(BaseModel):
    consultation_id: int
    consultation_date: datetime
    status: str
    diseaseinfo: DiseaseOut
    
    class Config:
        from_attributes = True

class PatientConsultationOut(BaseModel):
    consultation_id: int
    consultation_date: datetime
    status: str
    patient: PatientOut
    doctor: DoctorOut
    diseaseinfo: DiseaseOut
    
    class Config:
        from_attributes = True
       

class JSONPatientConsultationOut(JSONResult):
    data: PatientConsultationOut
    
    class Config:
        from_attributes = True


class PatientConsultationResponse(BaseModel):
    count: int
    Consultations: List[ConsultationHistory]
    
    class Config:
        from_attributes = True    
        

class JSONPatientConsultationResponse(JSONResult):
    data: PatientConsultationResponse
    
    class Config:
        from_attributes = True
        

class DoctorConsultationOut(BaseModel):
    consultation_id: int
    consultation_date: datetime
    status: str
    patient: PatientOut
    doctor: DoctorOut
    diseaseinfo: DiseaseOut
    
    class Config:
        from_attributes = True


class JSONDoctorConsultationOut(JSONResult):
    data: DoctorConsultationOut
    
    class Config:
        from_attributes = True

        
class DoctorConsultationResponse(BaseModel):
    count: int
    Consultations: List[ConsultationHistory]
    
    class Config:
        from_attributes = True 


class JSONDoctorConsultationResponse(JSONResult):
    data: DoctorConsultationResponse
    
    class Config:
        from_attributes = True


# CHATS: Schema
        

class Chat(BaseModel):
    message: str


class ChatOut(BaseModel):
    consultation_id: int
    created_at: datetime
    message: str
    sender_id: int
    class Config:
        from_attributes = True
  

class JSONChatOut(JSONResult):
    data: ChatOut
    
    class Config:
        from_attributes = True


class ChatList(BaseModel):
    consultation_id: int
    status: str
    chats: list[ChatOut]
    class Config:
        from_attributes = True


class JSONChatList(JSONResult):
    data: ChatList
    
    class Config:
        from_attributes = True


class FeedbackCreate(BaseModel):
    feedback: str


class FeedbackOutput(BaseModel):
    id: int
    created_at: datetime
    feedback: str
    
    class Config:
        from_attributes = True


class JSONFeedbackOutput(JSONResult):
    data: FeedbackOutput
    
    class Config:
        from_attributes = True


class Sender(BaseModel):
    name: str
    surname: str
    
    class Config:
        from_attributes = True


class JSONSender(JSONResult):
    data: Sender
    
    class Config:
        from_attributes = True


class FeedbackOut(FeedbackCreate):
    sender: Sender
    
    class Config:
        from_attributes = True


class JSONFeedbackOut(JSONResult):
    data: FeedbackOut
    
    class Config:
        from_attributes = True

class FeedbackResponse(BaseModel):
    doctor_id: int
    FeedBacks: List[FeedbackOut]

    
    class Config:
        from_attributes = True

class JSONFeedbackResponse(JSONResult):
    data: FeedbackResponse
    
    class Config:
        from_attributes = True

class AdminDiseaseInfo(BaseModel):
    id: int
    patient_id: Optional[int]
    diseasename: str
    no_of_symp: int
    symptoms: list[str]
    confidence: float
    consultdoctor: str
    consultation_date: Optional[datetime]
    status: Optional[str]
    
    class Config:
        from_attributes = True


class JSONAdminDiseaseInfo(JSONResult):
    data: list[AdminDiseaseInfo]

    class Config:
        from_attributes = True