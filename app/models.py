from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))


class Patient(Base):
    __tablename__ = "patients"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    is_patient = Column(Boolean, default=True)
    is_doctor = Column(Boolean, default=False)
    name = Column(String, nullable=False, max_length=50)
    dob = Column(DateTime, nullable=False)
    address = Column(String, nullable=False, max_length=100)
    mobile_no = Column(String, nullable=False, max_length=15)
    gender = Column(String, nullable=False, max_length=10)

    @property
    def age(self):
        today = datetime.now().date()
        age = today.year - self.dob.year
        if today.month < self.dob.month or (today.month == self.dob.month and today.day < self.dob.day):
            age -= 1
        return age


class Doctor(Base):
    __tablename__ = "doctors"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    is_patient = Column(Boolean, default=False)
    is_doctor = Column(Boolean, default=True)
    name = Column(String, nullable=False, max_length=50)
    dob = Column(DateTime, nullable=False)
    address = Column(String, nullable=False, max_length=100)
    mobile_no = Column(String, nullable=False, max_length=15)
    gender = Column(String, nullable=False, max_length=10)
    registration_no = Column(String, nullable=False, max_length=20)
    year_of_registration = Column(DateTime, nullable=False)
    qualification = Column(String, nullable=False, max_length=20)
    state_medical_council = Column(String, nullable=False, max_length=30)
    specialization = Column(String, nullable=False, max_length=30)
    rating = Column(Integer, default=0)


class DiseaseInfo(Base):
    __tablename__ = "diseaseinfos"

    id = Column(Integer, primary_key=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.user_id", ondelete="SET NULL"), nullable=True)
    diseasename = Column(String, nullable=False, max_length=200)
    no_of_symp = Column(Integer, nullable=False)
    symptomsname = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    consultdoctor = Column(String, nullable=False, max_length=200)


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.user_id", ondelete="SET NULL"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.user_id", ondelete="SET NULL"), nullable=True)
    diseaseinfo_id = Column(Integer, ForeignKey("diseaseinfos.id", ondelete="SET NULL"), nullable=True)
    consultation_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, max_length=20)


class PublicPost(Base):
    __tablename__ = "publicposts"

    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), default=1)
    post_header = Column(String, nullable=False, max_length=250)
    post_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))


class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("doctors.user_id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("publicposts.post_id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))


class RatingReview(Base):
    __tablename__ = "ratingreviews"

    id = Column(Integer, primary_key=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.user_id", ondelete="SET NULL"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.user_id", ondelete="SET NULL"), nullable=True)
    rating = Column(Integer, default=0)
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

    id = Column(Integer, primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text('now()'))
    consultation_id = Column(Integer, ForeignKey("consultations.id", ondelete="CASCADE"))
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    message = Column(Text, nullable=False)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text('now()'))
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    feedback = Column(Text, nullable=False)

