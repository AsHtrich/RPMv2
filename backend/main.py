from typing import List
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas, models as _models
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import HTTPException,BackgroundTasks
import pandas as pd
import pickle
import io


app = _fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this if your frontend is served from a different origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
FILES_DIR = "files"

with open("./ml/model_iso_forest.pkl", "rb") as f:
    model = pickle.load(f)

def load_csv_data():
    return pd.read_csv("./data/heart.csv")
# channel_id = "2309020"
# read_api_key = "https://api.thingspeak.com/channels/2309020/feeds.json?results=1"

@app.post("/api/users")
async def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await _services.create_user(user, db)

    return await _services.create_token(user)

@app.post("/api/token")
async def generate_token(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user = await _services.authUser(form_data.username, form_data.password, db)
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
    return await _services.create_token(user)

@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user 

@app.get("/api/users", response_model=List[_schemas.User])
async def get_users(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_users(db=db)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

@app.post("/api/patients", response_model=_schemas.Patient)
async def create_patients(patient: _schemas.Patient, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db),):
    return await _services.create_patients(user=user, patient=patient, db=db)

@app.get("/api/patients", response_model=List[_schemas.Patient])
async def get_patients(db: _orm.Session = _fastapi.Depends(_services.get_db),user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
   return await _services.get_patients(db=db,user=user)

@app.get("/api/patients/{patID}", status_code=200)
async def get_patient( patID: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_item(item_id=patID, db=db, item_model=_models.Patients,item_id_attr=_models.Patients.patID)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

@app.post("/api/prescriptions/{patID}", response_model=_schemas.Presc)
async def create_prescs(patID: int,presc: _schemas.Presc, db: _orm.Session = _fastapi.Depends(_services.get_db),):
    return await _services.create_presc(patID=patID,presc=presc, db=db)

@app.get("/api/prescriptions/{patID}", response_model=List[_schemas.Presc])
async def get_prescs(patID: int,db: _orm.Session = _fastapi.Depends(_services.get_db)):
   return await _services.get_prescs(db=db,patID=patID)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

@app.get("/api/files")
async def list_files():
    # List files in the specified directory
    try:
        files = os.listdir(FILES_DIR)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error listing files")

@app.get("/api/files/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(FILES_DIR, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------

@app.post("/api/reports", response_model=_schemas.Requests)
async def reporter(report: _schemas.Requests, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.reporter(report=report,db=db)

@app.get("/api/stream_predictions")
async def stream_predictions(background_tasks: BackgroundTasks,db: _orm.Session = _fastapi.Depends(_services.get_db)):
    data = load_csv_data()  # Load CSV data
    response =  StreamingResponse(_services.generate_predictions(data=data,db=db), media_type="text/plain")
    return response

@app.get("/api/alerts", response_model=List[_schemas.Alerts])
async def get_alerts(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_alerts(db=db)

@app.get("/api/alerts/{aid}", status_code=200)
async def get_alert(aid: int,db: _orm.Session = _fastapi.Depends(_services.get_db)):
   return await _services.get_item(item_id=aid, db=db, item_model=_models.Alerts,item_id_attr=_models.Alerts.aid)


@app.get("/api/hrate")
async def get_heart_rate():
    """
    SSE Endpoint to stream heart rate data.
    """
    # Keep-alive for SSE with `chunked` transfer encoding
    response = StreamingResponse(
        _services.stream_csv_data(), 
        media_type="text/event-stream",
        headers={"Transfer-Encoding": "chunked"}
    )
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    return response










@app.get("/api")
async def root():
    return {"message": "Awsm CCM Application"}