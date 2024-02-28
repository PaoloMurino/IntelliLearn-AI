import pandas as pd
import matplotlib.pyplot as plt
from src.algoritmoFia.Node import Node
from src.algoritmoFia.CostruzioneGrafo import costruzione_grafo
import time

from src.algoritmoFia.Non_Informata.BFS import breadth_first_search
from src.algoritmoFia.Non_Informata.DFS import depth_first_search

def percorso_ottimale(gate):
    # Definizione del punto di partenza
    start_point = Node(lat=39.4305577, lon=-0.3351722)

    # Definizione del punto di destinazione
    if gate == 1:
        end_point = Node(lat=39.4242222, lon=-0.3140294)
    elif gate == 2:
        end_point = Node(lat=39.441493, lon=-0.3274658)
    elif gate == 3:
        end_point = Node(lat=39.4384956, lon=-0.3037465)
    else:
        raise ValueError("Il gate deve essere 1, 2 o 3.")

    # Legge i dati delle coordinate da un file CSV e crea una lista di tuple (coordinate)
    file_path = "coordinate.csv"
    df = pd.read_csv(file_path, names=['latitudine', 'longitudine'])

    # Converte la colonna della latitudine in numeri
    df['latitudine'] = pd.to_numeric(df['latitudine'], errors='coerce')

    # Converte la colonna della longitudine in numeri
    df['longitudine'] = pd.to_numeric(df['longitudine'], errors='coerce')

    # Rimuove eventuali righe duplicate
    df_no_duplicates = df.drop_duplicates(subset=['latitudine', 'longitudine']).copy()
    # Rimuove eventuali righe con dati mancanti
    df_no_duplicates = df_no_duplicates.dropna(subset=['latitudine', 'longitudine'])

    # Crea la lista delle coordinate
    dataset = [(row['latitudine'], row['longitudine']) for index, row in df_no_duplicates.iterrows()]

    # Costruzione del grafo
    graph = costruzione_grafo(dataset)

    # Misura del tempo di esecuzione di BFS
    start_time = time.time()
    path_BFS, _ = breadth_first_search(start_point, end_point, graph)
    BFS_execution_time = time.time() - start_time

    # Misura del tempo di esecuzione di DFS
    start_time = time.time()
    path_DFS, _ = depth_first_search(start_point, end_point, graph)
    DFS_execution_time = time.time() - start_time

    # Chiamata alla funzione per visualizzare i percorsi
    visualizza_path(path_BFS, path_DFS,  graph)

    return (path_BFS, BFS_execution_time),(path_DFS, DFS_execution_time), graph


# Funzione per la rappresentazione grafica dei percorsi individuati
def visualizza_path(path_BFS, path_DFS, graph):
    # Estrae le coordinate dal grafo
    coordinates = list(graph.keys())

    # Estrae latitudini e longitudini dal percorso BFS
    latitudes_BFS = [coord[0] for coord in path_BFS]
    longitudes_BFS = [coord[1] for coord in path_BFS]

    # Estrae latitudini e longitudini dal percorso DFS
    latitudes_DFS = [coord[0] for coord in path_DFS]
    longitudes_DFS = [coord[1] for coord in path_DFS]

    # Estrae latitudini e longitudini dai nodi nel grafo
    all_latitudes = [coord[0] for coord in coordinates]
    all_longitudes = [coord[1] for coord in coordinates]

    # Disegna il grafo e i percorsi per BFS
    plt.figure(figsize=(10, 8))
    plt.plot(all_longitudes, all_latitudes, 'o', color='blue', markersize=4, label='Nodi')
    plt.plot(longitudes_BFS, latitudes_BFS, marker='o', color='red', linestyle='-', markersize=8, label='Percorso BFS')
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    plt.title('Percorso Ottimale - BFS')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Disegna il grafo e i percorsi per DFS
    plt.figure(figsize=(10, 8))
    plt.plot(all_longitudes, all_latitudes, 'o', color='blue', markersize=4, label='Nodi')
    plt.plot(longitudes_BFS, latitudes_BFS, marker='o', color='purple', linestyle='-', markersize=8, label='Percorso DFS')
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    plt.title('Percorso Ottimale - DFS')
    plt.legend()
    plt.grid(True)
    plt.show()



# ESECUZIONE DEL MAIN

# Scelta del punto di destinazione {1, 2, 3}
gate = 1
path_BFS, path_DFS,  graph = percorso_ottimale(gate)


print("Tempo di esecuzione di BFS: ", path_BFS[1])
print("Tempo di esecuzione di DFS: ", path_DFS[1])
