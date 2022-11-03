from typing import TypeVar, Generic, List
from aresta import Aresta
import sys

V = TypeVar('V')


def caminho_para(source: V, target: V) -> bool:
    visited = list()
    visited.append(source)

    queue = [source]

    while queue:
        n = queue.pop(0)
        if n == target:
            return True

        # nova fronteira de busca
        for i in graph.neighbors_for_vertex(n):
            if i not in visited:
                queue.append(i)
                visited.append(i)
    return False


class Grafo(Generic[V]):
    def __init__(self, vertices=None) -> None:
        if vertices is None:
            vertices = []
        self._vertices: List[V] = vertices
        self._arestas: List[List[Aresta]] = [[] for _ in vertices]

    def get_vertices(self):
        return self._vertices

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)  # Number of vertices

    @property
    def edge_count(self) -> int:
        return sum(map(len, self._arestas))  # Number of edges

    # Add a vertex to the graph and return its index
    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._arestas.append([])  # add empty list for containing edges
        return self.vertex_count - 1  # return index of added vertex

    # This is an undirected graph,
    # so we always add edges in both directions
    def add_edge(self, edge: Aresta) -> None:
        self._arestas[edge.u].append(edge)

    # Add an edge using vertex indices (convenience method)
    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge: Aresta = Aresta(u, v)
        self.add_edge(edge)

    # Add an edge by looking up vertex indices (convenience method)
    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v)

    # Find the vertex at a specific index
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    # Find the index of a vertex in the graph
    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    # Find the vertices that a vertex at some index is connected to
    def neighbors_for_index(self, index: int) -> List[V]:
        return list(map(self.vertex_at, [e.v for e in self._arestas[index]]))

    # Lookup a vertices index and find its neighbors (convenience method)
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))

    # Return all the edges associated with a vertex at some index
    def edges_for_index(self, index: int) -> List[Aresta]:
        return self._arestas[index]

    # Lookup the index of a vertex and return its edges (convenience method)
    def edges_for_vertex(self, vertex: V) -> List[Aresta]:
        return self.edges_for_index(self.index_of(vertex))

    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc


if __name__ == "__main__":
    distinct_vertices: List[str] = list()

    with open(sys.argv[1], encoding="UTF8") as f:
        lines = f.readlines()
        for line in lines:
            content = line.split(' ')
            if content[0] not in distinct_vertices:
                distinct_vertices.append(content[0])
            if content[2] not in distinct_vertices:
                distinct_vertices.append(content[2].strip())

        # creates the graph
        graph: Grafo[str] = Grafo(distinct_vertices)

        for line in lines:
            content = line.split(' ')
            graph.add_edge_by_vertices(content[0], content[2].strip())
    f.close()

    print("-" * 20)
    print(graph)
    print("-" * 20)

    n_connections = 0

    # para cada nodo no grafo
    new_combination: set = set()
    for primeiro_sabor in graph.get_vertices():
        for segundo_sabor in graph.get_vertices():
            if primeiro_sabor != segundo_sabor:
                if caminho_para(primeiro_sabor, segundo_sabor):
                    new_combination.add(f"{primeiro_sabor} -> {segundo_sabor}")

    print("Combinações para 2 sabores: ", len(new_combination))
    print(new_combination)

    # para cada nodo no grafo
    new_combination: set = set()
    for primeiro_sabor in graph.get_vertices():
        for segundo_sabor in graph.get_vertices():
            if primeiro_sabor != segundo_sabor:
                if caminho_para(primeiro_sabor, segundo_sabor):
                    for terceiro_sabor in graph.get_vertices():
                        if terceiro_sabor not in [primeiro_sabor, segundo_sabor]:
                            if caminho_para(segundo_sabor, terceiro_sabor):
                                new_combination.add(f"{primeiro_sabor} -> {segundo_sabor} -> {terceiro_sabor}")

    print("Combinações para 3 sabores: ", len(new_combination))
    print(new_combination)
