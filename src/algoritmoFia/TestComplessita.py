from math import log

import networkx as nx


def analisiComplessita(graph):
    V = len(graph)  # Numero totale di nodi
    E = sum(len(neighbors) for neighbors in graph.values())  # Numero totale di archi
    d = max(len(neighbors) for neighbors in graph.values())  # Massimo grado di un nodo

    # Complessità temporale
    time_complexity = (V + E) * log(V)

    # Complessità spaziale
    space_complexity = V

    return time_complexity, space_complexity

def isBilanciato(graph):

    thresholdValue = 0.5
    G = nx.Graph(graph)

    #----BIALNCIAMENTO DI GRADO----
    #Calcolo del grado di ciascun nodo
    degreeDistribution = [len(graph[node]) for node in graph]

    #Calcolo della media dei gradi
    averageDegree = sum(degreeDistribution)/len(degreeDistribution)

    #Verifica della distribuzione dei gradi
    balanced = all(abs(degree - averageDegree) <= thresholdValue for degree in degreeDistribution)

    #----BILANCIAMENTO DI NODI----
    #Trova i componenti connessi
    components = [list(component) for component in nx.connected_components(G)]

    # Calcola la media del numero di nodi nei componenti connessi
    averageNodeCount = sum(len(component) for component in components) / len(components)

    #Verifica se il numero di nodi è più o meno uguale
    balancedNodes = all(abs(len(component) - averageNodeCount) <= thresholdValue for component in components)

    #----BILANCIAMENTO DI ARCHI----
    #Calcolo del numero medio di archi dei nodi
    averageEdges = sum(len(edges) for edges in graph.values()) / len(graph)

    #Verifica se l'allocazione degli archi è uniforme
    balancedEdges = all(abs(len(edges) - averageEdges) <= thresholdValue for edges in graph.values())

    return balanced, balancedNodes, balancedEdges