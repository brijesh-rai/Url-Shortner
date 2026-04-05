from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends

# main.py
from models import URL
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
import string, random


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class ActualUrl(BaseModel):
    original_url:str

app = FastAPI()

@app.get("/")
def root():
    return "Hello"

@app.post("/generate_shorturl")
def generate_shorturl(actualurl:ActualUrl, db: Session = Depends(get_db)):

    db_url = URL(
        original_url=actualurl.original_url,
        short_url=f"http://localhost:8000/go/{generate_short_code()}"
    )

    db.add(db_url)       # stage insert
    db.commit()          # save to DB
    db.refresh(db_url)   # get updated data (like id)

    return {"short_url":db_url.short_url}