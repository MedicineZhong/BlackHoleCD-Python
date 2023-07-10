from typing import Set, Dict, Tuple

Node = int
NodeSet = Set[Node]

CID = int
ClusterSet = Dict[CID, Set[Node]]

Node = int
Pos = Tuple[float, ...]
NodePosSet = Dict[Node, Pos]
NodeCID = Dict[Node, CID]
NodeNearPoints = Dict[Node, NodeSet]
