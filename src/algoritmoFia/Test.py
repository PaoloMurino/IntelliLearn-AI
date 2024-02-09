import pandas as pd
from src.algoritmoFia.AlgAStar import distanza_haversine

file_path = "percorso_ottimaleGate3.csv"
df = pd.read_csv(file_path, names=['latitudine', 'longitudine'])

# Converte la colonna della latitudine in numeri
df['latitudine'] = pd.to_numeric(df['latitudine'], errors='coerce')

# Converte la colonna della longitudine in numeri
df['longitudine'] = pd.to_numeric(df['longitudine'], errors='coerce')

# Crea la lista delle coordinate
percorso_ottimale = [(row['latitudine'], row['longitudine']) for index, row in df.iterrows()]

def ammissibile(percorso_ottimale):

    # Calculate the heuristic (Haversine distance) from the start to the goal
    start = percorso_ottimale[0]
    goal = percorso_ottimale[-1]
    heuristic = distanza_haversine(start[0], start[1], goal[0], goal[1])

    # Calculate the total cost of the path
    total_cost = 0
    for i in range(len(percorso_ottimale) - 1):
        total_cost += distanza_haversine(percorso_ottimale[i][0], percorso_ottimale[i][1], percorso_ottimale[i+1][0], percorso_ottimale[i+1][1])

    if heuristic <= total_cost:
        print("ammissibile!")
    else:
        print("non ammissibile!")

    # The heuristic is admissible if it never overestimates the cost to reach the goal
    return heuristic <= total_cost

def testConsistenza(percorso_ottimale):
    # Get the start and goal from the keys of the dictionary
    goal = percorso_ottimale[-1]

    # Iterate over all nodes in the path
    for i in range(len(percorso_ottimale) - 1):
        # Get the current node and the next node
        current_node = percorso_ottimale[i]
        next_node = percorso_ottimale[i + 1]

        # Calculate the cost from the current node to the next node
        g_score = distanza_haversine(current_node[0], current_node[1], next_node[0], next_node[1])

        # Calculate the heuristic from the current node to the goal and from the next node to the goal
        h_score_current = distanza_haversine(current_node[0], current_node[1], goal[0], goal[1])
        h_score_next = distanza_haversine(next_node[0], next_node[1], goal[0], goal[1])

        # If the cost plus the heuristic from the next node is greater than the heuristic from the current node, the heuristic is not consistent
        if g_score + h_score_next > h_score_current:
            return False

    # If no inconsistency is found, the heuristic is consistent
    return True

ammissibilita = ammissibile(percorso_ottimale)
print(ammissibilita)

consistenza = testConsistenza(percorso_ottimale)
print(consistenza)



