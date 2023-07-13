import math
import queue
import random
from typing import Dict, List, Set, Tuple
from DataUtils import DataUtils
from Network import Node, NodeSet
from Pos import Pos
from type import CID, ClusterSet, NodeCID, NodeNearPoints, NodePosSet


class DBScan:
    def __init__(self, nodePoses: NodePosSet, nodeNum: int, minPts: int, nodeCID: NodeCID):
        self.nodePoses = nodePoses
        self.nodeNum = nodeNum
        self.minPts = minPts
        self.nodeCID = nodeCID
        self.eps = self.get_eps(0) * 5
        self.clusterIdx = -1
        self.nodeNearPoints: NodeNearPoints = {}

    def dbscan(self):
        self._init()
        self._check_near_points()

        for node in self.nodePoses:
            if self.nodeCID[node] == NOT_CLASSIFIED:
                if self._is_core_object(node):
                    self.clusterIdx += 1
                    self._bfs(node, self.clusterIdx)
                else:
                    self.nodeCID[node] = NOISE

        clusterSet: ClusterSet = {}
        for node in self.nodePoses:
            if self.nodeCID[node] != NOISE:
                clusterID = self.nodeCID[node]
                if clusterID not in clusterSet:
                    clusterSet[clusterID] = set()
                clusterSet[clusterID].add(node)

        print(f"[Cluster Count] {self.clusterIdx}")
        DataUtils.writeNodePoses(".\\", "test", self.nodePoses)

    def _init(self):
        for node in self.nodePoses:
            self.nodeCID[node] = NOT_CLASSIFIED

    def _check_near_points(self):
        for node1 in self.nodePoses:
            for node2 in self.nodePoses:
                if node1 == node2:
                    continue
                if self._euclidean_distance(self.nodePoses[node1], self.nodePoses[node2]) <= self.eps:
                    if node1 not in self.nodeNearPoints:
                        self.nodeNearPoints[node1] = set()
                    self.nodeNearPoints[node1].add(node2)

    def _is_core_object(self, idx: Node) -> bool:
        return len(self.nodeNearPoints[idx]) >= self.minPts

    def _dfs(self, now: Node, c: int):
        self.nodeCID[now] = c
        if not self._is_core_object(now):
            return

        S = [(iter(self.nodeNearPoints[now]), iter(self.nodeNearPoints[now]))]
        while S:
            t = S[-1]
            try:
                next = next(t[0])
                if next is None:
                    S.pop()
                    continue
            except StopIteration:
                S.pop()
                continue

            if self.nodeCID[next] == NOISE:
                self.nodeCID[next] = c
            if self.nodeCID[next] != NOT_CLASSIFIED:
                continue
            self.nodeCID[next] = c
            if self._is_core_object(next):
                S.append((iter(self.nodeNearPoints[next]), iter(self.nodeNearPoints[next])))

    def _bfs(self, now: Node, c: int):
        self.nodeCID[now] = c
        que = queue.Queue()
        que.put(now)
        while not que.empty():
            t = que.get()
            for next in self.nodeNearPoints[t]:
                if self.nodeCID[next] == NOISE:
                    self.nodeCID[next] = c
                if self.nodeCID[next] != NOT_CLASSIFIED:
                    continue
                self.nodeCID[next] = c
                if self._is_core_object(next):
                    que.put(next)

    def get_eps(self, removePercentage: float) -> float:
        dist_vec = [0.0] * self.nodeNum
        dist_sorted = [0.0] * self.nodeNum

        for i, (_, pos1) in enumerate(self.nodePoses.items()):
            for j, (_, pos2) in enumerate(self.nodePoses.items()):
                if i == j:
                    continue
                dist_sorted[j] = self._euclidean_distance(pos1, pos2)
            dist_sorted.sort()
            dist_vec[i] = dist_sorted[self.minPts - 1]

        dist_vec.sort(reverse=True)
        trunc = self.nodeNum * removePercentage
        tr = int(trunc)

        for i in range(tr):
            dist_vec[i] = 0.0

        dist_vec.sort(reverse=True)

        original = [(i, dist) for i, dist in enumerate(dist_vec)]

        maxVal = max(original, key=lambda x: x[1])[1]
        minVal = min(original, key=lambda x: x[1])[1]
        original = [(x / self.nodeNum, (y - minVal) / (maxVal - minVal)) for x, y in original]

        original = [(x * math.cos(-math.pi / 4.0) + math.sin(-math.pi / 4.0) * (y - 1.0),
                     -math.sin(-math.pi / 4.0) * x + math.cos(-math.pi / 4.0) * (y - 1.0)) for x, y in original]

        minValueIdx = min(enumerate(original), key=lambda x: x[1][1])[0]
        return dist_vec[minValueIdx]

    def _euclidean_distance(self, pu: Pos, pv: Pos) -> float:
        return math.sqrt(sum((pu[i] - pv[i]) ** 2 for i in range(len(pu))))

NOT_CLASSIFIED = -1
NOISE = -2
PI = math.pi
