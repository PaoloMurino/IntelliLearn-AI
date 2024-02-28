import time

import matplotlib.pyplot as plt
import pandas as pd
from src.algoritmoFia.Informata.AlgAStar import Node, a_star
from src.algoritmoFia.Informata.AlgBeamSearch import beam_search
from src.algoritmoFia.Informata.AlgBestFirstGreedy import best_first_greedy

from src.algoritmoFia.CostruzioneGrafo import costruzione_grafo


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

    # Misura del tempo di esecuzione di A*
    start_time = time.time()
    path_astar, _ = a_star(start_point, end_point, graph)
    astar_execution_time = time.time() - start_time

    # Misura del tempo di esecuzione di Best-First Greedy
    start_time = time.time()
    path_greedy, _ = best_first_greedy(start_point, end_point, graph)
    greedy_execution_time = time.time() - start_time

    # Misura del tempo di esecuzione di Beam Search
    start_time = time.time()
    path_beam_search, _ = beam_search(start_point, end_point, graph)
    beam_search_execution_time = time.time() - start_time

    # Chiamata alla funzione per visualizzare i percorsi
    visualizza_path(path_astar, path_greedy, path_beam_search, graph)

    return (path_astar, astar_execution_time), (path_greedy, greedy_execution_time), (
    path_beam_search, beam_search_execution_time), graph


# Funzione per la rappresentazione grafica dei percorsi individuati
def visualizza_path(path_astar, path_greedy, path_beam_search, graph):
    # Estrae le coordinate dal grafo
    coordinates = list(graph.keys())

    # Estrae latitudini e longitudini dal percorso A*
    latitudes_astar = [coord[0] for coord in path_astar]
    longitudes_astar = [coord[1] for coord in path_astar]

    # Estrae latitudini e longitudini dal percorso Best-First Greedy
    latitudes_greedy = [coord[0] for coord in path_greedy]
    longitudes_greedy = [coord[1] for coord in path_greedy]

    # Estrae latitudini e longitudini dal percorso Beam Search
    latitudes_beam_search = [coord[0] for coord in path_beam_search]
    longitudes_beam_search = [coord[1] for coord in path_beam_search]

    # Estrae latitudini e longitudini dai nodi nel grafo
    all_latitudes = [coord[0] for coord in coordinates]
    all_longitudes = [coord[1] for coord in coordinates]

    # Disegna il grafo e i percorsi per A*
    plt.figure(figsize=(10, 8))
    plt.plot(all_longitudes, all_latitudes, 'o', color='blue', markersize=4, label='Nodi')
    plt.plot(longitudes_astar, latitudes_astar, marker='o', color='red', linestyle='-', markersize=8,
             label='Percorso A*')
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    plt.title('Percorso Ottimale - A*')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Disegna il grafo e i percorsi per Best-First Greedy
    plt.figure(figsize=(10, 8))
    plt.plot(all_longitudes, all_latitudes, 'o', color='blue', markersize=4, label='Nodi')
    plt.plot(longitudes_greedy, latitudes_greedy, marker='o', color='green', linestyle='-', markersize=8,
             label='Percorso Best-First Greedy')
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    plt.title('Percorso Ottimale - Best-First Greedy')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Disegna il grafo e i percorsi per Beam Search
    plt.figure(figsize=(10, 8))
    plt.plot(all_longitudes, all_latitudes, 'o', color='blue', markersize=4, label='Nodi')
    plt.plot(longitudes_beam_search, latitudes_beam_search, marker='o', color='purple', linestyle='-', markersize=8,
             label='Percorso Beam Search')
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    plt.title('Percorso Ottimale - Beam Search')
    plt.legend()
    plt.grid(True)
    plt.show()


# ESECUZIONE DEL MAIN

# Scelta del punto di destinazione {1, 2, 3}
gate = 3
path_astar, path_greedy, path_beam_search, graph = percorso_ottimale(gate)

print("Tempo di esecuzione di A*: ", path_astar[1])
print("Tempo di esecuzione di Best-First Greedy: ", path_greedy[1])
print("Tempo di esecuzione di Beam Search: ", path_beam_search[1])
