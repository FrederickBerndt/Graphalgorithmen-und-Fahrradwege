from networkx import Graph
from UnionFind import UnionFind
def kruskal(G, weight="weight"):
    """ Der Kruskal Algorithmus aus der Vorlesung.

    Args:
        G (MultiDiGraph): Graph
        weight (str, optional): Das relevante Kantengewicht. Defaults to "weight".
    """
    def nodeId(node):
        """ Bestimmt für die Union-Find Datenstruktur den Index des Knotens.

        Args:
            node (int): NodeID

        Returns:
            int: Index des Knotens in G
        """
        return list(G.nodes()).index(node)
    
    T = UnionFind(len(G.nodes()))
    E = [(float(G[u][v][num][weight]), u, v) for u in G for v in G[u] for num in G[u][v]]
    Gk = Graph()
    for k, u, v in E:
        if not T.connected(u,v) and float(k) < float("inf"):
            T.union(u,v)
            Gk.add_nodes_from([u,v])
            Gk.add_edge(u,v, weight=k)
    return Gk