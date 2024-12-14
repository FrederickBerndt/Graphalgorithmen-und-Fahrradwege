from pathlib import Path
from os import getcwd
from osmnx import load_graphml
from Kruskal import kruskal
from osmnx import plot_graph_routes, plot_graph
    
place_name = "Hofstede, Germany"
graph = load_graphml(
        Path(getcwd()) / f"{place_name}_bike_network.graphml"
    )  # Gerichteter Graph
graph_complete = load_graphml(Path(getcwd()) / f"{place_name}_complete_network.graphml")
SCC_graph = load_graphml(Path(getcwd()) / f"{place_name}_scc_network.graphml")
print('Start constructing SCC tree')
SCC_tree = kruskal(SCC_graph)
print("Constructed SCC tree")
fig, ax = plot_graph_routes(
    graph_complete,
    routes=[SCC_graph.edges[(*edge, 0)]["route"] for edge in SCC_tree.edges() if SCC_graph.edges[(*edge, 0)]["route"] is not None],
    route_colors="red",
    route_linewidth=1,
    route_alpha=0.5,
    node_size=0,
    edge_linewidth=0.2,
    edge_color="grey",
    bgcolor="white",
    show=False,
    close=False,
)
plot_graph(
    graph,
    ax=ax,
    node_size=0,
    edge_linewidth=2,
    edge_color="black",
    bgcolor="white",
    show=False,
    close=False,
)
fig.show()
summe = sum([float(SCC_tree.edges[edge]["weight"]) for edge in SCC_tree.edges()])
print(f"Es sind zwischen {summe/2000:.3} und {summe/1000:.3}km an neuen Fahrradwegen nötig.")

# Hier kommen weitere Tests