# PROJET 3


## Introduction
Pour cette 3eme partie du projet demandé par Datascientest, nous avons choisi d'utiliser le système de base de données de neo4j. 
Nous trouvons que travailler avec neo4j nous demande de faire un effort particulier de reflexion car ce système nous oblige à réflechir l'orchestration des données de façon différente. 
Voici les instructions pour le projet 3: 
 https://docs.google.com/document/d/1AK0o4QIazxQ2XIPxkwWi7nVdaK5SAu4R/edit

Nous avons choisi de coupler le sujet avec le dataset de l'équipe data de stackoverflow, car nous trouvons assez intéressant de voir l'ecosystème des différentes technologies (language informatique) ainsi que leurs intéractions. 
https://www.kaggle.com/stackoverflow/stack-overflow-tag-network

Nous avons décidé d'appeler cette api "Your cv on neo4j"
En effet nous avons imaginer que les profiles des personnes pourraient être ajouter à ce type de base de données ainsi que les projets afin de connaître les disponibilité mais aussi les compétences qui matcheraient avec les projets. 

## Fonctionnement

Tout est gérer via un docker-compose qui lance la base de données neo4j, un tunnel en local permet d'accéder à l'interface via l'adresse suivante   http://localhost:7474/browser/  
username : neo4j 
password : neo4j

Puis ensuite l'api est accessible via cette adresse http://localhost:8000/docs#/ . 
L'api charge les noeuds et les liens du dataset de  stack-overflow-tag-network dans la base de donnée.
IL faut s'identifer avec les identifiants suivant: 
ID: "alice" 
MP: "wonderland"

Il est ensuite possible, via l'api de requêter: 
- Informations
    - listtechno : liste des noms des techologies.
    - listgroup : Liste des groupes des technologies.
    - listlink : liste des liens de ces technologies.
    - matchprojet: voir la compatibilitée entre un projet et un candidat.
- Interaction
    - addcandidate : possibiliter d'ajouter un candidat.
    - addprojet : possibiliter d'ajouter un projet.
    - delete : Suppression d'un noeud et de ses liaisons.

## Utilisation de l'api
Dans un premier temps il suffit de lancer le docker compose: 
>docker-compose up

Il ne faut pas oublier de changer l'ip bolt comme ceci: bolt://0.0.0.0:7687 to  bolt://<ip_machine>:7687

Normalement neo4j browser at: http://localhost:7474/browser/

Les CSV se trouvent dans le volume "/import" , ce volume et bridgé au dossier du même nom "/import" du container neo4j.  le chargement se fait donc automatiquement via l'api. 
https://www.kaggle.com/stackoverflow/stack-overflow-tag-network

## Illustrations: 


1-docker-compose:
![alt text](https://github.com/IDRIMalek/Projet3/blob/main/pictures/docker-compose.png)

2-Connexion neo4j
![alt text](https://github.com/IDRIMalek/Projet3/blob/main/pictures/neo4jconnexion.png)

3-Vue de l'ecosystème: 
![alt text](https://github.com/IDRIMalek/Projet3/blob/main/pictures/ecosystem.png)

4-Post candidate (ajouter un candidat): 
![alt text](https://github.com/IDRIMalek/Projet3/blob/main/pictures/candidate.png)

5-Post project (ajouter un projet): 
![alt text](https://github.com/IDRIMalek/Projet3/blob/main/pictures/projet.png)

6-Vue candidats et projets neo4j: 
![alt text](https://github.com/IDRIMalek/Projet3/blob/main/pictures/neo4jview.png)

7-Resultat requête "match": 
![alt text](https://github.com/IDRIMalek/Projet3/blob/main/pictures/matchview.png)

## Les difficultés rencontrées. 
- Le choix du système de base de données et du dataset à pris pas mal de temps, il y avait une certaine liberté dans cette étape du projet que nous avions pas dans les autres. ce qui peut être à double tranchant. 
- Lors du lancement du docker compose, l'api n'arivait pas à se connecter à la base de données car celle-ci n'était pas encore en service malgré le fait que nous aillont ajouter la dependence "depend_on" permetant de savoir si un container est actif avant d'en lancer un autre.  La solution a été d'ajouter le paramètre "healthcheck" qui permet de verifier si un service est veritablement en marche . 

## Aller plus loin
Nous arions put aller beaucoup plus loin, comme ajouter les secteurs d'activités, changer la propriété des noeuds des candidats afin de savoir s'ils sont disponibles, obtenir une visualisation sur une interface web a l'aide d'avec Neovis.js par exemple
https://neo4j.com/developer/tools-graph-visualization/. 
Ce projet est plein de perspectives mais pour le cahier des charges demandé par datascientest nous en sommes restés aux requêtes simples. 