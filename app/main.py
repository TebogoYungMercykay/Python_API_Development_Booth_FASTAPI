from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import utils
from . import models
from .database import engine
from .routers import post, user, auth, consultations, disease_prediction, chats, admin
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return { "status": "welcomed", "id": utils.random_number(), "data": "Welcome, To The HealthConnect FastAPI" }

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(consultations.router)
app.include_router(disease_prediction.router)
app.include_router(chats.router)
app.include_router(post.router)