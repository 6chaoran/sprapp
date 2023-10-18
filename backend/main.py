from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import os

from Parser import GPTParser
parser = GPTParser()

import numpy as np

# Supabase DB (PostgreSQL)
SUPABASE_PASSWORD = os.getenv('SUPABASE_PASSWORD')
from db2 import DB as Supabase
supabase = Supabase(SUPABASE_PASSWORD)

# Reminder email
from mail import Email
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
sgclient = Email(SENDGRID_API_KEY)


# reCAPTHCA
# from recaptcha import reCAPTCHA
# recaptcha = reCAPTCHA()

from response_models import PRRecord, Matches, AddStatus, CRUDStatus, UserExist

app = FastAPI(
    title = 'SPR Profile Estimator',
    version='0.9',
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


@app.get("/api/v2/version")
def version():
    version = "v0.9"
    return version

@app.get("/api/v2/get_matches")
def api_get_matches2(text:str) -> Matches:
    v = parser.get_embedding(text)
    top_n = 5
    matches = supabase.get_similar_from_embedding(v)
    n_pass = sum([i['status'] == "pass" for i in matches])
    odds =  n_pass / top_n
    pred_decision = 'pass' if n_pass > 2 else 'rejected'
    durations = [i['duration'] for i in matches if i['status'] == pred_decision]
    pred_duration = sum(durations) / len(durations)
    return {'matches': matches, 'odds': odds, 'pred_decision': pred_decision, 'pred_duration': pred_duration}


@app.post("/api/v2/add_record")
def api_add_record2(username:str, password:str, text: str, email: str, status: str, applied_date:str, closed_date:str)  -> AddStatus:
    msg = supabase.add_row(username, password, email, status, text, applied_date, closed_date, mode="create", tablename='profile')
    return msg

@app.get("/api/v2/update_profile_latest")
def update_profile_latest() -> CRUDStatus:
    supabase.update_profile_latest()
    return {'status': 'ok'}


@app.put("/api/v2/ingest")
def ingest2(id, text) -> CRUDStatus:
    emb = parser.get_embedding(text)
    completion = parser.get_completion(text)
    compl_dict = parser.completion_to_dict(completion)
    extraction = compl_dict.get('extraction', {})
    description_en = compl_dict.get('english_translation', 'Apologies, something wrong with the translation')
    supabase.update_completion(id, emb, description_en)
    supabase.upload_extraction(id, extraction)
    supabase.update_profile_latest()
    return {'status': 'ok'}

@app.put("/api/v2/edit_record")
def api_edit_record2(username:str, password:str, text: str, email: str, status: str, applied_date:str, closed_date:str) -> AddStatus:
    msg = supabase.add_row(username, password, email, status, text, applied_date, closed_date, mode="edit", tablename='profile')
    supabase.update_profile_latest()
    return msg

@app.get("/api/v2/list_records")
def api_list_records2() -> list[PRRecord]:
    return supabase.api_fetch_all()

@app.delete("/api/v2/delete_record")
def api_delete_records(ids: list[str]) -> CRUDStatus:
    supabase.delete_records(ids)
    return {'status': 'ok'}

@app.get("/api/v2/list_user_records")
def api_list_user_records2(username: str) -> list[PRRecord]:
    res = supabase.list_user_records(username)
    return res

@app.post("/api/v2/send_email")
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


@app.get('/api/v2/verify_user')
def api_verify_user2(username, password):
    return supabase.verify_user(username, password)

@app.get('/api/v2/check_user_exist')
def api_check_user_exist2(username) -> UserExist:
    exist = supabase.check_user_exist(username)
    return {'exist': exist, 'username': username}

@app.on_event('shutdown')
async def shutdown_event():
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
