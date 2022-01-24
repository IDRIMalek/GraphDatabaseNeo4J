# Projet3
https://docs.google.com/document/d/1AK0o4QIazxQ2XIPxkwWi7nVdaK5SAu4R/edit


Projet DE #3 - Base de données & API de données


Cursus concerné : Data Engineer

Difficulté : 7 / 10

Description détaillée

L’objectif de ce projet est de choisir, mettre en place, et peupler une base de données à partir d’un jeu de données de l’open data, et d’implémenter une API vous permettant de requêter cette base de données.

Data

Vous êtes libres de choisir n’importe quel jeu de données accessible sur internet qui vous semble pertinent.

Vous pouvez notamment trouver des jeux de données sur kaggle : https://www.kaggle.com/datasets

Voici néanmoins une liste qui pourrait être intéressante :

https://www.kaggle.com/vardan95ghazaryan/top-250-football-transfers-from-2000-to-2018
https://data.world/datafiniti/electronic-products-and-pricing-data
https://data.world/promptcloud/fashion-products-on-amazon-com
https://www.kaggle.com/csanhueza/the-marvel-universe-social-network
https://www.kaggle.com/stackoverflow/stack-overflow-tag-network?select=stack_network_links.csv
https://www.kaggle.com/zynicide/wine-reviews?select=winemag-data-130k-v2.json
https://www.kaggle.com/abcsds/pokemon

Livrables attendus:

Vous devrez créer un repository GitHub contenant les livrables suivants :
Fichier README.md indiquant comment lancer votre projet.
Fichiers sources (csv, python, SQL, Dockerfile, docker-compose.yml)

Votre travail devra comprendre les éléments suivant:
Choix d’une base de données (et être capable de justifier ce choix) en fonction des données, parmi les bdd suivantes : ElasticSearch, relationnelle (MySQL ou PostgreSQL), Neo4J, MongoDB.
Scripts (sql, python, autre) pour peupler la base de données à partir du jeu de données.
API (FastAPI, Flask) permettant de requêter la base de données (et potentiellement d’ajouter de nouveaux éléments)
Potentiellement un fichier docker-compose.yml permettant de lancer les différents services (bdd, script de peuplement de la bdd, API) en même temps.
