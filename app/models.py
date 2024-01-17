import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Float, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

# POSTS: Database Models

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)



class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("doctors.doctor_id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))


# USERS: Database Models

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    is_active = Column(Boolean, nullable=False, server_default='FALSE')
    is_superuser = Column(Boolean, nullable=False, server_default='FALSE')
    is_staff = Column(Boolean, nullable=False, server_default='FALSE')
    last_login = Column(DateTime(timezone=True), nullable=True, server_default=text('now()'))


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)    
    dob = Column(DateTime, nullable=False)
    address = Column(String(100), nullable=False)
    mobile_no = Column(String(15), nullable=True)
    gender = Column(String(10), nullable=False)
    is_patient = Column(Boolean, server_default='TRUE')
    is_doctor = Column(Boolean, server_default='FALSE')

    @property
    def age(self):
        today = datetime.now().date()
        age = today.year - self.dob.year
        if today.month < self.dob.month or (today.month == self.dob.month and today.day < self.dob.day):
            age -= 1
        return age


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    dob = Column(DateTime, nullable=False)
    address = Column(String(100), nullable=False)
    mobile_no = Column(String(15), nullable=True)
    gender = Column(String(10), nullable=False)
    qualification = Column(String(50), nullable=False)
    registration_no = Column(String(20), nullable=False)
    year_of_registration = Column(DateTime, nullable=False)
    state_medical_council = Column(String(50), nullable=False)
    specialization = Column(String(30), nullable=False)
    rating = Column(Integer, server_default='0')
    is_patient = Column(Boolean, server_default='FALSE')
    is_doctor = Column(Boolean, server_default='TRUE')


# Disease Information and Consultations: Database Models

class DiseaseInfo(Base):
    __tablename__ = "diseaseinfos"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="SET NULL"), nullable=True)
    diseasename = Column(String(200), nullable=False)
    no_of_symp = Column(Integer, nullable=False)
    symptoms = Column(ARRAY(String), nullable=False)
    confidence = Column(Float, nullable=False)
    consultdoctor = Column(String(200), nullable=False)


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="SET NULL"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id", ondelete="SET NULL"), nullable=True)
    diseaseinfo_id = Column(Integer, ForeignKey("diseaseinfos.id", ondelete="SET NULL"), nullable=True)
    consultation_date = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)


class RatingReview(Base):
    __tablename__ = "ratingreviews"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="SET NULL"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id", ondelete="SET NULL"), nullable=True)
    rating = Column(Integer, server_default='0')
    review = Column(Text, nullable=True)

    @property
    def rating_is(self):
        new_rating = 0
        rating_objs = RatingReview.query.filter_by(doctor_id=self.doctor_id).all()
        for i in rating_objs:
            new_rating += i.rating

        new_rating = new_rating / len(rating_objs)
        new_rating = int(new_rating)

        return new_rating


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))
    consultation_id = Column(Integer, ForeignKey("consultations.id", ondelete="CASCADE"))
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    message = Column(Text, nullable=False)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    receiver_id = Column(Integer, ForeignKey("doctors.doctor_id", ondelete="CASCADE"))
    feedback = Column(Text, nullable=False)

