import os
import sys
from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Generic, List, Set, TypeVar, Union

# Generics
V = TypeVar('V')
os.makedirs("results/", exist_ok=True)


def path_to(source: V, target: V) -> bool:
    """
    Using Breadth-First Search, checks if a node target is reachable
    starting from source node.

    Args:
        source: node where the path begins
        target:  node where the algorithm wants to end

    Returns:
        bool: True if there is a path between source and targe, False otherwise
    """
    # Creates the visited and queue lists
    visited: List[V] = list()
    visited.append(source)

    queue: List[V] = [source]

    # While there is frontier to be explored
    while queue:
        # Removes the first element and checks if it is target value
        n: V = queue.pop(0)
        if n == target: return True

        # Explore the adjacent vertices
        for i in g.neighbors_for_vertex(n):
            if i not in visited:
                queue.append(i)
                visited.append(i)
    return False


def write_to_file(file_name: str, series: Union[Set[str], List[str]]) -> None:
    """
    Given a set of strings with possible flavor combinations, write them to a
    file.

    Args:
        file_name: path to write the file
        series: Set of string values to write on file
    """
    with open(file_name, mode="w", encoding="UTF8") as file:
        for elem in series:
            file.write(elem)
            file.write("\n")
    file.close()


@dataclass
class Edge:
    u: int  # "from" vertex
    v: int  # "to" vertex

    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"


class Graph(Generic[V]):
    """
    A generic Graph class to be used in the current work.
    """

    def __init__(self, vertices=None) -> None:
        if vertices is None:
            vertices = []
        self._vertices: List[V] = vertices
        self._edges: List[List[Edge]] = [[] for _ in vertices]

    def get_vertices(self):
        return self._vertices

    @property
    def vertex_count(self) -> int:
        # Number of vertices
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        # Number of edges
        return sum(map(len, self._edges))

    def add_vertex(self, vertex: V) -> int:
        """
        Add a vertex to the graph and return its index.

        Args:
            vertex: The vertex you want to get the index

        Returns:
            The index integer
        """
        self._vertices.append(vertex)
        self._edges.append([])
        return self.vertex_count - 1

    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)

    def add_edge_by_indices(self, u: int, v: int) -> None:
        """
        Add an edge using vertex indices

        Args:
            u: First node you want to add
            v: Second node you want to add
        """
        edge: Edge = Edge(u, v)
        self.add_edge(edge)

    def add_edge_by_vertices(self, first: V, second: V) -> None:
        """
        Add an edge by looking up the vertex indices.

        Args:
            first: First node of the edge
            second: Second node of the edge
        """
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v)

    def vertex_at(self, index: int) -> V:
        """
        Find the vertex at a specific index.

        Args:
            index: Index of the vertex you want

        Returns:
            Returns the vertex item of type V
        """
        return self._vertices[index]

    # Find the index of a vertex in the graph
    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    # Find the vertices that a vertex at some index is connected to
    def neighbors_for_index(self, index: int) -> List[V]:
        return list(map(self.vertex_at, [e.v for e in self._edges[index]]))

    # Lookup a vertices index and find its neighbors
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))

    # Return all the edges associated with a vertex at some index
    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]

    # Lookup the index of a vertex and return its edges
    def edges_for_vertex(self, vertex: V) -> List[Edge]:
        return self.edges_for_index(self.index_of(vertex))

    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc

    def bfs(self, initial, goal, successors):
        frontier: Queue[Node[V]] = Queue()
        frontier.push(Node(initial, None))

        explored: Set[V] = {initial}

        while not frontier.empty:
            current_node: Node[V] = frontier.pop()
            current_state: V = current_node.state
            current_vertex = self.vertex_at(self.index_of(current_state))

            if initial == goal: return True
            
            for child in self.neighbors_for_vertex(current_vertex):
                if child in explored:
                    continue
                explored.add(child)
                frontier.push(Node(child, current_node))
        return False



if __name__ == "__main__":
    distinct_vertices: List[str] = list()

    # opening file and reading from it
    with open(sys.argv[1], encoding="UTF8") as f:
        lines: List[str] = f.readlines()
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
            content: List[str] = line.split(' ')
            g.add_edge_by_vertices(content[0], content[2].strip())
    f.close()


    # generates combinations of vertices
    all_combinations: Set[str] = set()
    for first_flavor, second_flavor in permutations(g.get_vertices(), 2):
        if first_flavor != second_flavor:
            if path_to(first_flavor, second_flavor):
                all_combinations.add(f"{first_flavor} -> {second_flavor}")
    print("All combinations for two flavors: ", len(all_combinations))

    all_combinations: Set[str] = set()
    for first_flavor, second_flavor, third_flavor in permutations(g.get_vertices(), 3):
            if first_flavor != second_flavor and path_to(first_flavor, second_flavor):
                if third_flavor not in [first_flavor, second_flavor] and path_to(second_flavor, third_flavor):
                    all_combinations.add(f"{first_flavor} -> {second_flavor} -> {third_flavor}")
    print("All combinations for three flavors: ", len(all_combinations))