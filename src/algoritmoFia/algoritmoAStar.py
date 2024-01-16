import osmnx as ox
import networkx as nx
import pandas as pd


def get_port_graph(place_name):
    # Impostare manualmente i limiti geografici per includere il porto di Valencia
    """north, south, east, west = 39.4640, 39.4310, -0.2850, -0.3280
    place = ox.geocode_to_gdf("Valencia, Spain")

    # Estrai la rete stradale del porto
    G = ox.graph_from_bbox(north, south, east, west, network_type='drive')"""
    place = ox.geocode(place_name)
    G = ox.graph_from_place(place, network_type='drive')

    # Raccogli le coordinate dei nodi
    nodes_coordinates = [(data['y'], data['x']) for node, data in G.nodes(data=True)]
    print(G, nodes_coordinates)

    return G, nodes_coordinates

def calculate_optimal_path(graph, origin, destination):
    # Adapt the function as needed based on the characteristics of the port
    # You may need to consider additional constraints or attributes specific to the port's road network
    origin_node = ox.distance.nearest_nodes(graph, origin[0], origin[1])
    destination_node = ox.distance.nearest_nodes(graph, destination[0], destination[1])

    path = nx.shortest_path(graph, origin_node, destination_node, weight='length')

    path_coordinates = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in path]

    return path_coordinates

# Esempio di utilizzo
place_name = "Valencia, Spain"
graph_port, nodi = get_port_graph(place_name)
origin_point = (39.43054, -0.33518)
destination_point = (39.4507282, -0.3073923)

path = calculate_optimal_path(graph_port, origin_point, destination_point)

print("Percorso ottimale nel porto:", path)

# Creazione di un DataFrame con i dati dei nodi
df_nodes = pd.DataFrame(nodi, columns=['Latitude', 'Longitude'])

# Salvataggio del DataFrame in un file Excel
excel_file_path = 'coordinate_nodi_rete_stradale.xlsx'
df_nodes.to_excel(excel_file_path, index=False)
