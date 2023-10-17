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

# Supabase DB (PostgreSQL)
SUPABASE_PASSWORD = os.getenv('SUPABASE_PASSWORD')
from db2 import DB as Supabase
supabase = Supabase(SUPABASE_PASSWORD)

# Reminder email
from mail import Email
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
sgclient = Email(SENDGRID_API_KEY)

# Data ingestion
from ingest import Ingestor
ingestor = Ingestor(index, parser)

from batch_ingest import BatchIngestor
import pandas as pd
from sqlalchemy import create_engine
port = 3306
schema = 'sgprapp'
engine = create_engine(f'mysql+mysqlconnector://{MARIA_DB_USER}:{MARIA_DB_PASSWORD}@{MARIA_DB_HOST}:{port}/{schema}', echo = False)
ingestor_b = BatchIngestor(parser, engine, maria_db, index, uat = True)

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
    "http://spr.ichaoran.com",
    "https://spr.ichaoran.com",
    "http://6chaoran.github.io",
    "https://6chaoran.github.io",
    "https://sgprapp.web.app",  # firebase
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

@app.get("/api/version")
def version():
    version = "v0.8"
    return version

@app.get("/")
def read_index():
    return FileResponse("./app.html")

@app.post("/api/v1/get_matches")
def api_get_matches(text:str, request:Request) -> dict:
    v = parser.get_embedding(text)
    top_n = 5
    matches = index.query(
        vector=v,
        top_k=top_n,
        include_metadata=True,
        include_values=True,
        namespace='spr',
        filter={
            'result': {"$in":['pass', 'rejected']},
            'duration': {"$gt": 0}
                }
    )
    out = matches.to_dict()
    out = [i['metadata'] for i in out['matches']]
    n_pass = sum([i['result'] == "pass" for i in out])
    odds =  n_pass / top_n
    pred_decision = 'pass' if n_pass > 2 else 'rejected'
    durations = [i['duration'] for i in out if i['result'] == pred_decision]
    pred_duration = sum(durations) / len(durations)

    return {'matches': out, 'odds': odds, 'pred_decision': pred_decision, 'pred_duration': pred_duration}

@app.post("/api/v2/get_matches")
def api_get_matches2(text:str, request:Request) -> dict:
    v = parser.get_embedding(text)
    top_n = 5
    # matches = index.query(
    #     vector=v,
    #     top_k=top_n,
    #     include_metadata=True,
    #     include_values=True,
    #     namespace='spr',
    #     filter={
    #         'result': {"$in":['pass', 'rejected']},
    #         'duration': {"$gt": 0}
    #             }
    # )
    matches = supabase.get_similar_from_embedding(v)
    # out = matches.to_dict()
    # out = [i['metadata'] for i in out['matches']]
    
    n_pass = sum([i['status'] == "pass" for i in matches])
    odds =  n_pass / top_n
    pred_decision = 'pass' if n_pass > 2 else 'rejected'
    durations = [i['duration'] for i in matches if i['status'] == pred_decision]
    pred_duration = sum(durations) / len(durations)

    return {'matches': matches, 'odds': odds, 'pred_decision': pred_decision, 'pred_duration': pred_duration}

@app.post("/add_record")
def add_record(username:str, password:str, text: str, email: str, status: str, applied_date:str, closed_date:str):
    msg = maria_db.add_row(username, password, email, status, text, applied_date, closed_date, mode="create", tablename='profile')
    _ = maria_db.add_row(username, password, email, status, text, applied_date, closed_date, mode="create", tablename='latest')
    return msg

@app.post("/api/v1/add_record")
def api_add_record(username:str, password:str, text: str, email: str, status: str, applied_date:str, closed_date:str):
    msg = maria_db.add_row(username, password, email, status, text, applied_date, closed_date, mode="create", tablename='profile')
    _ = maria_db.add_row(username, password, email, status, text, applied_date, closed_date, mode="create", tablename='latest')
    return msg

@app.post("/api/v2/add_record")
def api_add_record2(username:str, password:str, text: str, email: str, status: str, applied_date:str, closed_date:str):
    msg = supabase.add_row(username, password, email, status, text, applied_date, closed_date, mode="create", tablename='profile')
    _ = supabase.add_row(username, password, email, status, text, applied_date, closed_date, mode="create", tablename='latest')
    return msg

@app.post("/ingest")
def ingest(username, text, status, applied_date, closed_date, update_time):
    _ = ingestor.ingest(username, text, status, applied_date, closed_date, update_time)

@app.post("/api/v1/ingest")
def ingest_b(username, text, status, applied_date, closed_date, update_time):
    id = username + '-' + update_time
    row = pd.Series({
        'username': username,
        'description': text,
        'status': status,
        'applied_date': applied_date,
        'closed_date': closed_date,
        'update_ts': update_time,
        'id': id
    })
    _ = ingestor_b.ingest_row(row)


@app.post("/api/v2/ingest")
def ingest2(id, text):
    emb = parser.get_embedding(text)
    completion = parser.get_completion(text)
    compl_dict = parser.completion_to_dict(completion)
    extraction = compl_dict.get('extraction', {})
    description_en = compl_dict.get('english_translation', 'Apologies, something wrong with the translation')
    supabase.update_completion(id, emb, description_en)
    supabase.upload_extraction(id, extraction)
    return {'status': 'ok'}

@app.post("/api/v1/edit_record")
def api_edit_record(username:str, password:str, text: str, email: str, status: str, applied_date:str, closed_date:str):
    msg = maria_db.add_row(username, password, email, status, text, applied_date, closed_date, mode="edit", tablename='profile')
    maria_db.update_profile_latest()
    return msg

@app.post("/api/v2/edit_record")
def api_edit_record2(username:str, password:str, text: str, email: str, status: str, applied_date:str, closed_date:str):
    msg = supabase.add_row(username, password, email, status, text, applied_date, closed_date, mode="edit", tablename='profile')
    supabase.update_profile_latest()
    return msg

@app.get("/list_records")
def list_records() -> list[dict]:
    return maria_db.fetch_all(nrows = 10)

@app.get("/api/v1/list_records")
def api_list_records() -> list[dict]:
    return maria_db.api_fetch_all()

@app.get("/api/v2/list_records")
def api_list_records2() -> list[dict]:
    return supabase.api_fetch_all()


@app.get("/api/v2/delete_record")
def api_delete_record(id: str):
    supabase.delete_record(id)
    return {'status': 'ok'}

@app.post("/api/v1/send_email")
def api_send_email(recipient_email: str, 
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


@app.post('/api/v1/verify_user')
def api_verify_user(username, password):
    return maria_db.verify_user(username, password)

@app.post('/api/v2/verify_user')
def api_verify_user2(username, password):
    return supabase.verify_user(username, password)

@app.post('/api/v2/check_user_exist')
def api_check_user_exist2(username):
    exist = supabase.check_user_exist(username)
    return {'exist': exist}

@app.on_event('shutdown')
async def shutdown_event():
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
