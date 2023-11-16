from typing import Self
from urllib.parse import urlencode, parse_qs, parse_qsl, urlparse


class URL:

    def __init__(self, url: str | Self):
        self.url = str(url)
        if "?" in self.url:
            self._query = dict(parse_qsl(self.url.split("?")[1], True))
        else:
            self._query = {}

    def update_query(self, **kwargs):
        """
        Добавляет новые параметры к существующему GET-запросу.
        """
        for key, value in kwargs.items():
            self._query[key] = str(value)
        self.url = f"{self.url.split('?')[0]}?{urlencode(self._query)}"

    def set_query(self, **kwargs):
        """
        Удаляет старые параметры GET-запроса и устанавливает переданные.
        """
        self._query = {key: str(value) for key, value in kwargs.items()}
        self.url = f"{self.url.split('?')[0]}?{urlencode(self._query)}"

    def clean_query(self):
        """
        Удаляет GET-запросы из ссылки.
        """

        self.url = self.url.split("?")[0]
        self._query = {}

    @property
    def root_url(self):
        parsed_url = urlparse(self.url)
        return parsed_url.scheme + "://" + parsed_url.netloc

    @property
    def clean_link(self):
        if "?" in self.url:
            return self.url.split("?")[0]
        return self.url

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url
