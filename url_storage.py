import string
import db_lib
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
    """Storage class that abstract from persistence"""

    def process_url(self, url):
        next_id = self._get_next_id()
        title = self._get_url_title(url)

        self._store_url(next_id, url, title)
        return next_id

    def _get_next_id(self) -> str:
        last = self._get_last_id()

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

    def _get_last_id(self) -> str:
        return ""

    def get_statistics(self):
        return []

    def get_site(self, id) -> Site | None:
        return None

    def get_redirect_url(self, id) -> str | None:
        return None

    def _store_url(self, id, url, title):
        pass


class InMemoryStorage(Storage):
    """Core class that may abstract from persistence"""

    __URLS = {}

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

    def _get_last_id(self):
        if len(self.__URLS):
            last = max(self.__URLS.keys())
        else:
            last = ""
        return last

    def _store_url(self, id, url, title):
        self.__URLS[id] = Site(url, title)


class DBStorage(Storage):
    def _get_last_id(self):
        return db_lib.get_max_site_id()

    def _store_url(self, id, url, title):
        db_lib.append_site(id, url, title)

    def get_redirect_url(self, id):
        url = None
        if site := db_lib.get_site(id):
            url = site[1]
        return url

    def get_site(self, id) -> Site:
        site = None
        if db_site := db_lib.get_site(id):
            site = Site(db_site[1], db_site[2])

        return site

    def get_statistics(self):
        return db_lib.get_usage()
