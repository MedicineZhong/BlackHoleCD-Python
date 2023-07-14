from GraphDrawing import GraphDrawing
from DBScan import DBScan
import time

class BlackHole:
    @staticmethod
    def exec(network, dim, nodePoses, nodeCID):
        start = time.time()
        nodePoses.clear()
        a = 0.01
        r = 0.0
        graphDrawing = GraphDrawing(dim, a, r, 50)
        graphDrawing.exec(network, nodePoses)
        dbscan = DBScan(nodePoses, network.getNodeNum(), 0, nodeCID)
        dbscan.dbscan()
        end = time.time()
        print(f"[BlackHole::exec] [{end - start}s]")

