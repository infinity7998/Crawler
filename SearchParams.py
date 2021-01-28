class SearchParams:
    def __init__(self, max_depth: int = 5, max_nodes_bound: int = 50, max_edges_bound: int = 5000):
        self.max_depth = max_depth
        self.max_nodes_bound = max_nodes_bound
        self.max_edges_bound = max_edges_bound
        pass

    def __str__(self):
        return self.__dict__.__str__()
