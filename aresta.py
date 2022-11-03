from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Aresta:
    u: int  # vertice "de"
    v: int  # vertice "para"

    def reverso(self) -> Aresta:
        return Aresta(self.v, self.u)

    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"
