from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

class ActualUrl(BaseModel):
    original_url:str

class UrlData(BaseModel):
    original_url:str
    short_url:str
    created_at:datetime
    expires_at:datetime

print(UrlData({
    "original_url":"str",
}))

app = FastAPI()

@app.get("/")
def root():
    return "Hello"

@app.post("/generate_shorturl")
def generate_shorturl(actualurl:ActualUrl):
    print(actualurl.original_url)
    return "IN generate short url function"