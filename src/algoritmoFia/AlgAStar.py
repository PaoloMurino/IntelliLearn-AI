import heapq
import pandas as pd
from itertools import combinations
from haversine import haversine, Unit


# Definizione della classe Node per rappresentare i nodi nel grafo
class Node:
    def __init__(self, lat, lon, cost=0, parent=None):
        self.lat = lat  # Latitudine del nodo
        self.lon = lon  # Longitudine del nodo
        self.cost = cost  # Costo del percorso finora per raggiungere il nodo
        self.parent = parent  # Nodo genitore nel percorso

    def __lt__(self, other):
        return self.cost < other.cost  # Permette di confrontare nodi in base al costo

# Funzione per calcolare la distanza haversine tra due coordinate
def haversine_distance(lat1, lon1, lat2, lon2):
    coord1 = (lat1, lon1)  # Coordinata 1
    coord2 = (lat2, lon2)  # Coordinata 2
    distance = haversine(coord1, coord2, unit=Unit.KILOMETERS)  # Calcola la distanza
    return distance


# Algoritmo A* per trovare il percorso ottimale tra due punti
def a_star(start, goal, graph):
    open_set = [start]  # Inizializza l'insieme aperto con il nodo di partenza
    closed_set = set()  # Inizializza l'insieme chiuso vuoto

    while open_set:
        current_node = heapq.heappop(open_set)  # Estrae il nodo con il costo minimo dall'insieme aperto

        if (current_node.lat, current_node.lon) in closed_set:  # Se il nodo è già stato esplorato, salta
            continue

        if (current_node.lat, current_node.lon) == (goal.lat, goal.lon):  # Se il nodo corrente è il nodo di destinazione, costruisci e restituisci il percorso
            path = []
            while current_node:
                path.append((current_node.lat, current_node.lon))
                current_node = current_node.parent
            return path[::-1]

        closed_set.add((current_node.lat, current_node.lon))  # Aggiunge il nodo corrente all'insieme chiuso

        for neighbor in graph[(current_node.lat, current_node.lon)]:  # Scorre i vicini del nodo corrente
            if neighbor not in closed_set:  # Se il vicino non è stato esplorato
                g_score = current_node.cost + haversine_distance(current_node.lat, current_node.lon, neighbor[0], neighbor[1])  # Calcola il costo del percorso finora per raggiungere il vicino
                h_score = haversine_distance(neighbor[0], neighbor[1], goal.lat, goal.lon)  # Calcola l'euristica (distanza diretta al nodo di destinazione)
                f_score = g_score + h_score  # Calcola il punteggio totale (costo finora + euristica)

                neighbor_node = Node(neighbor[0], neighbor[1], f_score, current_node)  # Crea un nuovo nodo per il vicino

                if neighbor_node not in open_set:  # Se il vicino non è nell'insieme aperto, lo aggiunge
                    heapq.heappush(open_set, neighbor_node)

    return None  # Se nessun percorso viene trovato


# Definizione dei punti di partenza e di destinazione
start_point = Node(lat=39.4305577,
                   lon=-0.3351722)
end_point = Node(lat=39.4242222,
                 lon=-0.3140294)

# 39.4384956,-0.3037465 punto gate 3
# 39.441493,-0.3274658 punto gate 2
# 39.4242222,-0.3140294 punto gate 1


# Legge i dati delle coordinate da un file CSV e crea una lista di tuple (coordinate)
file_path = "coordinate.csv"
df = pd.read_csv(file_path, names=['latitudine', 'longitudine'])

# Converte la colonna della latitudine in numeri
df['latitudine'] = pd.to_numeric(df['latitudine'], errors='coerce')

# Converte la colonna della longitudine in numeri
df['longitudine'] = pd.to_numeric(df['longitudine'], errors='coerce')

# Rimuove le righe duplicate
df_no_duplicates = df.drop_duplicates(subset=['latitudine', 'longitudine']).copy()
# Rimuove le righe con dati mancanti
df_no_duplicates = df_no_duplicates.dropna(subset=['latitudine', 'longitudine'])

# Crea la lista delle coordinate
dataset = [(row['latitudine'], row['longitudine']) for index, row in df_no_duplicates.iterrows()]

# Crea il grafo rappresentato come un dizionario delle liste di adiacenza
graph = {coord: [] for coord in dataset}

# Trova le coppie di coordinate vicine e aggiunge gli archi al grafo
for coord1, coord2 in combinations(dataset, 2):
    if haversine_distance(coord1[0], coord1[1], coord2[0], coord2[1]) < 0.026:  # Soglia di 26 metri per decidere i vicini
        graph[coord1].append(coord2)
        graph[coord2].append(coord1)

# Trova il percorso ottimale utilizzando l'algoritmo A*
path = a_star(start_point, end_point, graph)

if path:
    # Crea un DataFrame dal percorso
    path_df = pd.DataFrame(path, columns=['latitudine', 'longitudine'])

    # Salva il DataFrame in un file CSV
    path_df.to_csv('percorso_ottimaleGate1.csv', index=False)
    print("Percorso ottimale salvato in 'percorso_ottimaleGate1.csv'")
else:
    print("Nessun percorso trovato.")