# PROJET 3

Here are the project instruction: 
 https://docs.google.com/document/d/1AK0o4QIazxQ2XIPxkwWi7nVdaK5SAu4R/edit

For the third step of datascience project we choose to use neo4j because it was the most exotic kind of database system. 
 We choose to populate this with the dataset of related software laguages from stackoverflow data team. 
https://www.kaggle.com/stackoverflow/stack-overflow-tag-network

We choose to call the little projet "Your cv on neo4j"

First of, you can lauch the project the the cmd below: 
>docker-compose up

Don't forget to change the bolt url bolt://0.0.0.0:7687 to  bolt://<ip_machine>:7687

Normaly you can now reach neo4j browser at: http://localhost:7474/browser/
Now you can load the datas from  stack-overflow-tag-network, the csv files are already in the import folder that is bridged to the container
https://www.kaggle.com/stackoverflow/stack-overflow-tag-network

LOAD CSV WITH HEADERS FROM "file:///stack_network_nodes.csv" AS row 
MERGE (:language {name: row.name, 
                    group: row.group, 
                    nodesize: row.nodesize });

LOAD CSV WITH HEADERS FROM "file:///stack_network_links.csv" AS row 
MATCH (a:language) WHERE a.name = row.source 
MATCH (b:language) WHERE b.name = row.target AND a.name <> b.name
MERGE (a)-[l:link {value:row.value} ]->(b);


Nous avons créer une API avec  FAST API. 
Dans un premier temps, il faut créer un envirronement virtuel: 
>sudo apt-get install python3-venv
>python3 -m venv .
>source bin/activate
Charger les librairies Python se trouvant dans requirements.txt:
> pip install -r requirements.txt

Lancer l'api:
> uvicorn api:app --reload
Se rendre sur l'api en local
>http://127.0.0.1:8000/docs#
Pour s'identifier il faut utiliser l'identifiant: 
>l'identifiant:"alice" et me mot de passe: "wonderland"
Aller sur le chemin 
>"http://127.0.0.1:8000/docs#/default/itineraire_itineraire_post


![alt text](https://github.com/IDRIMalek/Projet3/blob/main/example.png?raw=true)

Here the result

![alt text](https://github.com/IDRIMalek/Projet3/blob/main/example2.png?raw=true)

We could have gone much futher like, having sectors nodes, adding properties to nodes, like: availablities of canditdates, having vizualisation...