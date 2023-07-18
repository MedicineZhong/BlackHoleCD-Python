import os
import time
from typing import Dict, Set, Tuple

from Network import Network
from type import Node, NodePosSet, NodeCID


class DataUtils:
    @staticmethod
    def getDataRoot(exePath: str) -> str:
        print("WARNING: \"getDataRoot\" is a now debugging function!")
        return os.path.join(exePath[:exePath.find("src")], "Datasets")

    @staticmethod
    def readNetwork(dataRoot: str, dataset: str, network: Network) -> str:
        start = time.time()
        network.clear()
        filename = os.path.join(dataRoot, dataset + ".ungraph_sample.txt")
        with open(filename, "r") as fin:
            for line in fin:
                line = line.strip()
                if len(line) == 0 or line[0] == '#':
                    continue
                v1, v2 = line.split("\t")
                v1 = int(v1)
                v2 = int(v2)
                network.insertEdge(v1, v2)
        end = time.time()
        print(f"[readNetwork] [{dataset}] [{end - start:.2f}s] {network.getNodeNum()} nodes, {network.getEdgeNum()} edges")
        return filename

    @staticmethod
    def writeNodePoses(dataRoot: str, dataset: str, nodePoses: NodePosSet) -> str:
        start = time.time()
        filename = os.path.join(dataRoot, dataset + ".nodePoses.txt")
        with open(filename, "w") as fout:
            nps = sorted(nodePoses.items(), key=lambda x: x[0])
            for node, pos in nps:
                fout.write(str(node))
                for p in pos:
                    fout.write(f"\t{p}")
                fout.write("\n")
        end = time.time()
        print(f"[writeNodePoses] [{dataset}] [{end - start:.2f}s] {len(nodePoses)} nodePoses")
        return filename

    @staticmethod
    def writeNodeCIDs(dataRoot: str, dataset: str, nodeCID: NodeCID) -> str:
        start = time.time()
        filename = os.path.join(dataRoot, dataset + ".nodeCIDs.txt")
        with open(filename, "w") as fout:
            for node, cid in nodeCID.items():
                fout.write(f"{node}\t{cid}\n")
        end = time.time()
        print(f"[writeNodeCIDs] [{dataset}] [{end - start:.2f}s] {len(nodeCID)} nodeCIDs")
        return filename

    @staticmethod
    def draw(dataRoot: str, dataset: str, dataFilename: str, clusterFilename: str, nodePoses: NodePosSet) -> None:
        filename = DataUtils.writeNodePoses(dataRoot, dataset, nodePoses)
        cmd = f"python draw.py {dataFilename} {filename} {clusterFilename}"
        print(">>>>>>>>>>>>", cmd)
        # os.system(cmd)

    @staticmethod
    def metrics(dataFilename: str, clusterFilename: str) -> None:
        cmd = f"python Metrics.py {dataFilename} {clusterFilename}"
        print(">>>>>>>>>>>>", cmd)
        # os.system(cmd)
