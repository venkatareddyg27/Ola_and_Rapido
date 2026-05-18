# app/main.py

from fastapi import FastAPI

from app.core.database import Base, engine

# Import Models
from app.models.user import User
from app.models.parcel import Parcel


# Create Tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Ola Rapido Backend"
)


@app.get("/")
def home():
    return {
        "message": "Backend Running Successfully"
    }