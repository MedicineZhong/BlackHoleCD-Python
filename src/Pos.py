import math
from typing import List, Union


class Pos:
    def __init__(self, dim: int):
        self.dim = dim
        self.pos = [0.0] * dim

    def __add__(self, other: 'Pos') -> 'Pos':
        r = Pos(self.dim)
        for i in range(self.dim):
            r.pos[i] = self.pos[i] + other.pos[i]
        return r

    def __sub__(self, other: 'Pos') -> 'Pos':
        r = Pos(self.dim)
        for i in range(self.dim):
            r.pos[i] = self.pos[i] - other.pos[i]
        return r

    def __mul__(self, f: float) -> 'Pos':
        r = Pos(self.dim)
        for i in range(self.dim):
            r.pos[i] = self.pos[i] * f
        return r

    def __truediv__(self, f: float) -> 'Pos':
        r = Pos(self.dim)
        for i in range(self.dim):
            r.pos[i] = self.pos[i] / f
        return r

    def __neg__(self) -> 'Pos':
        r = Pos(self.dim)
        for i in range(self.dim):
            r.pos[i] = -self.pos[i]
        return r

    def __eq__(self, other: 'Pos') -> bool:
        return self.dim == other.dim and self.pos == other.pos

    def __ne__(self, other: 'Pos') -> bool:
        return not self.__eq__(other)

    def __iadd__(self, other: 'Pos') -> 'Pos':
        for i in range(self.dim):
            self.pos[i] += other.pos[i]
        return self

    def __isub__(self, other: 'Pos') -> 'Pos':
        for i in range(self.dim):
            self.pos[i] -= other.pos[i]
        return self

    def __imul__(self, f: float) -> 'Pos':
        for i in range(self.dim):
            self.pos[i] *= f
        return self

    def __itruediv__(self, f: float) -> 'Pos':
        for i in range(self.dim):
            self.pos[i] /= f
        return self

    def __getitem__(self, i: int) -> float:
        return self.pos[i]

    def __setitem__(self, i: int, value: float) -> None:
        self.pos[i] = value

    def setZero(self) -> None:
        self.pos = [0.0] * self.dim

    def length(self) -> float:
        r = 0.0
        for i in self.pos:
            r += i * i
        return math.sqrt(r)

    def eucDis(self) -> float:
        euc = 0.0
        for i in self.pos:
            euc += i * i
        return euc

    def getDim(self) -> int:
        return self.dim
