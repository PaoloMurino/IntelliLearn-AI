import osmnx as ox
import random
import pandas as pd

# Funzione per ottenere coordinate casuali lungo le strade
def generate_random_coordinates_along_roads(graph, num_points):
    # Lista per memorizzare le coordinate generate
    coordinates = []

    for _ in range(num_points):
        # Seleziona un segmento di strada casuale dal grafo
        edge = random.choice(list(graph.edges(keys=True)))

        # Estrai coordinate casuali lungo il segmento di strada
        point = ox.distance.nearest_edges(graph, (random.uniform(edge[0][1], edge[1][1]),
                                                     random.uniform(edge[0][0], edge[1][0])))

        coordinates.append((point[1], point[0]))

    return coordinates

# Imposta la città di Valencia come area di interesse
place_name = "Valencia, Spain"
graph = ox.graph_from_place(place_name, network_type="all")
# Specifica il numero di punti desiderato nel dataset
num_points = 100
# Genera il dataset di coordinate casuali
dataset = generate_random_coordinates_along_roads(graph, num_points)

# Creare un DataFrame con pandas
df = pd.DataFrame(dataset, columns=['Latitude', 'Longitude'])

# Salva il DataFrame in un file Excel
excel_file_path = 'porto_valencia_coordinates.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"Dataset salvato con successo in {excel_file_path}")
