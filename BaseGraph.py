from collections import defaultdict
from abc import ABCMeta
from abc import abstractmethod
from typing import Iterable
from SearchParams import SearchParams
from copy import deepcopy as dc
import itertools
from math import inf
import time


class Node:
    def __init__(self):
        pass

    def value(self):
        return

    def label(self):
        return

    def data(self):
        return

    def __hash__(self):
        return hash(self.value())

    def __str__(self):
        return str(self.label())


class Edge:
    def __init__(self, start: Node, end: Node):
        self._start = start
        self._end = end
        pass

    def start(self):
        return self._start

    def end(self):
        return self._end

    def value(self):
        return

    def label(self):
        return

    def weight(self):
        return

    def __hash__(self):
        return hash(self.value())

    def __str__(self):
        return str(self.label())


class Graph:
    def __init__(self, name='', directed=True, search_params: SearchParams = None):
        self.adjacencies = dict()
        self.nodes = set()
        self.directed = directed
        self.edges = defaultdict(set)
        self.name = name
        self.search_params = search_params
        pass

    def neighbors(self, node: Node):
        if node in self.adjacencies:
            yield from self.adjacencies[node]

    def add_node(self, node: Node):
        if node not in self.adjacencies:
            self.nodes |= {node}
            self.adjacencies[node] = set()

    def add_nodes(self, nodes: Iterable[Node]):
        for node in nodes:
            self.add_node(node)
        pass

    def add_edge(self, start: Node, end: Node):
        edge = Edge(start, end)

        self.adjacencies[start] |= {(end, edge)}
        self.edges[edge] |= {(start, end)}

        if not self.directed:
            self.adjacencies[end] |= {(start, edge)}

    def add_edges(self, edges: Iterable[Edge]):
        for start, end in edges:
            self.add_edge(start, end)

    def bfs_explore(self, start: Node):
        _max_depth = self.search_params.max_depth
        _max_nodes_bound = self.search_params.max_nodes_bound
        _max_edges_bound = self.search_params.max_edges_bound

        _queue = [(start, None)]
        _visited_nodes = set()
        _visited_edges = set()
        _distances = defaultdict(lambda: inf)
        _distances[start] = 0

        def rest_of_bounds():
            return all(
                (
                    len(_visited_nodes) <= _max_nodes_bound,
                    len(_visited_edges) <= _max_edges_bound
                )
            )

        while _queue and rest_of_bounds():
            current, parent = _queue.pop(0)
            _visited_nodes |= {current}

            for nbr, edge in self.neighbors(current):
                if nbr not in _visited_nodes and edge not in _visited_edges:
                    if _distances[nbr] != inf and _distances[nbr] >= _max_depth:
                        continue
                    elif _distances[current] + 1 < _distances[nbr]:
                        _distances[nbr] = _distances[current] + 1
                        _visited_edges |= {edge}
                        _queue.append((nbr, current))
        for x in _distances:
            print(x, _distances[x])
        return _distances

    def __getitem__(self, key):
        if key in self.adjacencies:
            return self.adjacencies[key]
        raise Exception(f'No node of key: {key}')

    def __iter__(self):
        return iter(self.adjacencies)

    def __len__(self):
        return len(self.adjacencies)

    def adj(self):
        return self.adjacencies

    def size(self):
        return len(self.edges)

    def __str__(self):
        return f'Graph: {self.name} has {len(self.adjacencies)} nodes.'
