from typing import List, Tuple
from DataUtils import NodePosSet, Network
import math


class OctTree:
    MAX_DEPTH = 18

    class NodeData:
        def __init__(self, np: int, tr: 'OctTree'):
            self.np = np
            self.tr = tr

    def __init__(self, dim: int, nodePoses: NodePosSet):
        self.dim = dim
        self.nMaxChild = 1 << (dim + 1)
        self.isLeaf = True
        self.maxPos = [0.0] * dim
        self.minPos = [0.0] * dim
        self.massCenter = [0.0] * dim
        self.regionCenter = [0.0] * dim
        self.weight = 0
        self.nodePoses = nodePoses
        self.data = []  # type: List[Union[int, 'OctTree']]
    
    def assign(self, network: Network, nodes: List[int], depth: int) -> None:
        if not nodes:
            return

        if not self.checkSplit(network, nodes) or depth >= self.MAX_DEPTH:
            self.data = nodes
            self.isLeaf = True
            return

        self.data = [None] * self.nMaxChild
        childNodes = [[] for _ in range(self.nMaxChild)]
        self.isLeaf = False
        for node in nodes:
            cidx = self.getIndex(node)
            childNodes[cidx].append(node)
        for i in range(self.nMaxChild):
            if childNodes[i]:
                self.data[i] = OctTree(self.dim, self.nodePoses)
                self.data[i].assign(network, childNodes[i], depth + 1)
    
    def depth(self) -> int:
        if self.isLeaf:
            return 1
        d = 0
        for nd in self.data:
            if isinstance(nd, OctTree):
                d = max(d, nd.depth())
        return d + 1
    
    def count(self) -> int:
        if self.isLeaf:
            return len(self.data)
        d = 0
        for nd in self.data:
            if isinstance(nd, OctTree):
                d += nd.count()
        return d
    
    def width(self) -> float:
        s = 0.0
        for i in range(self.dim):
            s = max(s, self.maxPos[i] - self.minPos[i])
        return s * 1.414
    
    def checkSplit(self, network: Network, nodes: List[int]) -> bool:
        self.maxPos = self.minPos = self.nodePoses[nodes[0]]
        self.weight = 0
        self.massCenter = [0.0] * self.dim
        for node in nodes:
            p = self.nodePoses[node]
            nodeDegree = network.getNodeDegree(node)
            self.weight += nodeDegree
            for i in range(self.dim):
                self.maxPos[i] = max(self.maxPos[i], p[i])
                self.minPos[i] = min(self.minPos[i], p[i])
            for i in range(self.dim):
                self.massCenter[i] += p[i] * nodeDegree
        for i in range(self.dim):
            self.massCenter[i] /= self.weight
        s = 0.0
        for i in range(self.dim):
            s = max(s, self.maxPos[i] - self.minPos[i])
        self.regionCenter = [(self.maxPos[i] + self.minPos[i]) / 2.0 for i in range(self.dim)]
        d = math.sqrt(sum((self.regionCenter[i] - self.massCenter[i]) ** 2 for i in range(self.dim)))
        THETA = 16
        return s / d > THETA
    
    def getIndex(self, node: int) -> int:
        childIndex = 0
        p = self.nodePoses[node]
        for i in range(self.dim):
            if p[i] > self.regionCenter[i]:
                childIndex += 1 << i
        return childIndex
