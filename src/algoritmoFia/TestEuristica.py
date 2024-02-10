import pandas as pd
from src.algoritmoFia.AlgAStar import distanza_haversine

file_path = "percorso_ottimaleGate3.csv"
df = pd.read_csv(file_path, header=None, names=['latitudine', 'longitudine'], skiprows=1)

# Converte la colonna della latitudine in numeri
df['latitudine'] = pd.to_numeric(df['latitudine'], errors='coerce')

# Converte la colonna della longitudine in numeri
df['longitudine'] = pd.to_numeric(df['longitudine'], errors='coerce')

# Crea la lista delle coordinate
percorso_ottimale = [(row['latitudine'], row['longitudine']) for index, row in df.iterrows()]


def ammissibile(percorso_ottimale):

    # Calcolo dell'euristica (distanza di Haversine) dallo start all'obiettivo
    start = percorso_ottimale[0]
    goal = percorso_ottimale[-1]
    heuristic = distanza_haversine(start[0], start[1], goal[0], goal[1])

    # Calcolo del costo totale del percorso
    total_cost = 0
    for i in range(len(percorso_ottimale) - 1):
        total_cost += distanza_haversine(percorso_ottimale[i][0], percorso_ottimale[i][1], percorso_ottimale[i+1][0], percorso_ottimale[i+1][1])

    if heuristic <= total_cost:
        print("ammissibile!")
    else:
        print("non ammissibile!")

    # L'euristica è ammissibile se non sovrastima il costo per raggiungere l'obiettivo
    return heuristic <= total_cost

def testConsistenza(percorso_ottimale):
    # Individuazione del nodo obiettivo
    goal = percorso_ottimale[-1]

    # Itera tutti i nodi del percorso ottimale
    for i in range(len(percorso_ottimale) - 1):
        # Individua il nodo corrente e il nodo successivo
        current_node = percorso_ottimale[i]
        next_node = percorso_ottimale[i + 1]

        # Calcola il costo di passo tra il nodo corrente e il nodo successivo
        g_score = distanza_haversine(current_node[0], current_node[1], next_node[0], next_node[1])

        # Calcolo dell'euristica dal nodo corrente all'obiettivo e dal nodo successivo all'obiettivo
        h_score_current = distanza_haversine(current_node[0], current_node[1], goal[0], goal[1])
        h_score_next = distanza_haversine(next_node[0], next_node[1], goal[0], goal[1])

        # Se il costo di passo più l'euristica dal nodo successivo è maggiore dell'euristica dal nodo corrente, l'euristica non è consistente
        if g_score + h_score_next > h_score_current:
            print("consistente!")
            #return None

    # Se nessuna incosistenza è stata trovata, l'euristica è consistente
    return True

ammissibilita = ammissibile(percorso_ottimale)
print(ammissibilita)

consistenza = testConsistenza(percorso_ottimale)
print(consistenza)


