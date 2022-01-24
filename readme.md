### PARTIE 1

# ----Création du graphe----------------------------------

# Chargement des noeuds
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/pauldechorgnat/cool-datasets/master/ratp/stations.csv" AS row
MERGE (:station {nom: row.nom_gare, 
                    x: toFloat(row.x), 
                    y: toFloat(row.y), 
                    name: row.nom_clean ,
                    Trafic: toInteger(row.Trafic), 
                    Ville: row.Ville,
                    ligne: row.ligne
});

# Chargement des relations DESSERT
LOAD CSV WITH HEADERS FROM "https://github.com/pauldechorgnat/cool-datasets/raw/master/ratp/liaisons.csv" AS row
MATCH (a:station) WHERE a.name = row.start
MATCH (b:station) WHERE b.name = row.stop AND b.ligne = a.ligne 
MERGE (a)-[l:DESSERT {ligne: row.ligne, times:(SQRT((a.x-b.x)^2+(a.y-b.y)^2)/  (40000/3600))}]-(b);

## liaisons entre station du même nom CORRESPONDANCE
MATCH (a:station) 
MATCH (b:station) WHERE a.nom = b.nom AND a.ligne <> b.ligne
MERGE (a)-[:CORRESPONDANCE {times:(4*60)}]-(b);

# Liaisons A PIED
MATCH (a:station)
MATCH (b:station) WHERE a.name<>b.name AND SQRT((a.x-b.x)^2+(a.y-b.y)^2)<1000 AND a.ligne <> b.ligne
MERGE (a)-[:A_PIED {times:((SQRT((a.x-b.x)^2+(a.y-b.y)^2))/ (4000/3600) )}]-(b)
RETURN a, b;




### PARTIE 2

# --------Exploration-------------------------------------

# -1---Quel est le nombre de correspondances par station ?

MATCH (a:station)-[r:CORRESPONDANCE]->(b)
WITH a, count(b) as nb_correspondance
RETURN DISTINCT a.name, nb_correspondance
ORDER BY nb_correspondance


# -2-Quel est le nombre de stations à moins de deux kilomètres de la station LADEFENSE (on pourra prendre la distance brute sans considération de relation) ?


MATCH (a: station {name: "LADEFENSE"})
MATCH (b: station {name:"CHATEAUDEVINCENNES"})
CALL gds.alpha.shortestPath.stream({
  nodeQuery: 'MATCH (n) RETURN id(n) as id',
  relationshipQuery: 'MATCH (n1)-[r]-(n2) RETURN id(r) as id, id(n1) as source, id(n2) as target, r.times as temps',
  startNode: a,
  endNode: b,
  relationshipWeightProperty: 'temps'
})
YIELD nodeId, cost
RETURN gds.util.asNode(nodeId).name AS Name, cost AS duree ORDER BY duree DESC LIMIT 1

# 1478.6 secondes >> 24.6 min

## -3-Combien de temps faut-il pour aller à pied de LADEFENSE à CHATEAUDEVINCENNES (on pourra considérer que tout le chemin se fait à pied, sans considération de relation) ?

MATCH (a: station {name: "LADEFENSE"})
MATCH (b: station {name:"CHATEAUDEVINCENNES"})
RETURN (SQRT((n.x-m.x)^2+(n.y-m.y)^2))/1.1

## 14397.88 s > 240 min > 4h

# -4-Est-il plus rapide de faire un changement à SAINTLAZARE pour aller de MONTPARNASSEBIENVENUE à GABRIELPERI ?

MATCH (a: station {name: "MONTPARNASSEBIENVENUE"})
MATCH (b: station {name:"GABRIELPERI"})
CALL gds.alpha.shortestPath.stream({
  nodeQuery: 'MATCH (n) RETURN id(n) as id',
  relationshipQuery: 'MATCH (n1)-[r]-(n2) RETURN id(r) as id, id(n1) as source, id(n2) as target, r.times as temps',
  startNode: a,
  endNode: b,
  relationshipWeightProperty: 'temps'
})
YIELD nodeId, cost
RETURN gds.util.asNode(nodeId).name AS Name, cost AS duree;


# Aucune des option produite par la procédure ShortestPath ne fait prendre de correspondance à SAINTLAZARE";



# -5-Combien de stations se trouvent dans un rayon de 10 stations par train autour de SAINTLAZARE  STLAZARE?

MATCH (a: station {name: "STLAZARE"})-[:DESSERT*..10]-(b:station) 
WHERE b.name <> "STLAZARE"
WITH count(DISTINCT(b.name)) as nb_station
RETURN nb_station

## 73 stations Sans correspondance

MATCH (a: station {name: "STLAZARE"})-[:DESSERT|CORRESPONDANCE*..10]-(b:station) 
WHERE b.name <> "STLAZARE"
WITH count(DISTINCT(b.name)) as nb_station
RETURN nb_station

# 198 stations

# -6-Combien de stations se trouvent dans un rayon de 20 minutes par train autour de SAINTLAZARE STLAZARE ?

MATCH p=(a: station {name: "STLAZARE"})-[r:DESSERT*..]-(b:station) 
UNWIND r as r2
WITH sum(r2.times) as t, b
WHERE t<(20*60) 
RETURN count(distinct(b.name))

# 65 stations sont à moins de 20min de STLAZARE




### PARTIE 3

# J'ai créer une API avec  FAST API. 
# Dans un premier temps, il faut créer un envirronement virtuel: 
>>sudo apt-get install python3-venv
>>python3 -m venv .
>>source bin/activate
# Charger les librairies Python se trouvant dans requirements.txt:
>> pip install -r requirements.txt
# Lancer l'api:
>> uvicorn api:app --reload
# Se rendre sur l'api en local
>>http://127.0.0.1:8000/docs#
# Pour s'identifier il faut utiliser l'identifiant: 
>>l'identifiant:"alice" et me mot de passe: "wonderland"
# Aller sur le chemin 
>>"http://127.0.0.1:8000/docs#/default/itineraire_itineraire_post
# Rentrer les coordonnées de départ (x1, y1) et d'arrivées (x2, y2)
>>Exemple : 
Depart
#x1=647512.6733
#y2=6870374.1848
Arrivée
#x2=657895.8989
#y2=6866354.1329999985


