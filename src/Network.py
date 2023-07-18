from typing import Set, Dict, Tuple

Node = int
NodeSet = Set[Node]

Edge = Tuple[Node, Node]
EdgeSet = Set[Edge]

def EDGE(v1, v2):
    return ((v1 << 32) | v2) if v1 < v2 else ((v2 << 32) | v1)

def V1(edge):
    return (edge >> 32) & 0xffffffff

def V2(edge):
    return edge & 0xffffffff

class Network:
    def __init__(self):
        self.nodes: NodeSet = set()
        self.edges: EdgeSet = set()
        self.degMat: Dict[Node, int] = {}
        self.allDegree: int = 0
        self.maxNodeId: Node = 0

    def insertEdge(self, v1: Node, v2: Node) -> None:
        self.nodes.add(v1)
        self.nodes.add(v2)
        self.edges.add((v1, v2))
        self.maxNodeId = max(self.maxNodeId, max(v1, v2))
        self.allDegree += 2
        self.degMat[v1] = self.degMat.get(v1, 0) + 1
        self.degMat[v2] = self.degMat.get(v2, 0) + 1

    def clear(self) -> None:
        self.nodes.clear()
        self.edges.clear()
        self.degMat.clear()

    def getNodeSet(self) -> NodeSet:
        return self.nodes

    def getEdgeSet(self) -> EdgeSet:
        return self.edges

    def getNodeNum(self) -> int:
        return len(self.nodes)

    def getEdgeNum(self) -> int:
        return len(self.edges)

    def getFactor(self, u: Node, v: Node) -> float:
        return float(self.degMat.get(u, 0)) * float(self.degMat.get(v, 0)) / self.allDegree

    def getFactor(self, u: Node) -> float:
        return float(self.degMat.get(u, 0)) / self.allDegree

    def getNodeDegree(self, u: Node) -> int:
        return self.degMat.get(u, 0)
