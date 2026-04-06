from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import timedelta, datetime
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends

from models import URL
import string, random
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
EXPIRY_SECONDS = int(config.get("app", "ttl"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_expiry_time():
    return datetime.utcnow() + timedelta(seconds=EXPIRY_SECONDS)

class ActualUrl(BaseModel):
    original_url:str

class ShortCode(BaseModel):
    short_code:str

app = FastAPI()

@app.get("/")
def root():
    return "Hello"

@app.post("/generate_shorturl")
def generate_shorturl(actualurl:ActualUrl, req: Request, db: Session = Depends(get_db)):
    print(req.base_url)
    db_url = URL(
        original_url=actualurl.original_url,
        short_url_code=f"{generate_short_code()}",
        expires_at=get_expiry_time()
    )

    db.add(db_url)       # stage insert
    db.commit()          # save to DB
    db.refresh(db_url)   # get updated data (like id)

    return {"short_url":f"{req.base_url}go/{db_url.short_url_code}"}

@app.post("/")
def get_original_url(short_code:ShortCode, db: Session = Depends(get_db)):
    result = db.query(URL).filter(
        URL.short_url_code == short_code.short_code, 
    ).first()

    if result:
        if result.expires_at > datetime.utcnow():
            resp = {
                "original_url":result.original_url,
                "status":"success"
            }
        else:
            resp = {
                "message":"Link is expired!",
                "status":"failed"
            }
    else:
        resp = {
            "message":"No link found for this short url!",
            "status":"failed"
        }
    
    return resp