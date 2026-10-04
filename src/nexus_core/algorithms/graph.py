"""
Graph Algorithms Module
=======================
Implements state-of-the-art graph exploration, shortest path, and topological ordering.
"""

from typing import Dict, List, Optional, Set, Tuple, Hashable, TypeVar
import heapq

T = TypeVar("T", bound=Hashable)


class GraphNode:
    """Represents a graph vertex with adjacent weighted edges."""

    def __init__(self, key: str) -> None:
        self.key = key
        self.neighbors: Dict["GraphNode", float] = {}

    def add_edge(self, neighbor: "GraphNode", weight: float = 1.0) -> None:
        self.neighbors[neighbor] = weight

    def __repr__(self) -> str:
        return f"GraphNode({self.key!r})"


class DirectedGraph:
    """Directed weighted graph with memory-efficient adjacency map."""

    def __init__(self) -> None:
        self.nodes: Dict[str, GraphNode] = {}

    def get_or_create(self, key: str) -> GraphNode:
        if key not in self.nodes:
            self.nodes[key] = GraphNode(key)
        return self.nodes[key]

    def add_edge(self, u: str, v: str, weight: float = 1.0) -> None:
        node_u = self.get_or_create(u)
        node_v = self.get_or_create(v)
        node_u.add_edge(node_v, weight)

    def dijkstra(self, source_key: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        """
        Computes single-source shortest path using a min-heap priority queue.
        Time Complexity: O((V + E) log V)
        Space Complexity: O(V)
        """
        if source_key not in self.nodes:
            raise KeyError(f"Source vertex '{source_key}' does not exist in graph.")

        distances: Dict[str, float] = {k: float("inf") for k in self.nodes}
        predecessors: Dict[str, Optional[str]] = {k: None for k in self.nodes}
        distances[source_key] = 0.0

        pq: List[Tuple[float, str]] = [(0.0, source_key)]

        while pq:
            current_dist, current_key = heapq.heappop(pq)

            if current_dist > distances[current_key]:
                continue

            current_node = self.nodes[current_key]
            for neighbor, weight in current_node.neighbors.items():
                distance = current_dist + weight
                if distance < distances[neighbor.key]:
                    distances[neighbor.key] = distance
                    predecessors[neighbor.key] = current_key
                    heapq.heappush(pq, (distance, neighbor.key))

        return distances, predecessors

    def topological_sort(self) -> List[str]:
        """
        Kahn's Algorithm for Topological Sorting on Directed Acyclic Graphs (DAG).
        Time Complexity: O(V + E)
        Raises:
            ValueError: If a cycle is detected.
        """
        in_degree: Dict[str, int] = {k: 0 for k in self.nodes}
        for u in self.nodes.values():
            for v in u.neighbors:
                in_degree[v.key] += 1

        queue: List[str] = [k for k, deg in in_degree.items() if deg == 0]
        result: List[str] = []

        while queue:
            node_key = queue.pop(0)
            result.append(node_key)
            for neighbor in self.nodes[node_key].neighbors:
                in_degree[neighbor.key] -= 1
                if in_degree[neighbor.key] == 0:
                    queue.append(neighbor.key)

        if len(result) != len(self.nodes):
            raise ValueError("Graph contains at least one directed cycle; topological sort impossible.")

        return result
