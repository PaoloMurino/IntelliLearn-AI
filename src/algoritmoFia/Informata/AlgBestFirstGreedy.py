import heapq
from haversine import haversine, Unit
from src.algoritmoFia.Node import Node

# Funzione per calcolare la distanza haversine tra due coordinate
def distanza_haversine(lat1, lon1, lat2, lon2):
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    distance = haversine(coord1, coord2, unit=Unit.KILOMETERS)  # Calcolo della distanza
    return distance

# Algoritmo Best-First Greedy per trovare il percorso tra due punti
def best_first_greedy(start, goal, graph):
    open_set = [(distanza_haversine(start.lat, start.lon, goal.lat, goal.lon), start)]  # Inizializza l'insieme aperto con il nodo di partenza e la sua euristica
    closed_set = set()  # Inizializza l'insieme chiuso vuoto

    while open_set:
        _, current_node = heapq.heappop(open_set)  # Estrae il nodo con l'euristica minima dall'insieme aperto

        if (current_node.lat, current_node.lon) in closed_set:  # Se il nodo è già stato esplorato, salta
            continue
        # Se il nodo corrente è il nodo di destinazione, costruisci e restituisci il percorso
        if (current_node.lat, current_node.lon) == (goal.lat, goal.lon):
            path = []
            while current_node:
                path.append((current_node.lat, current_node.lon))
                current_node = current_node.parent
            return path, len(open_set) + len(closed_set)  # Restituisce il percorso e la complessità spaziale

        closed_set.add((current_node.lat, current_node.lon))  # Aggiunge il nodo corrente all'insieme chiuso

        for neighbor in graph[(current_node.lat, current_node.lon)]:  # Scorre i vicini del nodo corrente
            if neighbor not in closed_set:  # Se il vicino non è stato esplorato
                h_score = distanza_haversine(neighbor[0], neighbor[1], goal.lat,
                                             goal.lon)  # Calcola l'euristica (distanza diretta al nodo di destinazione)

                neighbor_node = Node(neighbor[0], neighbor[1], h_score,
                                     current_node)  # Crea un nuovo nodo per il vicino

                if neighbor_node not in open_set:  # Se il vicino non è nell'insieme aperto, lo aggiunge
                    heapq.heappush(open_set, (h_score, neighbor_node))

    return None, None  # Se nessun percorso viene trovato, restituisce None per il percorso e la complessità spaziale

