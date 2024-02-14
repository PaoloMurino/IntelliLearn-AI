from haversine import haversine, Unit
from itertools import combinations


# utilizzo della formula di haversine per calcolare i vicini di ogni punto del dataset
def distanza_haversine(lat1, lon1, lat2, lon2):
    # coord1 e coord2 devono essere tuple (latitudine, longitudine)
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    distance = haversine(coord1, coord2, unit=Unit.KILOMETERS)
    return distance


def costruzione_grafo(dataset):
    # Crea il grafo rappresentato come un dizionario delle liste di adiacenza
    graph = {coord: [] for coord in dataset}

    # Trova le coppie di coordinate vicine e aggiunge gli archi al grafo
    for coord1, coord2 in combinations(dataset, 2):
        if distanza_haversine(coord1[0], coord1[1], coord2[0], coord2[1]) < 0.026:  # Soglia di 26 metri per decidere i vicini
            graph[coord1].append(coord2)
            graph[coord2].append(coord1)

    return graph
