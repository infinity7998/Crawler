import selenium as se
from BaseGraph import Node, Edge, Graph
from SearchParams import SearchParams
from collections import defaultdict
from math import inf
from typing import List, Dict, Set, Tuple


class DOMNode(Node):
    def __init__(self, dom_node: se.webdriver.remote.webelement.WebElement, value=None, label=None, data=None):
        super().__init__()
        self._value = value
        self._label = label
        self._data = data
        self._node_id = None
        self._underlying_dom_node = None

        if dom_node is None:
            return

        self._underlying_dom_node = dom_node
        self._node_id = dom_node.id

        if dom_node.tag_name == 'a':
            self._value = dom_node.get_attribute('href')
            temp = dom_node.get_attribute('text')
            if temp.strip() != '':
                self._label = temp
            else:
                self._label = 'unlabelled/link'

        elif dom_node.tag_name == 'img':
            self._value = dom_node.get_attribute('src')
            temp = dom_node.get_attribute('alt')
            if temp.strip() != '':
                self._label = temp
            else:
                self._label = 'no-alt/image'
        else:
            pass

    def __hash__(self):
        return hash(self._value)

    def value(self):
        return self._value

    def label(self):
        return self._label

    def data(self):
        return self._data

    def get_underlying_dom_node(self):
        return self._underlying_dom_node

    def get_node_id(self):
        return self._node_id

    def __str__(self):
        return str(self.label())


class DOMEdge(Edge):
    def __init__(
            self,
            start: DOMNode,
            end: DOMNode,
            weight: float = 1.0,
            value: str = '',
            label: str = ''
    ):
        super().__init__(start=start, end=end)

        self._label = label if label else f'({str(start)} ==> {str(end)}, weight: {weight})'
        self._value = value if value else self._label
        self._weight = weight
        self._start = start
        self._end = end
        self._edge_id = f'{start.get_node_id()}==>{end.get_node_id()}'

    def value(self):
        return self._value

    def label(self):
        return self._label

    def weight(self):
        return self._weight

    def start(self):
        return self._start

    def end(self):
        return self._end

    def get_edge_id(self):
        return self._edge_id

    def __str__(self):
        return f'Label: {self._label}\nValue: {self._value}'

    def __hash__(self):
        return hash(self.get_edge_id())


class DOMGraph(Graph):
    def __init__(self, get_neighbors, name='', directed=True, **kwargs):
        self.name = name
        self.directed = directed
        self.get_neighbors = get_neighbors
        super().__init__(name=name, directed=directed, **kwargs)

    def neighbors(self, node: DOMNode):
        if node in self.adjacencies:
            yield from self.adjacencies[node]
        else:
            yield from []

    def bfs_explore(self, start: DOMNode):

        _queue: List[Tuple[DOMNode, DOMNode]] = [(start, None)]
        _visited_nodes = set()
        _visited_edges = set()
        _distances = defaultdict(lambda: inf)
        _distances[start] = 0

        def rest_of_bounds():
            return all(
                (
                    len(_visited_nodes) <= self.search_params.max_nodes_bound,
                    len(_visited_edges) <= self.search_params.max_edges_bound
                )
            )

        while _queue and rest_of_bounds():
            current, parent = _queue.pop(0)
            while current.value() in _visited_nodes and _queue:
                current, parent = _queue.pop(0)
            _visited_nodes |= {current.value()}

            if len(self.adjacencies[current]) == 0:
                for _dom_node in self.get_neighbors(current):
                    if _dom_node not in self.adjacencies:
                        self.add_node(_dom_node)
                    self.add_edge(current, _dom_node)
                pass
            for nbr, edge in self.neighbors(current):
                if nbr.value() not in _visited_nodes:
                    if _distances[nbr] != inf and _distances[nbr] >= self.search_params.max_depth:
                        continue
                    elif _distances[current] + 1 < _distances[nbr]:
                        _distances[nbr] = _distances[current] + 1
                        _visited_edges |= {edge.value()}
                        _queue.append((nbr, current))
        return _visited_nodes

    def __str__(self):
        return super().__str__()
