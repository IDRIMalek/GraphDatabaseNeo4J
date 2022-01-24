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

app = FastAPI(title='Stack Overflow Tag Network')

security = HTTPBasic()

users_db = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

driver = GraphDatabase.driver('bolt://0.0.0.0:7687',
                              auth=('neo4j', 'neo4j'))

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

@app.post('/listtechno')
def listtechno(username: str = Depends(get_current_username)):
    query='Match (n:language) Return n.name;'
    with driver.session() as session:
        result=session.run(query).data()
    return {'results': result}

@app.post('/listgroup')
def listgroup(username: str = Depends(get_current_username)):
    query='Match (n) Return distinct(labels(n));'
    with driver.session() as session:
        result=session.run(query).data()
    return {'results': result}

@app.post('/listlink')
def listlink(username: str = Depends(get_current_username)):
    query='MATCH (n)-[l]-(m)RETURN distinct(TYPE(l));'
    with driver.session() as session:
        result=session.run(query).data()
    return {'results': result}

@app.post('/addtechno')
def addtechno(name, label, name_to, label_to , link_type, username: str = Depends(get_current_username)):

    query="MERGE (n:"+ label +"{name:'"+name+"',group:'custom', nodesize:'1'}) MERGE (m:"+ label_to +" {name:'"+name_to+"'}) MERGE (n)-[:"+link_type+"]->(m)Return n.name, ID(n);"
    with driver.session() as session:
        result=session.run(query).data()
    return {'node added': result}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
