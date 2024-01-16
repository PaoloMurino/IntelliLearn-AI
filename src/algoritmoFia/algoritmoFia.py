import pandas as pd
import heapq
import math

def calcola_distanza(lat1, lon1, lat2, lon2):
    # Formula di Haversine per calcolare la distanza geospaziale tra due punti dati latitudine e longitudine
    R = 6371  # Raggio medio della Terra in chilometri

    # Converte le latitudini e le longitudini da gradi a radianti
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calcola le differenze di latitudine e longitudine
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Calcola la distanza utilizzando la formula di Haversine
    a = math.sin(delta_lat / 2)*2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)*2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distanza = R * c

    return distanza

def euristica(lat1, lon1, lat2, lon2):
    # Puoi utilizzare la stessa formula di Haversine o altre euristiche basate sulla distanza geospaziale
    return calcola_distanza(lat1, lon1, lat2, lon2)

def costruisci_grafo(dati, soglia_distanza=0.4):
    grafo = {}

    for i in range(len(dati)):
        nodo_attuale = (dati['latitude'].iloc[i], dati['longitude'].iloc[i])

        # Aggiungi il nodo attuale al grafo se non è già presente
        if nodo_attuale not in grafo:
            grafo[nodo_attuale] = []

        # Cerca nodi vicini basati su distanza spaziale
        for j in range(len(dati)):
            if i != j:  # Assicurati di non confrontare il nodo con se stesso
                nodo_successivo = (dati['latitude'].iloc[j], dati['longitude'].iloc[j])
                distanza = calcola_distanza(nodo_attuale[0], nodo_attuale[1], nodo_successivo[0], nodo_successivo[1])

                if distanza < soglia_distanza:
                    # Aggiungi il nodo successivo al grafo se non è già presente
                    if nodo_successivo not in grafo:
                        grafo[nodo_successivo] = []

                    grafo[nodo_attuale].append(nodo_successivo)
                    grafo[nodo_successivo].append(nodo_attuale)

    return grafo


def trova_percorso_ottimale(punto_inizio, punto_fine, dati):
    grafo = costruisci_grafo(dati)

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
            nuova_distanza = distanze[nodo_attuale] + calcola_distanza(nodo_attuale[0], nodo_attuale[1], vicino[0], vicino[1])
            if nuova_distanza < distanze[vicino]:
                distanze[vicino] = nuova_distanza
                costo_totale = nuova_distanza + euristica(vicino[0], vicino[1], punto_fine[0], punto_fine[1])
                predecessori[vicino] = nodo_attuale
                heapq.heappush(coda_prioritaria, (costo_totale, vicino))

    return None  # Nessun percorso trovato

# Leggi i dati dal file Excel
dati = pd.read_excel("training/Valencia.xlsx")

punto_inizio = (39.43054, -0.33518)
punto_fine = (39.4507282, -0.3073923)
percorso_ottimale = trova_percorso_ottimale(punto_inizio, punto_fine, dati)

# Crea un DataFrame con i risultati
risultati_df = pd.DataFrame(percorso_ottimale, columns=['latitude', 'longitude'])

# Salva il DataFrame in un file Excel
risultati_df.to_excel("percorso_ottimale.xlsx", index=False)
print("Percorso ottimale:", percorso_ottimale)