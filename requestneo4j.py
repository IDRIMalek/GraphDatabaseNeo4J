from neo4j import GraphDatabase

#connexion à la base de données
driver = GraphDatabase.driver('bolt://0.0.0.0:7687',
                              auth=('neo4j', 'neo4j'))


##~ASNIERESGENNEVILLIERSLESCOURTILLES
#x=647512.6733
#y=6870374.1848
##~BOBIGNYPANTINRAYMONDQUENEAU
#x2=657895.8989
#y2=6866354.1329999985

def Shortpath(x1,y1,x2,y2):

    #Requête pour ajouter les deux noeud temporaires
    query1 = '''
        MATCH (b:station)
        MERGE (a:tmp{name:'start', x:'''+str(x1)+''', y:'''+str(y1)+'''})
        MERGE (c:tmp{name:'end', x:'''+str(x2)+''', y:'''+str(y2)+'''})
        MERGE (a)-[:A_PIED {times:((SQRT((a.x-b.x)^2+(a.y-b.y)^2))/ (4000/3600) )}]->(b)
        MERGE (a)-[:A_PIED {times:((SQRT((a.x-c.x)^2+(a.y-c.y)^2))/ (4000/3600) )}]->(c)
        MERGE (b)-[:A_PIED {times:((SQRT((b.x-c.x)^2+(b.y-c.y)^2))/ (4000/3600) )}]->(c);
        '''
    #Requête Trouver les meilleurs itinéraires
    query2 = '''
        MATCH (a:tmp), (b:tmp)
        WHERE a.name='start' AND b.name='end'
        CALL gds.alpha.shortestPath.stream({
        nodeQuery: 'MATCH (n) RETURN id(n) as id',
        relationshipQuery: 'MATCH (n1)-[r]-(n2) RETURN id(r) as id, id(n1) as source, id(n2) as target, r.times as temps',
        startNode: a,
        endNode: b,
        relationshipWeightProperty: 'temps'
        })
        YIELD nodeId, cost
        WITH gds.util.asNode(nodeId) AS noeuds, collect(cost) AS Duree
        RETURN noeuds.name, noeuds.ligne, Duree
        '''
    #Requête pour supprimer les noeuds temporaires
    query3='MATCH (n:tmp) DETACH DELETE n;'


    with driver.session() as session:
        session.run(query1).data()
        result = session.run(query2).data()
        session.run(query3).data()

    return result

