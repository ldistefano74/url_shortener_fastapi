import string
from collections import Counter
import requests
from bs4 import BeautifulSoup

class Site:
    url: str = None
    title: ""

    def __init__(self, url, title):
        self.url = url
        self.title = title


class Storage:
    """Core class that may abstract from persistence"""

    __URLS = {}

    def process_url(self, url):
        next_id = self._get_next_id()
        title = self._get_url_title(url)

        self.__URLS[next_id] = Site(url, title)
        return next_id

    def get_statistics(self):
        stats = Counter(url.url for url in self.__URLS.values())
        return sorted(stats.items(), key=lambda x: x[1], reverse=True)[:100]

    def get_site(self, id) -> Site:
        return self.__URLS.get(id)

    def get_redirect_url(self, id):
        ret = None
        site = self.__URLS.get(id)
        if site:
            print("Redirect: ", site.url)
            ret = site.url

        return ret

    def _get_next_id(self):
        if len(self.__URLS):
            last = max(self.__URLS.keys())
        else:
            last = ""
        new = ""

        if not last or last[-1] == string.ascii_lowercase[-1]:
            new = last + string.ascii_lowercase[0]
        else:
            pos = string.ascii_lowercase.find(last[-1])
            new = last[:-1] + string.ascii_lowercase[pos + 1]

        return new

    def _get_url_title(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find('title').get_text()

