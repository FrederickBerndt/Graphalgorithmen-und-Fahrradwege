from pathlib import Path
from os import getcwd
from osmnx import load_graphml
from random import choices
from StronglyConnectedComponents import SCC
from Dijkstra import dijkstra

def preprocessSCC(G):
    """ Verarbeitet die Komponenten aus der SCC Klasse zu einem Dictionary,
        in dem jeder Knoten auf seine Komponente abgebildet wird.

    Args:
        G (MultiDiGraph): Graph

    Returns:
        Dict: Das Dictionary mit den Komponenten
    """
    components = SCC(G).components
    # YOUR CODE HERE
    dict_of_components = {}
    ret_dict = {}
    #create dict with reps as keys and component as values
    for node in components.keys():
        if components[node] not in dict_of_components: dict_of_components[components[node]] = [node]
        else: dict_of_components[components[node]].append(node)
    #rewrite them as frozensets
    for component in dict_of_components.keys():
        dict_of_components[component] = frozenset(dict_of_components[component])
    #associate nodes with their frozenset component
    for c in components.keys():
        ret_dict[c] = dict_of_components[components[c]]
    return ret_dict

def relevante_pois(G, node_v, kategorie, poi_dict):
    """ Bestimmt die relevanten POIs für einen Knoten node_v und eine Kategorie bei gegebener Zuordnung.

    Args:
        G: graph
        node_v (int): Node ID des Knotens
        kategorie (str): Die Kategorie
        
    Returns:
        List: Liste der relevanten POIs
    """
    dict_of_components = preprocessSCC(G)
    pois = poi_dict[kategorie]
    relevante_pois = [poi for poi in pois if poi in dict_of_components[node_v]]
    return relevante_pois

if __name__ == "__main__":
    #set recursion limit
    import sys
    sys.setrecursionlimit(10000)

    place_name = "Hofstede, Germany"
    graph = load_graphml(
        Path(getcwd()) / f"{place_name}_bike_network.graphml"
    )  # Gerichteter Graph
    place_name = "Hofstede, Germany"

    from geopandas import read_file
    gdf = read_file(Path(getcwd()) / f"{place_name}_poi.geojson", driver="GeoJSON")

    poi_dict = {}
    for index, poi in gdf.iterrows():
        if poi['amenity'] not in poi_dict:
            poi_dict[poi['amenity']] = []
        poi_dict[poi['amenity']].append(poi["nearest_node"])

    for _ in range(10):
        node_v = choices(list(graph.nodes), k=1)[0]
        kategorie = choices(list(poi_dict.keys()), k=1)[0]
        pois = relevante_pois(graph, node_v, kategorie)
        assert all([poi in poi_dict[kategorie] for poi in pois])
        assert all([poi in preprocessSCC(graph)[node_v] for poi in pois])
        for poi in relevante_pois(graph, node_v, kategorie):
            erg = dijkstra(graph, node_v, poi)
            assert erg is not None
            print(erg[0])
