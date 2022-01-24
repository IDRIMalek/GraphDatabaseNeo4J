# PROJET 3

# First of, you can lauch the project the the cmd below: 
>docker-compose up

#### Don't forget to change the bolt url bolt://0.0.0.0:7687 to  bolt://<ip_machine>:7687

### Normaly you can now reach neo4j browser at: http://localhost:7474/browser/
### Now you can load the datas from  stack-overflow-tag-network, the csv files are already in the import folder that is bridged to the container
https://www.kaggle.com/stackoverflow/stack-overflow-tag-network

>LOAD CSV WITH HEADERS FROM "file:///stack_network_nodes.csv" AS row 
>MERGE (:language {name: row.name, 
>                    group: row.group, 
>                    nodesize: row.nodesize });

LOAD CSV WITH HEADERS FROM "file:///stack_network_links.csv" AS row 
MATCH (a:language) WHERE a.name = row.source 
MATCH (b:language) WHERE b.name = row.target AND a.name <> b.name
MERGE (a)-[l:link {value:row.source} ]->(b);


## Nous avons créer une API avec  FAST API. 
## Dans un premier temps, il faut créer un envirronement virtuel: 
>>sudo apt-get install python3-venv
>>python3 -m venv .
>>source bin/activate
## Charger les librairies Python se trouvant dans requirements.txt:
>> pip install -r requirements.txt
## 

## Lancer l'api:
>> uvicorn api:app --reload
## Se rendre sur l'api en local
>>http://127.0.0.1:8000/docs#
## Pour s'identifier il faut utiliser l'identifiant: 
>>l'identifiant:"alice" et me mot de passe: "wonderland"
## Aller sur le chemin 
>>"http://127.0.0.1:8000/docs#/default/itineraire_itineraire_post



