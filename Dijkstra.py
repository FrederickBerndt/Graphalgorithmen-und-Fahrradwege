from pathlib import Path
from os import getcwd
from osmnx import load_graphml, save_graphml

import heapq
from collections import defaultdict
def dijkstra(G, source, target, weight="travel_time"):
    """ Bestimmt den kürzesten Weg von source nach target
        und verwendet die Datenstrukturen aus der Vorlesung.
        Die Python implementierung heapq ist nicht addressierbar,
        Sie können stattdessen das Werte Tupel (Distanz, Knoten) direkt hinzufügen. 

    Args:
        G (MultiDiGraph): Graph
        source (int): Startknoten
        target (int): Endknoten
        weight (str, optional): _description_. Defaults to "travel_time".

    Returns:
        Tuple: (Schätzdistanzen, Endknoten, Kürzeste Wege Baum)
    """
    dist = defaultdict(lambda: float("inf"))
    parent = defaultdict(lambda: None)
    heap = []
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
    return (dist, target, parent) if parent[target] is not None else None # Trinäer Operator in Python oder Bedingte Zuweisung: Abhängig von parent[target] wird das Triple oder None zurück gegeben.

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
    place_name = "Hofstede, Germany"
    from random import choices
    from osmnx import shortest_path
    graph = load_graphml(
        Path(getcwd()) / f"{place_name}_bike_network.graphml"
    )  # Gerichteter Graph


    for _ in range(100):
        rnd_node1 = choices(list(graph.nodes), k=1)[0]
        rnd_node2 = choices(list(graph.nodes), k=1)[0]
        erg = dijkstra(graph, rnd_node1, rnd_node2)
        erg2 = shortest_path(graph, rnd_node1, rnd_node2, weight="travel_time")
        if erg is None:
            assert erg2 is None
        else:
            route1 = make_route(erg[1], erg[2])
            assert route1 == erg2

    count = 0
    for rnd_node in choices(list(graph.nodes), k=100):
        try:
            dijkstra(graph, rnd_node, choices(list(graph.nodes), k=1)[0])[:2]
            count += 1
        except TypeError:
            pass
    print(count)
