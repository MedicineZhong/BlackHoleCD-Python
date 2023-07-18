from Network import Network, EdgeSet, NodeSet, V1, V2
from type import NodePosSet
from typing import List
from OctTree import OctTree
from Pos import Pos
import time
import math
import random

class GraphDrawing:
    def __init__(self, dim: int, a: float, r: float, nIters: int):
        self.dim = dim
        self.a = a
        self.r = r
        self.fa = a
        self.fr = r
        self.nIters = nIters
    
    def exec(self, network: Network, nodePoses: NodePosSet) -> None:
        start = time.time()
        nodes = network.getNodeSet()
        edges = network.getEdgeSet()
        
        for node in nodes:
            nodePoses[node] = self.get_random_pos()

        nodeVec = list(nodes)

        fs = {}
        tf = Pos(self.dim)
        
        iter = 0
        while True:
            tree = OctTree(self.dim, nodePoses)
            tree.assign(network, nodeVec, 0)
            
            self.update_param(iter)
            
            for edge in edges:
                v1, v2 = V1(edge), V2(edge)
                self.cal_attractive_force(nodePoses[v1], nodePoses[v2], self.a, tf)
                if v1 in fs:
                    fs[v1] += tf
                else:
                    fs[v1] = tf
                
                tf = -tf
                
                if v2 in fs:
                    fs[v2] += tf
                else:
                    fs[v2] = tf

            for v1 in nodes:
                self.cal_repulsive_force(nodePoses[v1], tree, self.r, tf)
                fs[v1] += tf * network.getFactor(v1)
                
            minEnergy = self.cal_energy(network, tree, self.a, self.r, nodePoses)
            bestGamma = -1
            maxGamma = 1 << 6
            
            def test_gamma(gamma):
                newPoses = nodePoses.copy()
                rGamma = 1.0 / gamma
                for node in nodes:
                    newPoses[node] += fs[node] * rGamma
                energy = self.cal_energy(network, tree, self.a, self.r, newPoses)
                nonlocal bestGamma, minEnergy
                if bestGamma == -1 or energy < minEnergy:
                    bestGamma = gamma
                    minEnergy = energy
            
            for gamma in range(32, 0, -1):
                if bestGamma == -1 or (bestGamma >> 1) == gamma:
                    test_gamma(gamma)
            
            for gamma in range(64, 129):
                if bestGamma == (gamma >> 1):
                    test_gamma(gamma)
            
            if bestGamma != -1:
                gamma = 1.0 / bestGamma
                for node in nodes:
                    nodePoses[node] += fs[node] * gamma
            
            print(f"[iter = {iter}] gamma = {bestGamma}, energy = {minEnergy}, a = {self.a}, r = {self.r}")
            
            if iter > self.nIters:
                break
            
            iter += 1
        
        end = time.time()
        print(f"[GraphDrawing::exec] [{end - start}s] iter = {iter}")
    
    def get_random_pos(self) -> Pos:
        p = Pos(self.dim)
        for i in range(self.dim):
            p[i] = random.random() - 0.5  #(random.random() + 1) / 32767 
        return p
    
    def cal_attractive_force(self, u: Pos, v: Pos, a: float, fa: Pos) -> None:
        fa = v - u
        dst = fa.length()
        fa *= dst ** (a - 2)
    
    def cal_repulsive_force(self, u: Pos, tree: OctTree, r: float, fr: Pos) -> None:
        fr = u - tree.massCenter
        dist = fr.length()
        
        if dist < 1e-6:
            return
        
        if not tree.isLeaf and dist < 1.0 * tree.width():
            fr.setZero()
            t = Pos(fr.getDim())
            for nd in tree.data:
                if isinstance(nd, OctTree):
                    self.cal_repulsive_force(u, nd, r, t)
                    fr += t
            return
        
        fr *= tree.weight * dist ** (r - 2)
    
    def cal_energy(self, network: Network, tree: OctTree, a: float, r: float, nodePoses: NodePosSet) -> float:
        return self.cal_attractive_energy(network.getEdgeSet(), a, nodePoses) - self.cal_repulsive_energy(network, tree, r, nodePoses)
    
    def cal_enrgy_core(self, pu: Pos, pv: Pos, p: float) -> float:
        dst = (pu - pv).length()
        if abs(dst) < 1e-6:
            return 0.0
        return math.log(dst) if abs(p) < 1e-6 else  math.pow(dst, p) / p #todo
    
    
    def cal_enrgy_core_tree(self, pu: Pos, tree: OctTree, p: float) -> float:
        dist = (tree.massCenter - pu).length()
        if(abs(dist) < 1e-6):
            return 0.0
        
        if(not tree.isLeaf and dist < 1.0 * tree.width()):
            energy = 0.0
            for nd in tree.data:
                if (nd.tr is not None):
                    energy += self.cal_enrgy_core_tree(pu, nd.tr, p)
            return energy
        
        return tree.weight * self.cal_enrgy_core(pu, tree.massCenter, p)
    
    def cal_attractive_energy(self, edges :EdgeSet, a: float, nodePoses: NodePosSet) -> float:
        energy = 0.0
        for edge in edges:
            u, v = V1(edge), V2(edge)
            energy += 2 * self.cal_enrgy_core(nodePoses[u], nodePoses[v], a)
        return energy
    
    def cal_repulsive_energy(self, network: Network, tree: OctTree, r: float, nodePoses: NodePosSet) -> float:
        
        nodes: NodeSet = network.getNodeSet()
        energy = 0.0
        for u in nodes:
            f = network.getFactor(u)
            energy += f * self.cal_enrgy_core_tree(nodePoses[u], tree, r)
            
        return energy
    
    
    def update_param(self, iter: int):
        if iter >= 50 and self.fr < 1.0:
            self.a = self.fa
            self.r = self.fr
            
            if iter <= 0.6 * self.nIters:
                self.a = self.a + 1.1 * (1.0 - self.fr)
                self.r = self.r + 0.9 * (1.0 - self.fr)
            elif iter <= 0.9 * self.nIters:
                self.a = self.a + 0.1 * (1.0 - self.fr) * (0.9 - float(iter) / self.nIters) / 0.3
                self.r = self.r + 0.1 * (1.0 - self.fr) * (0.9 - float(iter) / self.nIters) / 0.3
    
    