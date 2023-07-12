from typing import Set, Dict
from Network import Node, NodeSet
from Pos import Pos

CID = int
ClusterSet = Dict[CID, NodeSet]

NodePosSet = Dict[Node, Pos]
NodeCID = Dict[Node, CID]
NodeNearPoints = Dict[Node, NodeSet]
