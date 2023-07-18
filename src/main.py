import time
from BlackHole import BlackHole
from DataUtils import DataUtils
from Network import Network
import os

if __name__ == "__main__":
    print("WARNING: srand(1) For Debug!")
    # srand(2) is not required in Python
    
    path1 = os.path.realpath(__file__)
    dataRoot = DataUtils.getDataRoot(path1)  # Assuming the getDataRoot function is defined correctly in DataUtils.py

    datasets = ["DBLP\\dblp"]
    dim = 2

    for dataset in datasets:
        start = time.time()
        network = Network()
        dataFilename = DataUtils.readNetwork(dataRoot, dataset, network)  # Assuming the readNetwork function is defined correctly in DataUtils.py
        nodePoses = {}
        nodeCID = {}
        BlackHole.exec(network, dim, nodePoses, nodeCID)
        clusterFilename = DataUtils.writeNodeCIDs(dataRoot, dataset, nodeCID)  # Assuming the writeNodeCIDs function is defined correctly in DataUtils.py
        end = time.time()
        print(f"[main] [{dataset}] [{end - start}s]")

        DataUtils.metrics(dataRoot, dataset)  # Assuming the metrics function is defined correctly in DataUtils.py
        DataUtils.draw(dataRoot, dataset)  # Assuming the draw function is defined correctly in DataUtils.py
