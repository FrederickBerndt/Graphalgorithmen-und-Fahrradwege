from itertools import combinations
from networkx import MultiGraph
from ComponentToNode import preprocessSCC
from GenerativeDijkstra import gen_dijkstra
from pathlib import Path
from os import getcwd
from Dijkstra import make_route
from osmnx import load_graphml

def min_connection(graph, komp_1, komp_2):
    """ Bestimmt die kürzeste Verbindung zwischen zwei Komponenten.

    Args:
        graph (MultiDiGraph): Der zugrundeliegende Graph (nicht der SCC-Graph)
        komp_1 (List): Liste von Knoten, die die erste Komponente bilden
        komp_2 (List): Liste von Knoten, die die zweite Komponente bilden

    Returns:
        Tuple: Das triple von (Komponente 1, Komponente 2, Dict mit Gewicht und Route),
                mit denen die Kanten und Kantenlängen im SCC-Graphen erstellt werden.
    """
    gen = gen_dijkstra(graph, komp_1, komp_2, "length")
    ergs = [(erg[0][erg[1]], make_route(*erg[1:]) if erg[0][erg[1]] < float("inf") else []) for _, erg in zip(range(len(komp_1)), list(gen))]
    min_weight, min_path = min(ergs) if len(ergs) > 0 else (float("inf"), [])
    return (komp_1, komp_2, {"weight": min_weight, "route": min_path})

if __name__ == "__main__":
    place_name = "Hofstede, Germany"
    graph = load_graphml(
        Path(getcwd()) / f"{place_name}_bike_network.graphml"
    )  # Gerichteter Graph
    place_name = "Hofstede, Germany"
    strongly_connected_components = preprocessSCC(graph)
    meta_nodes = set(strongly_connected_components.values())
    SCC_graph = MultiGraph()
    SCC_graph.add_nodes_from(meta_nodes)
    graph_for_scc_edges = load_graphml(Path(getcwd()) / f"{place_name}_complete_scc_network.graphml")
    edges = [min_connection(graph_for_scc_edges, komp_1, komp_2) for komp_1, komp_2 in combinations(meta_nodes, 2)]
    _ = SCC_graph.add_edges_from(edges, weight="weight", route="route")

    from networkx import multi_source_dijkstra_path_length
    from random import choices

    meta_nodes_lists = [list(meta_node) for meta_node in meta_nodes]
    for _ in range(10):
        komp_pair = choices(meta_nodes_lists, k=2)
        erg = multi_source_dijkstra_path_length(graph_for_scc_edges, komp_pair[0], weight="length")
        dist_list = [erg[node] for node in erg if node in komp_pair[1]]
        erg = multi_source_dijkstra_path_length(graph_for_scc_edges, komp_pair[1], weight="length")
        dist_list += [erg[node] for node in erg if node in komp_pair[0]]
        if min(dist_list, default=float("inf")) < float("inf"):
            assert abs(min_connection(graph_for_scc_edges, komp_pair[0], komp_pair[1])[2]["weight"] - min(dist_list)) < 1
        else:
            assert min_connection(graph_for_scc_edges, komp_pair[0], komp_pair[1])[2]["weight"] == float("inf")