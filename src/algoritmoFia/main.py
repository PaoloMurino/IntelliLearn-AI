import pandas as pd
import matplotlib.pyplot as plt
from src.algoritmoFia.AlgAStar import Node, a_star
from src.algoritmoFia.CostruzioneGrafo import costruzione_grafo
from src.algoritmoFia.TestComplessita import analisiComplessita


def percorso_ottimale(gate):
    # Definizione del punto di partenza
    start_point = Node(lat=39.4305577, lon=-0.3351722)

    # Definizione del punto  di destinazione
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

    # Individuazione del percorso ottimale utilizzando l'algoritmo A*
    path, spazio = a_star(start_point, end_point, graph)

    # Chiamata alla funzione per visualizzare il percorso
    visualizza_path(path, graph)

    return path, graph, spazio


# funzione per la rappresentazione grafica del percorso individuato
def visualizza_path(path, graph):
    # Estrae le coordinate dal grafo
    coordinates = list(graph.keys())

    # Estrae latitudini e longitudini dal percorso
    latitudes = [coord[0] for coord in path]
    longitudes = [coord[1] for coord in path]

    # Estrae latitudini e longitudini dai nodi nel grafo
    all_latitudes = [coord[0] for coord in coordinates]
    all_longitudes = [coord[1] for coord in coordinates]

    # Disegna il grafo
    plt.figure(figsize=(10, 8))
    plt.plot(all_longitudes, all_latitudes, 'o', color='blue', markersize=4, label='Nodi')
    plt.plot(longitudes, latitudes, marker='o', color='red', linestyle='-', markersize=8, label='Percorso ottimale')
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    plt.title('Percorso Ottimale')
    plt.legend()
    plt.grid(True)
    plt.show()


"""ESECUZIONE DEL MAIN"""

# Scelta del punto di destinazione {1, 2, 3}
gate = 1
path, graph, spazio = percorso_ottimale(gate)

# Analisi della complessità temporale
time_complexity = analisiComplessita(graph)

print(f"Complessità temporale: {time_complexity:.4f}")
print(f"Complessità spaziale: {spazio}")



"""SALVATAGGIO DEL PERCORSO OTTIMALE IN UN FILE CSV, USATO PER CONFRONTARE IL PERCORSO RISULTANTE SULLA MAPPA
if path:
    # Crea un DataFrame dal percorso
    path_df = pd.DataFrame(path, columns=['latitudine', 'longitudine'])

    # Salva il DataFrame in un file CSV
    path_df.to_csv('percorso_ottimaleGate4.csv', index=False)
    print("Percorso ottimale salvato in 'percorso_ottimaleGate4.csv'")
else:
    print("Nessun percorso trovato.")
"""
