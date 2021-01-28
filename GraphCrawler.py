from BaseCrawler import BaseCrawler
from DOMGraph import DOMGraph, DOMNode
from SearchParams import SearchParams
from time import sleep
from typing import Dict, List


class GraphCrawler(BaseCrawler):
    def __init__(self,
                 url: str = '',
                 name: str = '',
                 period: float = 2,
                 collect: str = 'text',
                 must_include: str = '',
                 **kwargs
                 ):
        super().__init__(url=url, period=period, **kwargs)
        self.root = None
        self.name = name
        self.cache = dict()
        self.period = period
        self.collect = collect
        self.must_include = must_include
        self._data: Dict[DOMNode, List[str]] = dict()
        self.graph = DOMGraph(self.fetch_neighbors, name=name, search_params=SearchParams())
        pass

    def _filter_content(self):
        _content = []
        if self.collect == 'text':
            _content = list(self.find_all_text())
        elif self.collect == 'img':
            for _dom, _dict in self.find_images():
                src = _dom.get_attribute("src")
                alt = _dom.get_attribute("alt")
                _content.append(f'{src} {alt if alt else "No-Alt"}\n')
        elif self.collect == 'anchor':
            for _dom, _dict in self.find_anchors():
                href = _dom.get_attribute('href')
                text = _dom.get_attribute('text')
                _content.append(f'{href} {text if text else "No-Text"}\n')
        elif self.collect == 'video':
            for _dom, _dict in self.find_videos():
                href = _dom.get_attribute('src')
                text = _dom.get_attribute('text')
                _content.append(f'{href} {text if text else "No-Text"}\n')
        return _content

    def fetch_neighbors(self, node: DOMNode):
        if node not in self._data or node not in self.cache:
            url = node.value()
            if url and self.must_include not in url:
                print('Skipped scraping: ', node)
                yield from []
                return
            self.get(url)
            sleep(self.period)
            self._data[node] = self._filter_content()
            self.cache[node] = set()
            for _dom, _dict in self.find_anchors(attributes=("href", "text")):
                self.cache[node] |= {(DOMNode(_dom, value=_dict["href"], label=_dict["text"], data=self._data[node]))}
            print('Just scraped: ', node)
            print(f'Current Data for {node} is:', self._data[node])
        yield from self.cache[node]

    def initialize_root(self):
        if not self.root:
            self.root = DOMNode(
                dom_node=None,
                value=self.url,
                label=f'Landing',
                data=self._filter_content()
            )
            self.graph.add_node(self.root)
            self._data[self.root] = self._filter_content()

        for _dom_elem, _dict in self.find_anchors(attributes=["href", "text"]):
            node = DOMNode(dom_node=_dom_elem, data='')
            self.graph.add_node(node)
            self.graph.add_edge(start=self.root, end=node)

        return self.graph

    def get_data(self) -> Dict[DOMNode, List[str]]:
        return self._data

    def __repr__(self):
        return self.__str__()

    #     @staticmethod
    #     def use_neighbors(graph):

    #         print(graph)
    #         return lambda x: [(None, None)]

    def __str__(self):
        return f'GraphCrawler: {self.name}, rooted at: {self.url}.\nMy cache is: {str(self.cache)}.'
