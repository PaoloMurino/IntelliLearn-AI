from collections import deque
from src.algoritmoFia.Node import Node


# Algoritmo BFS per trovare il percorso ottimale tra due punti
def breadth_first_search(start, goal, graph):
    queue = deque([start])  # Inizializza la coda con il nodo di partenza
    closed_set = set()  # Inizializza l'insieme chiuso vuoto
    nodes_in_memory = 0  # Necessario per memorizzare il numero di nodi effettivamente

    while queue:
        current_node = queue.popleft()  # Estrae il primo nodo dalla coda

        if (current_node.lat, current_node.lon) in closed_set:  # Se il nodo è già stato esplorato, salta
            continue

        if (current_node.lat, current_node.lon) == (
                goal.lat,
                goal.lon):  # Se il nodo corrente è il nodo di destinazione, costruisci e restituisci il percorso
            path = []
            while current_node:
                path.append((current_node.lat, current_node.lon))
                current_node = current_node.parent
            return path[::-1], nodes_in_memory

        closed_set.add((current_node.lat, current_node.lon))  # Aggiunge il nodo corrente all'insieme chiuso
        nodes_in_memory += 1  # Aggiorna l'insieme di nodi memorizzati in memoria

        for neighbor in graph[(current_node.lat, current_node.lon)]:  # Scorre i vicini del nodo corrente
            if neighbor not in closed_set:  # Se il vicino non è stato esplorato
                neighbor_node = Node(neighbor[0], neighbor[1], 0, current_node)  # Crea un nuovo nodo per il vicino
                queue.append(neighbor_node)  # Aggiunge il vicino alla coda

    return None, nodes_in_memory  # Se nessun percorso viene trovato
