import heapq

import pandas as pd
from geopy.distance import great_circle
from sklearn.neighbors import BallTree
import numpy as np

def costruisci_grafo(dati, soglia_distanza=1):
    grafo = {}

    # Verifica i nomi delle colonne nel DataFrame
    lat_col, lon_col = dati.columns

    coords = dati[[lat_col, lon_col]].to_numpy()
    coordinates = np.radians(coords)
    tree = BallTree(coordinates, metric='haversine')

    for i in range(len(dati)):
        nodo_attuale = tuple(np.round(coordinates[i], 6))  # Arrotonda a 6 decimali

        # Trova i vicini utilizzando BallTree
        distanze, indici_vicini = tree.query_radius([nodo_attuale], r=np.radians(soglia_distanza), return_distance=True)

        for distanza, j in zip(distanze[0], indici_vicini[0]):
            if i != j:
                nodo_successivo = tuple(np.round(coordinates[j], 6))  # Arrotonda a 6 decimali
                grafo.setdefault(nodo_attuale, []).append(nodo_successivo)
                grafo.setdefault(nodo_successivo, []).append(nodo_attuale)

    return grafo


def trova_percorso_ottimale(punto_inizio, punto_fine, grafo):
    coda_prioritaria = []
    heapq.heappush(coda_prioritaria, (0, punto_inizio))  # (costo totale, nodo)
    distanze = {nodo: float('infinity') for nodo in grafo}
    distanze[punto_inizio] = 0
    predecessori = {nodo: None for nodo in grafo}

    while coda_prioritaria:
        costo_totale, nodo_attuale = heapq.heappop(coda_prioritaria)

        if nodo_attuale == punto_fine:
            percorso_ottimale = []
            while nodo_attuale is not None:
                percorso_ottimale.append(nodo_attuale)
                nodo_attuale = predecessori[nodo_attuale]
            return percorso_ottimale[::-1]

        for vicino in grafo[nodo_attuale]:
            nuova_distanza = distanze[nodo_attuale] + great_circle(np.degrees(nodo_attuale), np.degrees(vicino)).kilometers
            if nuova_distanza < distanze[vicino]:
                distanze[vicino] = nuova_distanza
                costo_totale = nuova_distanza + great_circle(np.degrees(vicino), np.degrees(punto_fine)).kilometers
                predecessori[vicino] = nodo_attuale
                heapq.heappush(coda_prioritaria, (costo_totale, vicino))

    return None


# Leggi i dati dal file Excel
dati = pd.read_excel("coordinate.xlsx")

# Seleziona il punto di inizio e di fine dal dataset
punto_inizio = (39.43052, -0.33519)
punto_fine = (39.42422, -0.3141)

# Costruisci il grafo una sola volta
grafo = costruisci_grafo(dati)

# Arrotondamento a 6 decimali per punto_inizio e punto_fine
punto_inizio = tuple(np.round(np.radians(punto_inizio), 6))
punto_fine = tuple(np.round(np.radians(punto_fine), 6))

# Trova il percorso ottimale
percorso_ottimale = trova_percorso_ottimale(punto_inizio, punto_fine, grafo)

"""
# Trova il percorso ottimale
percorso_ottimale = trova_percorso_ottimale(tuple(np.radians(punto_inizio)), tuple(np.radians(punto_fine)), grafo)
"""

# Crea un DataFrame con i risultati
risultati_df = pd.DataFrame(percorso_ottimale, columns=['latitudine', 'longitudine'])
risultati_df[['latitudine', 'longitudine']] = np.degrees(risultati_df[['latitudine', 'longitudine']])

# Salva il DataFrame in un file Excel
risultati_df.to_excel("percorso_ottimale.xlsx", index=False)
print("Percorso ottimale:", percorso_ottimale)
