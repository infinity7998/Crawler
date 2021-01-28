import selenium.webdriver
import selenium as se
import itertools
from time import sleep


class BaseCrawler:
    """
    A Crawler wrapper of selenium Firefox WebDriver.
    """

    def __init__(self, url='', headless=True, **kwargs):
        self.driver = None
        self.url = url
        self.headless = headless
        self.period = kwargs.get('period', 2)
        pass

    def setup(self, options=None):
        if not options:
            options = selenium.webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('headless')
        self.driver = selenium.webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        sleep(self.period)

    def _lazy_init(self, **kwargs):
        if self.driver is None:
            self.setup(**kwargs)
        return

    def get(self, url=''):
        if url:
            self.url = url
        self.driver.implicitly_wait(5)
        self.driver.get(self.url)
        return self.driver

    def find_element(self, tag, attributes=()):
        self._lazy_init()
        all_elements = self.driver.find_elements_by_tag_name(tag)
        it1, it2 = itertools.tee(all_elements, 2)
        yield from zip(it1, map(lambda x: {attr: x.get_attribute(attr) for attr in attributes}, it2))

    def find_anchors(self, *args, **kwargs):
        yield from self.find_element(tag='a', *args, **kwargs)

    def find_images(self, *args, **kwargs):
        yield from self.find_element(tag='img', *args, **kwargs)

    def find_videos(self, *args, **kwargs):
        yield from self.find_element(tag='video', *args, **kwargs)

    def find_all_text(self):
        for _dom, _dict in self.find_element(tag='body'):
            yield _dom.text

    def driver(self):
        return self.driver

    def __str__(self):
        return f'Chrome crawler for: {self.url} \n Initialized: \t {self.driver is not None}'

    def done(self):
        self.driver.close()
        self.driver = None
