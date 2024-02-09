# Definizione della classe Node per rappresentare i nodi nel grafo
class Node:
    def __init__(self, lat, lon, cost=0, parent=None):
        self.lat = lat
        self.lon = lon
        self.cost = cost  # Costo del percorso finora per raggiungere il nodo
        self.parent = parent  # Nodo genitore nel percorso

    def __lt__(self, other):
        return self.cost < other.cost  # Permette di confrontare nodi in base al costo
