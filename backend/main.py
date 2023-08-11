from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import os
import pinecone
PINECONE_API_KEY =  os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT") 
pinecone.init(api_key=PINECONE_API_KEY,
              environment=PINECONE_ENVIRONMENT)
try:
    print(pinecone.list_indexes())
except:
    print('PINECONE is not init!')
index = pinecone.Index('spr')

from Parser import GPTParser
parser = GPTParser()

import numpy as np

MARIA_DB_HOST = os.getenv("MARIA_DB_HOST") 
MARIA_DB_USER = os.getenv("MARIA_DB_USER") 
MARIA_DB_PASSWORD = os.getenv("MARIA_DB_PASSWORD") 

# Maria DB for saving user records
from db import DB
maria_db = DB(MARIA_DB_HOST, MARIA_DB_USER, MARIA_DB_PASSWORD)

# Reminder email
from mail import Email
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
sgclient = Email(SENDGRID_API_KEY)

# Data ingestion
from ingest import Ingestor
ingestor = Ingestor(index, parser)

# reCAPTHCA
# from recaptcha import reCAPTCHA
# recaptcha = reCAPTCHA()

app = FastAPI(
    title = 'SPR Profile Estimator',
    version='0.8',
    # openapi_url = None,
    # docs_url = None,
    redoc_url=None
)
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4000",
    "http://www.ichaoran.com",
    "https://www.ichaoran.com",
    "http://6chaoran.github.io",
    "https://6chaoran.github.io",
    "http://spr.chaoran.tk",
    "https://spr.chaoran.tk",
    "http://frontend-dot-sgprapp.et.r.appspot.com",
    "https://frontend-dot-sgprapp.et.r.appspot.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.mount("/favicon", StaticFiles(directory="favicon"), name="favicon")


@app.get("/version")
def read_root():
    version = "0.8"
    return f"SPR profile estimate v{version}"

@app.get("/")
def read_index():
    return FileResponse("./app.html")

@app.post("/get_matches")
def get_matches(text:str, request:Request) -> dict:
    v = parser.get_embedding(text)
    top_n = 5
    matches = index.query(
        vector=v,
        top_k=top_n,
        include_metadata=True,
        include_values=True
    )
    out = matches.to_dict()
    out = [i['metadata'] for i in out['matches']]
    n_pass = sum([i['result'] == "pass" for i in out])
    odds =  n_pass / top_n
    pred_decision = 'pass' if n_pass > 2 else 'rejected'
    durations = [i['duration'] for i in out if i['result'] == pred_decision]
    pred_duration = sum(durations) / len(durations)

    return {'matches': out, 'odds': odds, 'pred_decision': pred_decision, 'pred_duration': pred_duration}

@app.post("/add_record")
def add_record(username:str, password:str, text: str, email: str, status: str, applied_date:str, closed_date:str):
    msg = maria_db.add_row(username, password, email, status, text, applied_date, closed_date, mode="create")
    return msg

@app.post("/ingest")
def ingest(username, text, status, applied_date, closed_date, update_time):
    ingestor.ingest(username, text, status, applied_date, closed_date, update_time)

@app.post("/edit_record")
def add_record(username:str, password:str, text: str, email: str, status: str, applied_date:str, closed_date:str):
    msg = maria_db.add_row(username, password, email, status, text, applied_date, closed_date, mode="edit")
    return msg

@app.get("/list_records")
def list_records() -> list[dict]:
    return maria_db.fetch_all(nrows = 10)

@app.post("/send_email")
def send_email(recipient_email: str, 
               username: str,
               password: str,
               applied_date: str,
               description: str,
               closed_date: str,
               status: str) -> str:
    """
    recipient_email: str
    """
    from_email = 'SPR Predictor <sprservice@ichaoran.com>'
    template_id ='d-c74e706457894ff5947350366dec104f'
    data=  {'username': username,
        "password": password,
        "applied_date": applied_date,
        "description": description,
        "closed_date": closed_date,
        "status": status }
    return sgclient.send_mail(from_email, 
                              recipient_email, 
                              template_id, 
                              data)

@app.post('/verify_user')
def verify_user(username, password):
    return maria_db.verify_user(username, password)


@app.on_event('shutdown')
async def shutdown_event():
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)