import heapq
from haversine import haversine, Unit
from src.algoritmoFia.Node import Node

# Funzione per calcolare la distanza haversine tra due coordinate
def distanza_haversine(lat1, lon1, lat2, lon2):
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    distance = haversine(coord1, coord2, unit=Unit.KILOMETERS)  # Calcolo della distanza
    return distance


# Algoritmo A* per trovare il percorso ottimale tra due punti
def a_star(start, goal, graph):
    open_set = [start]  # Inizializza l'insieme aperto con il nodo di partenza
    closed_set = set()  # Inizializza l'insieme chiuso vuoto
    nodes_in_memory = 0 #Necessario per memorizzare il numero di nodi effettivamente

    while open_set:
        current_node = heapq.heappop(open_set)  # Estrae il nodo con il costo minimo dall'insieme aperto

        if (current_node.lat, current_node.lon) in closed_set:  # Se il nodo è già stato esplorato, salta
            continue

        if (current_node.lat, current_node.lon) == (goal.lat, goal.lon):  # Se il nodo corrente è il nodo di destinazione, costruisci e restituisci il percorso
            path = []
            while current_node:
                path.append((current_node.lat, current_node.lon))
                current_node = current_node.parent
            return path[::-1], nodes_in_memory

        closed_set.add((current_node.lat, current_node.lon))  # Aggiunge il nodo corrente all'insieme chiuso
        nodes_in_memory += 1  # Aggiorna l'insieme di nodi memorizzati in memoria

        for neighbor in graph[(current_node.lat, current_node.lon)]:  # Scorre i vicini del nodo corrente
            if neighbor not in closed_set:  # Se il vicino non è stato esplorato
                g_score = current_node.cost + distanza_haversine(current_node.lat, current_node.lon, neighbor[0], neighbor[1])  # Calcola il costo del percorso finora per raggiungere il vicino
                h_score = distanza_haversine(neighbor[0], neighbor[1], goal.lat, goal.lon)  # Calcola l'euristica (distanza diretta al nodo di destinazione)
                f_score = g_score + h_score  # Calcola il punteggio totale (costo finora + euristica)

                neighbor_node = Node(neighbor[0], neighbor[1], f_score, current_node)  # Crea un nuovo nodo per il vicino

                if neighbor_node not in open_set:  # Se il vicino non è nell'insieme aperto, lo aggiunge
                    heapq.heappush(open_set, neighbor_node)

    return None  # Se nessun percorso viene trovato
