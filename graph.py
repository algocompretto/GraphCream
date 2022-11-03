from typing import TypeVar, Generic, List
from edge import Edge
from itertools import combinations_with_replacement
import sys

V = TypeVar('V')


def path_to(source: V, target: V) -> bool:
    visited = list()
    visited.append(source)

    queue = [source]

    while queue:
        n = queue.pop(0)
        if n == target:
            return True

        # new frontier search
        for i in g.neighbors_for_vertex(n):
            if i not in visited:
                queue.append(i)
                visited.append(i)
    return False


class Graph(Generic[V]):
    def __init__(self, vertices=None) -> None:
        if vertices is None:
            vertices = []
        self._vertices: List[V] = vertices
        self._edges: List[List[Edge]] = [[] for _ in vertices]

    def get_vertices(self):
        return self._vertices

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)  # Number of vertices

    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))  # Number of edges

    # Add a vertex to the graph and return its index
    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([])  # add empty list for containing edges
        return self.vertex_count - 1  # return index of added vertex

    # This is an undirected graph,
    # so we always add edges in both directions
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)

    # Add an edge using vertex indices (convenience method)
    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge: Edge = Edge(u, v)
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
        return list(map(self.vertex_at, [e.v for e in self._edges[index]]))

    # Lookup a vertices index and find its neighbors (convenience method)
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))

    # Return all the edges associated with a vertex at some index
    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]

    # Lookup the index of a vertex and return its edges (convenience method)
    def edges_for_vertex(self, vertex: V) -> List[Edge]:
        return self.edges_for_index(self.index_of(vertex))

    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc


if __name__ == "__main__":
    distinct_vertices: List[str] = list()

    # opening file read
    with open(sys.argv[1], encoding="UTF8") as f:
        lines = f.readlines()
        for line in lines:
            content = line.split(' ')
            if content[0] not in distinct_vertices:
                distinct_vertices.append(content[0])
            if content[2] not in distinct_vertices:
                distinct_vertices.append(content[2].strip())

        # creates the graph
        g: Graph[str] = Graph(distinct_vertices)

        # creating the edges
        for line in lines:
            content = line.split(' ')
            g.add_edge_by_vertices(content[0], content[2].strip())
    f.close()

    import time

    start = time.time()

    # generates combinations of vertices
    all_combinations: set = set()
    for first_flavor, second_flavor in combinations_with_replacement(g.get_vertices(), 2):
        if first_flavor != second_flavor:
            if path_to(first_flavor, second_flavor):
                all_combinations.add(f"{first_flavor} -> {second_flavor}")
    print("All combinations for two flavors: ", len(all_combinations))
    print("Result in: ", time.time() - start)

    start = time.time()
    # generates combinations of vertices
    all_combinations: set = set()
    for first_flavor, second_flavor, third_flavor in combinations_with_replacement(g.get_vertices(), 3):
        if first_flavor != second_flavor:
            if path_to(first_flavor, second_flavor):
                if third_flavor not in [first_flavor, second_flavor]:
                    if path_to(second_flavor, third_flavor):
                        all_combinations.add(f"{first_flavor} -> {second_flavor} -> {third_flavor}")

    print("All combinations for three flavors: ", len(all_combinations))
    print("Result in: ", time.time() - start)
