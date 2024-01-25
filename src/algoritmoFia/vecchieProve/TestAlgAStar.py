import heapq
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

class Node:
    def __init__(self, lat, lon, cost=0, parent=None):
        self.lat = lat
        self.lon = lon
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def a_star(start, goal, graph):
    open_set = [start]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)

        if (current_node.lat, current_node.lon) == (goal.lat, goal.lon):
            path = []
            while current_node:
                path.append((current_node.lat, current_node.lon))
                current_node = current_node.parent
            return path[::-1]

        closed_set.add((current_node.lat, current_node.lon))

        for neighbor in graph[(current_node.lat, current_node.lon)]:
            if neighbor not in closed_set:
                g_score = current_node.cost + haversine(current_node.lat, current_node.lon, neighbor[0], neighbor[1]) #0 e 1 indicano lat e lon di neighbor
                h_score = haversine(neighbor[0], neighbor[1], goal.lat, goal.lon)
                f_score = g_score + h_score

                neighbor_node = Node(neighbor[0], neighbor[1], f_score, current_node)

                if neighbor_node not in open_set:
                    heapq.heappush(open_set, neighbor_node)

    return None  # If no path is found

#Punto di inizio e punto di fine
start_point = (39.43053, -0.33519)
end_point = (39.4242263, -0.3141018)

# Leggi il foglio Excel con pandas
file_path = 'coordinate.xlsx'  # Modifica il percorso del tuo file Excel
df = pd.read_excel(file_path, names=['latitudine', 'longitudine'])

# Converti il DataFrame in una lista di tuple (coordinate)
dataset = [(row['latitudine'], row['longitudine']) for index, row in df.iterrows()]

graph = {coord: [] for coord in dataset}
for coord in dataset:
    for other_coord in dataset:
        if coord != other_coord:
            # Aggiungi il vicino solo se la distanza è inferiore a una soglia (puoi regolare la soglia a tuo piacimento)
            if haversine(coord[0], coord[1], other_coord[0], other_coord[1]) < 4.0:  # Soglia di 4.0 km
                graph[coord].append(other_coord)

#lista contenente il percorso ottimale
path = a_star(Node(*start_point), Node(*end_point), graph)

"""
# Esempio di utilizzo
start_point = Node(40.7128, -74.0060)  # Esempio: New York City
end_point = Node(34.0522, -118.2437)   # Esempio: Los Angeles

# Grafo rappresentato come un dizionario, dove le chiavi sono le coordinate e i valori sono i vicini
graph = {
    (40.7128, -74.0060): [(34.0522, -118.2437), (41.8781, -87.6298)],  # Esempio: New York City
    (34.0522, -118.2437): [(40.7128, -74.0060), (41.8781, -87.6298)],  # Esempio: Los Angeles
    (41.8781, -87.6298): [(40.7128, -74.0060), (34.0522, -118.2437)]   # Esempio: Chicago
}

path = a_star(start_point, end_point, graph)
"""

if path:
    print("Percorso ottimale:")
    for point in path:
        print(point)
else:
    print("Nessun percorso trovato.")
