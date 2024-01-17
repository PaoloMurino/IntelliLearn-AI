import heapq
import math

import pandas as pd


def calculate_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance

def a_star_search(graph, start, goal):
    heap = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while heap:
        current_cost, current_node = heapq.heappop(heap)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path_coordinates = [came_from[coord] for coord in list(reversed(path))[:-1]]
            print("Came from:")
            print(path_coordinates)
            return came_from

        for neighbor in graph[current_node]:
            new_cost = cost_so_far[current_node] + calculate_distance(current_node, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + calculate_distance(neighbor, goal)
                heapq.heappush(heap, (priority, neighbor))
                came_from[neighbor] = current_node

    return None

# Leggi il foglio Excel con pandas
file_path = 'coordinate.xlsx'  # Modifica il percorso del tuo file Excel
df = pd.read_excel(file_path, names=['latitudine', 'longitudine'])

# Converti il DataFrame in una lista di tuple (coordinate)
dataset = [(row['latitudine'], row['longitudine']) for index, row in df.iterrows()]

# Punto di inizio e punto di fine
punto_inizio = (39.43053, -0.33519)
punto_fine = (39.4242263, -0.3141018)

# Costruisci il grafo
graph = {coord: [other_coord for other_coord in dataset if other_coord != coord] for coord in dataset}

# Trova il percorso ottimale
path = a_star_search(graph, punto_inizio, punto_fine)

# Crea un nuovo DataFrame per il percorso ottimale
path_df = pd.DataFrame(path, columns=['latitudine', 'longitudine'])

# Salva il nuovo DataFrame in un file Excel
output_file_path = 'percorso_ottimale.xlsx'  # Modifica il percorso del tuo file di output
path_df.to_excel(output_file_path, index=False)

print("Percorso ottimale:", path)
