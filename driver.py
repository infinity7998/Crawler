from GraphCrawler import GraphCrawler
import os
import time
from pathlib import Path


URL = ''
FILENAME = ''
TOP = 'data'
DOMAIN = FILENAME


def curr_time():
    return time.strftime("%Y%m%d-%H%M%S")


def init():
    return GraphCrawler(
        url=URL,
        name='Crawley',
        headless=False,
        period=2,
        collect='video',
        must_include=FILENAME
    )


def main():
    folder = Path(f'{TOP}/{DOMAIN}')
    if not folder.is_dir():
        os.mkdir(f'{TOP}/{DOMAIN}')

    folder = Path(f'{TOP}/{DOMAIN}')

    crawler = init()
    crawler.initialize_root()
    crawler.graph.bfs_explore(start=crawler.root)
    _dict = crawler.get_data()

    for _key in _dict:
        with open(f'{folder}/{curr_time()}_{FILENAME}_{str(_key).replace(" ", "").replace("/", "")}.txt', 'w') as fl:
            fl.writelines([str(_key).replace(" ", "") + "\n\n"])
            fl.writelines(_dict[_key])
    print('done!')
    pass


if __name__ == '__main__':
    main()
