from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Edge:
    u: int  # vertice "de"
    v: int  # vertice "para"

    def reverso(self) -> Edge:
        return Edge(self.v, self.u)

    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"
