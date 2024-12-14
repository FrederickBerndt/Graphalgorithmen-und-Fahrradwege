from pathlib import Path
from os import getcwd
from osmnx import load_graphml
from random import randint, seed
from osmnx import plot_graph
from networkx import strongly_connected_components
from collections import defaultdict
from random import choices

class DFS:
    """ Ein Klasse für die Tiefensuche in einem Graphen G nach der Vorlesung.
    """
    def __init__(self, G):
        self.makierungen = defaultdict(int)  # 0 = unmakiert, 1 = aktiv, 2 = beendet
        self.G = G
        self.init()
        for node in G.nodes():
            if self.makierungen[node] == 0:
                self.root(node)
                self.DFS(node, node)

    def DFS(self, node_u, node_v):
        self.makierungen[node_v] = 1
        for node_w in self.G.neighbors(node_v):
            if self.makierungen[node_w] != 0:
                self.traverseNonTreeEdge(node_v, node_w)
            else:
                self.traverseTreeEdge(node_v, node_w)
                self.DFS(node_v, node_w)
        self.backtrack(node_u, node_v)
        self.makierungen[node_v] = 2
        
    def init(self):
        pass
            
    def root(self, node_w):
        pass
        
    def traverseNonTreeEdge(self, node_v, node_w):
        pass
    
    def traverseTreeEdge(self, node_v, node_w):
        pass
        
    def backtrack(self, node_u, node_v):
        pass    
        
class DFSwithdfsNum(DFS):
    """ Erweitert die Tiefensuche um die Tiefensuchennummern.
    """
    def init(self):
        self.dfsNum = defaultdict(int)
        self.finNum = defaultdict(int)
        self.dfsPos = 1
        self.finPos = 1
            
    def root(self, node_w):
        self.dfsNum[node_w] = self.dfsPos
        self.dfsPos += 1
    
    def traverseTreeEdge(self, node_v, node_w):
        self.dfsNum[node_w] = self.dfsPos
        self.dfsPos += 1
        
    def backtrack(self, node_u, node_v):
        self.finNum[node_v] = self.finPos
        self.finPos += 1   
        
class SCC(DFSwithdfsNum):
    """ Erweitert die Tiefensuche um die Bestimmung der starken Zusammenhangskomponenten.
    """
    def init(self):
        super().init()
        self.components = {}
        self.oReps = []
        self.oNodes = []
            
    def root(self, node_w):
        super().root(node_w)
        self.oReps.append(node_w)
        self.oNodes.append(node_w)
        
    def traverseTreeEdge(self, node_v, node_w):
        super().traverseTreeEdge(node_v, node_w)
        self.oReps.append(node_w)
        self.oNodes.append(node_w)
        
    def traverseNonTreeEdge(self, node_v, node_w):
        if node_w in self.oNodes:
            while self.dfsNum[node_w] < self.dfsNum[self.oReps[-1]]:
                self.oReps.pop()
        
    def backtrack(self, node_u, node_v):
        super().backtrack(node_u, node_v)
        if node_v == self.oReps[-1]:
            self.oReps.pop()
            node_w = self.oNodes.pop()
            self.components[node_w] = node_v
            while node_w != node_v:
                node_w = self.oNodes.pop()
                self.components[node_w] = node_v

def rnd_color(node=None):
    """ Erzeugt zufällige RGB Farben.

    Args:
        node (int, optional): Nimmt die Zahl als seed für den Random Number Generator. Defaults to None.

    Returns:
        str: RGB Farbe
    """
    if node is not None:
        seed(node)
    return f"#{randint(0, 255):02x}{randint(0, 255):02x}{randint(0, 255):02x}"

if __name__ == "__main__":
    #set recursion limit
    import sys
    sys.setrecursionlimit(10000)

    place_name = "Hofstede, Germany"
    graph = load_graphml(
        Path(getcwd()) / f"{place_name}_bike_network.graphml"
    )  # Gerichteter Graph
    place_name = "Hofstede, Germany"
    components = SCC(graph).components

    plot_graph(graph, edge_color=[rnd_color(components[edge[0]]) for edge in graph.edges], node_size=0, bgcolor="w")


    komps = list(strongly_connected_components(graph))
    for komp in komps:
        ref_node = list(komp)[0]
        assert all([components[node] == components[ref_node] for node in komp])
    for node in components:
        assert any([(node in komp and components[node]) for komp in komps if node in komp])