from math import log

import networkx as nx


def analisiComplessita(graph):
    V = len(graph)  # Numero totale di nodi
    E = sum(len(neighbors) for neighbors in graph.values())  # Numero totale di archi

    # Complessità temporale
    time_complexity = (V + E) * log(V)

    return time_complexity
