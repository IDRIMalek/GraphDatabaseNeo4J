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

app = FastAPI(title='Compatibilities cv->project with neo4j')

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

@app.get('/listtechno',tags=["informations"])
def listtechno(username: str = Depends(get_current_username)):
    '''
    This query allow you to see all node languages. 
    '''
    query='Match (n:language) Return n.name;'
    with driver.session() as session:
        result=session.run(query).data()
    return {'results': result}

@app.get('/listgroup',tags=["informations"])
def listgroup(username: str = Depends(get_current_username)):
    '''
    This query allow you to see all kind of labels(groups). 
    '''
    query='Match (n) Return distinct(labels(n));'
    with driver.session() as session:
        result=session.run(query).data()
    return {'results': result}

@app.get('/listlink',tags=["informations"])
def listlink(username: str = Depends(get_current_username)):
    '''
    This query allow you to see all kind of relationships. 
    '''
    query='MATCH (n)-[l]-(m)RETURN distinct(TYPE(l));'
    with driver.session() as session:
        result=session.run(query).data()
    return {'results': result}

@app.post('/addcandidate',tags=["interaction"])
def addcandidate(name, skill , value,  username: str = Depends(get_current_username)):
    '''
    This query allow you to add skill(languages)a candidate. 
    '''
    name=name.lower()
    skill=skill.lower()
    query="MERGE (n:candidate{name:'"+name+"',group:'candidate', nodesize:'1'}) MERGE (m:language {name:'"+skill+"'}) CREATE (n)-[:link{value:"+value+"}]->(m) CREATE (m)-[:link{value:"+value+"}]->(n) Return n.name, ID(n);"
    with driver.session() as session:
        result=session.run(query).data()
    return {'node added': result}


@app.post('/addprojet',tags=["interaction"])
def addprojet(name, neededskill, value,  username: str = Depends(get_current_username)):
    '''
    This query allow you to add a project. 
    '''
    name=name.lower()
    neededskill=neededskill.lower()
    query="MERGE (n:project{name:'"+name+"',group:'project', nodesize:'1'}) MERGE (m:language {name:'"+neededskill+"'}) CREATE (n)-[:link{value:"+value+"}]->(m) CREATE (m)-[:link{value:"+value+"}]->(n)  Return n.name, ID(n);"
    with driver.session() as session:
        result=session.run(query).data()
    return {'node added': result}


@app.get('/matchprojet',tags=["informations"])
def matchprojet(username: str = Depends(get_current_username)):
    '''
    This query allow you to see nodes matching projects for all candidates, up to seconde degrees 
    '''
    query="""
MATCH (c:candidate)-[rc:link]->(sc:language)-[rc2:link]->(sc2:language) , (p:project)-[rp:link]->(sp:language)-[rp2:link]->(sp2:language) 
WITH collect(distinct sc.name) as l , collect(distinct sc2.name) as l2, collect(distinct sp.name) as lp , collect(distinct sp2.name) as lp2, c, p
WITH l, l2, lp, lp2, size(lp) as skillsneed, size(lp2) as skill2sneed, c, p
WITH [n IN l WHERE n IN lp ] as matchskills1, [n IN l2 WHERE n IN lp2 ]as matchskills2, skillsneed, skill2sneed, c, p
RETURN c.name as candidate, p.name as project, round(size(matchskills1))/skillsneed as first_degree_compatibility,round(size(matchskills2)/skill2sneed) as second_degree_compatibility, matchskills1, matchskills2
    """
    
    with driver.session() as session:
        result=session.run(query).data()
    return {'results': result}

@app.post('/delete',tags=["interaction"])
def delete(name,username: str = Depends(get_current_username)):

    '''
    This query allow you to one particular node. 
    '''
    name=name.lower()
    query="Match (n) WHERE n.name= '"+ name +"' DETACH DELETE n;"
    with driver.session() as session:
        result=session.run(query).data()
    return {'results': result}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
