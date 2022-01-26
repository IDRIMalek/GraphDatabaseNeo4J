# PROJET 3


## Introduction
Pour cette 3eme partie du projet demandé par Datascientest, nous avons choisi d'utiliser le système de base de donnée de neo4j. 
Nous trouvons que travailler avec neo4j nous demande de faire un effort particulier de reflexion car ce système nous oblige à réflechire l'orchestration des données de façon différente. 
Voici les instructions pour le projet 3: 
 https://docs.google.com/document/d/1AK0o4QIazxQ2XIPxkwWi7nVdaK5SAu4R/edit

Nous avons choisi de coupler le sujet avec le dataset de l'équipe data de stackoverflow, car nous trouvons assez intéressant de voir l'ecosystème des différentes technologies (language informatique) ainsi que leurs intéractions. 
https://www.kaggle.com/stackoverflow/stack-overflow-tag-network

Nous avons décidé d'appeler cette api "Your cv on neo4j"
En effet nous avons imaginer que les profiles des personnes pourraient être ajouter à ce type de base de données ainsi que les projets afin de connaître les disponibilité mais aussi les compétences qui matcheraient avec les projets. 

## Fonctionnement

Tout est gérer via un docker-compose qui lance la base de données neo4j, un tunnel en local permet d'accéder à l'interface via l'adresse suivante   http://localhost:7474/browser/  puis ensuite l'api est accessible via cette adresse http://localhost:8000/docs#/ . 
L'api charge les noeuds et les liens du dataset de  stack-overflow-tag-network dans la base de donnée.
IL faut s'identifer avec les identifiants suivant: 
ID: "alice" MP: "wonderland"

Il est ensuite possible, via l'api de requêter: 
- Informations
    - listtechno : liste des noms des techologies
    - listgroup : Liste des groupes des technologies
    - listlink : liste des liens de ces technologies
    - matchprojet: voir la compatibilitée entre un projet et un candidat
- Interaction
    - addcandidate : possibiliter d'ajouter un candidat
    - addprojet : possibiliter d'ajouter un projet
    - delete : Suppersion d'un noeud et de ses liaisons
    
# Lancer l'api
Dans un premier temps il suffit de lancer le docker compose: 
>docker-compose up

Il ne faut pas oublier de changer l'ip bolt comme ceci: bolt://0.0.0.0:7687 to  bolt://<ip_machine>:7687

Normalement neo4j browser at: http://localhost:7474/browser/
Now you can load the datas from  stack-overflow-tag-network, the csv files are already in the import folder that is bridged to the container
https://www.kaggle.com/stackoverflow/stack-overflow-tag-network


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

Nous arrions pue aller beaucoup plus loin, comme ajouter les secteurs d'activités, changer la propriété des noeuds des candidats afin de savoir s'il étaient disponible, obtenir une visualisation sur une interface web à l'aide de avec Neovis.js par exemple
https://neo4j.com/developer/tools-graph-visualization/. 
Ce projet est plein de perspectives mais pour le cahier des charges demandé par datascientest nous en somme resté aux requêtes basiques. 