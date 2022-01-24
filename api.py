import uvicorn
import json
import secrets
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Optional
from pydantic import BaseModel
from neo4j import GraphDatabase
from requestneo4j import *

app = FastAPI(title='Stack Overflow Tag Network')

security = HTTPBasic()

users_db = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = True if credentials.username in users_db else False
    print("username", credentials.username)
    print("password", credentials.password)
    print("correct_username", correct_username)
    correct_password = False
    if (correct_username):
        correct_password = secrets.compare_digest(credentials.password, users_db[credentials.username])
        print("correct_password", correct_password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get('/')
def get_index():
    return {'data': 'hello world'}


@app.get('/status')
def get_status():
    return {
        'status': 'ready'
    }

@app.post('/itineraire')
def itineraire(x1:float,y1:float,x2:float,y2:float, username: str = Depends(get_current_username)):

    result=Shortpath(x1,y1,x2,y2)
    return {'results': result}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
