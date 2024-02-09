import pandas as pd
import json
from haversine import haversine, Unit
from itertools import combinations


# utilizzo della formula di haversine per calcolare i vicini di ogni punto del dataset
def haversine_distance(lat1, lon1, lat2, lon2):
    # coord1 e coord2 devono essere tuple (latitudine, longitudine)
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    distance = haversine(coord1, coord2, unit=Unit.KILOMETERS)
    return distance
"""
# Leggi il foglio Excel con pandas
file_path = 'coordinatePerProva.xlsx'  # Modifica il percorso del tuo file Excel
df = pd.read_excel(file_path, names=['latitudine', 'longitudine'])
"""
file_path = "coordinateOK1.csv"
df = pd.read_csv(file_path, names=['latitudine', 'longitudine'])

# Converti le colonne in numeri e gestisci eventuali errori
df['latitudine'] = pd.to_numeric(df['latitudine'], errors='coerce')
df['longitudine'] = pd.to_numeric(df['longitudine'], errors='coerce')

# Rimuovi le istanze duplicate nel DataFrame dopo la conversione numerica
df_no_duplicates = df.drop_duplicates(subset=['latitudine', 'longitudine']).copy()

# Rimuovi le righe con dati mancanti nelle colonne numeriche
df_no_duplicates = df_no_duplicates.dropna(subset=['latitudine', 'longitudine'])


# Converti il DataFrame senza duplicati in una lista di tuple (coordinate)
dataset = [(row['latitudine'], row['longitudine']) for index, row in df_no_duplicates.iterrows()]

graph = {str(coord): [] for coord in dataset}  # Converti le tuple in stringhe

# Utilizza itertools.combinations per ottenere tutte le coppie uniche di coordinate
for coord1, coord2 in combinations(dataset, 2):
    if haversine_distance(coord1[0], coord1[1], coord2[0], coord2[1]) < 0.026:  # Soglia di 26 m
        graph[str(coord1)].append(str(coord2))
        graph[str(coord2)].append(str(coord1))

"""
graph = {coord: [] for coord in dataset}

# Utilizza itertools.combinations per ottenere tutte le coppie uniche di coordinate
for coord1, coord2 in combinations(dataset, 2):
    if haversine(coord1[0], coord1[1], coord2[0], coord2[1]) < 1.0:  # Soglia di 1.0 km per decidere i vicini di punto
        graph[coord1].append(coord2)
        graph[coord2].append(coord1)

print("Stampa del grafo:")
for point, neighbors in graph.items():
    print(f"{point} -> {neighbors}")
"""
# Salva il grafo in un file JSON
output_file_path = 'grafo_coordinate2.json'
with open(output_file_path, 'w') as json_file:
    json.dump(graph, json_file, indent=2)

print(f"Grafo salvato in '{output_file_path}'")