import heapq
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from itertools import combinations
from haversine import haversine, Unit


class Node:
    def __init__(self, lat, lon, cost=0, parent=None):
        self.lat = lat
        self.lon = lon
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost


def haversine_distance(lat1, lon1, lat2, lon2):
    # coord1 e coord2 devono essere tuple (latitudine, longitudine)
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    distance = haversine(coord1, coord2, unit=Unit.KILOMETERS)
    return distance


def a_star(start, goal, graph):
    open_set = [start]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)
        print(current_node.lat, current_node.lon)
        if (current_node.lat, current_node.lon) == (goal.lat, goal.lon):
            path = []
            while current_node:
                print("ci siamo!")
                path.append((current_node.lat, current_node.lon))
                current_node = current_node.parent
            return path[::-1]

        closed_set.add((current_node.lat, current_node.lon))

        for neighbor in graph[(current_node.lat, current_node.lon)]:
            if neighbor not in closed_set:
                g_score = current_node.cost + haversine_distance(current_node.lat, current_node.lon, neighbor[0], neighbor[1])  # 0 e 1 indicano lat e lon di neighbor
                h_score = haversine_distance(neighbor[0], neighbor[1], goal.lat, goal.lon)
                f_score = g_score + h_score

                neighbor_node = Node(neighbor[0], neighbor[1], f_score, current_node)

                if neighbor_node not in open_set:
                    heapq.heappush(open_set, neighbor_node)

    return None  # If no path is found


# Punto di inizio e punto di fine
start_point = Node(lat=39.4304979,
                   lon=-0.335182)
end_point = Node(lat=39.4242263,
                 lon=-0.3141018)
"""
# legge il foglio Excel con pandas
file_path = 'coordinatePerProva.xlsx'  # Modifica il percorso del tuo file Excel
df = pd.read_excel(file_path, names=['latitudine', 'longitudine'])

# Rimuove le istanze duplicate nel DataFrame
df_no_duplicates = df.drop_duplicates(subset=['latitudine', 'longitudine'])
"""
# legge il file csv con pandas
file_path = "coordinateOK1.csv"
df = pd.read_csv(file_path, names=['latitudine', 'longitudine'])

# converte le colonne in numeri e gestisci eventuali errori
df['latitudine'] = pd.to_numeric(df['latitudine'], errors='coerce')
df['longitudine'] = pd.to_numeric(df['longitudine'], errors='coerce')

# rimuove le istanze duplicate nel DataFrame dopo la conversione numerica
df_no_duplicates = df.drop_duplicates(subset=['latitudine', 'longitudine']).copy()

# rimuove le righe con dati mancanti nelle colonne numeriche
df_no_duplicates = df_no_duplicates.dropna(subset=['latitudine', 'longitudine'])

# converte il DataFrame senza duplicati in una lista di tuple (coordinate)
dataset = [(row['latitudine'], row['longitudine']) for index, row in df_no_duplicates.iterrows()]

graph = {coord: [] for coord in dataset}

# Utilizza itertools.combinations per ottenere tutte le coppie uniche di coordinate
for coord1, coord2 in combinations(dataset, 2):
    if haversine_distance(coord1[0], coord1[1], coord2[0], coord2[1]) < 1.0:  # Soglia di 45 m per decidere i vicini di punto
        graph[coord1].append(coord2)
        graph[coord2].append(coord1)

# lista contenente il percorso ottimale
path = a_star(start_point, end_point, graph)

if path:
    print("Percorso ottimale:")
    for point in path:
        print(point)
else:
    print("Nessun percorso trovato.")
