from pathlib import Path
from os import getcwd
from osmnx import load_graphml, plot_graph, plot_graph_routes, plot_graph_route, plot_graph, shortest_path
from random import randint
from collections import defaultdict
from ComponentToNode import relevante_pois
from geopandas import read_file
import heapq
from collections import defaultdict

def gen_dijkstra(G, sources, targets, weight="travel_time"):
    """ Eine Generator-Variante von Dijkstras Algorithmus,
        der eine Liste von Ziel- und Startknoten akzeptiert
        und diese nach der Entfernung zurückgibt.
    Args:
        G (MultiDiGraph): Graph
        sources (List[int]): Startknoten
        targets (List[int]): Endknoten
        weight (str, optional): _description_. Defaults to "travel_time".

    Returns:
        Tuple: (Schätzdistanzen, Erreichter Knoten, Kürzeste Wege Wald)
    """
    targets = set(targets)
    dist = defaultdict(lambda: float("inf"))
    parent = defaultdict(lambda: None)
    heap = []
    for source in sources:
        parent[source] = source
        dist[source] = 0
        heapq.heappush(heap, (0, source))
    while len(heap) > 0:
        u = heapq.heappop(heap)[1]
        for v in G[u].keys():
            for num in G[u][v].keys():
                if dist[u] + G[u][v][num][weight] < dist[v]:
                    dist[v] = dist[u] + G[u][v][num][weight]
                    parent[v] = u
                    found = False
                    for i in range(len(heap)):
                        if heap[i][1] == v:
                            heap[i] = (dist[v], v)
                            heapq.heapify(heap)
                            found = True
                    if not found: heapq.heappush(heap, (dist[v], v))
        if u in targets:
            yield (dist, u, parent)

def make_route(node, parent):
    """ Bestimmt die Route von node bis zur Wurzel anhand des parent Dictionaries.

    Args:
        node (int): Startknoten
        parent (Dict): Kürzeste Wege Baum

    Returns:
        List: Liste der Knoten auf der Route
    """
    route = [node]
    while node != parent[node]:
        node = parent[node]
        route.append(node)
    return route[::-1]

if __name__ == "__main__":
    #set recursion limit
    import sys
    sys.setrecursionlimit(10000)

    place_name = "Hofstede, Germany"
    graph = load_graphml(
        Path(getcwd()) / f"{place_name}_bike_network.graphml"
    )  # Gerichteter Graph
    place_name = "Hofstede, Germany"
    gdf = read_file(Path(getcwd()) / f"{place_name}_poi.geojson", driver="GeoJSON")

    poi_dict = {}
    for index, poi in gdf.iterrows():
        if poi['amenity'] not in poi_dict:
            poi_dict[poi['amenity']] = []
        poi_dict[poi['amenity']].append(poi["nearest_node"])

    for _ in range(10):
        rnd_node = list(graph.nodes)[randint(0, len(graph.nodes)-1)]
        rnd_cat = list(poi_dict.keys())[randint(0, len(poi_dict.keys())-1)]
        pois = relevante_pois(graph, rnd_node, rnd_cat, poi_dict)
        gen = gen_dijkstra(graph, [rnd_node], pois)

        # plot route to the k nearest POIs
        k = 5
        routes = [make_route(*erg[1:]) for _, erg in zip(range(k), list(gen))]    
        erg2 = shortest_path(graph, [rnd_node]*len(pois), pois, weight="travel_time")
        
        assert all([any([route == erg for erg in erg2]) for route in routes])
        
        if len(routes) > 1:
            fig, ax = plot_graph_routes(graph, routes, show=False, close=False, node_size=0, route_colors="green")
        elif len(routes) == 1:
            fig, ax = plot_graph_route(graph, routes[0], show=False, close=False, node_size=0, route_color="green")
        else:
            fig, ax = plot_graph(graph, show=False, close=False, node_size=0)
        # Add Startnode to plot
        ax.scatter(graph.nodes[rnd_node]['x'], graph.nodes[rnd_node]['y'], c="red", s=100)
        fig.show()
        
    for _ in range(100):
        rnd_node = list(graph.nodes)[randint(0, len(graph.nodes)-1)]
        rnd_cat = list(poi_dict.keys())[randint(0, len(poi_dict.keys())-1)]
        pois = relevante_pois(graph, rnd_node, rnd_cat, poi_dict)
        gen = gen_dijkstra(graph, [rnd_node], pois)

        # plot route to the k nearest POIs
        k = 5
        routes = [make_route(*erg[1:]) for _, erg in zip(range(k), list(gen))]    
        erg2 = shortest_path(graph, [rnd_node]*len(pois), pois, weight="travel_time")
        assert all([any([route == erg for erg in erg2]) for route in routes])