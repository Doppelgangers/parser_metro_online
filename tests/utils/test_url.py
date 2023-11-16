import pytest

from utils.urls import URL


def test_init():
    url = URL("https://example.com/path?a=1&b=2")
    assert url.url == "https://example.com/path?a=1&b=2"
    assert url._query == {"a": "1", "b": "2"}

    url2 = URL(url)
    assert url.url == url2.url
    assert url is not url2

    url = URL("https://example.com/path")
    assert url.url == "https://example.com/path"
    assert url._query == {}


def test_update_query():
    url = URL("https://example.com/path?a=1&b=2")
    url.update_query(c=3)
    assert url.url == "https://example.com/path?a=1&b=2&c=3"
    assert url._query == {"a": "1", "b": "2", "c": "3"}

    url = URL(r"https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba")
    url.update_query(in_stock=1)
    assert url._query == {"in_stock": "1"}
    assert url.url == r"https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?in_stock=1"


def test_set_query():
    url = URL("https://example.com/path?a=1&b=2")
    url.set_query(d="4", e="5")
    assert url._query == {"d": "4", "e": "5"}
    assert url.url == "https://example.com/path?d=4&e=5"

    url = URL(r"https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba")
    url.set_query(in_stock=1)
    assert url._query == {"in_stock": "1"}
    assert url.url == r"https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?in_stock=1"


def test_clean_query():
    url = URL("https://example.com/path?a=1&b=2")
    url.clean_query()
    assert url.url == "https://example.com/path"
    assert url._query == {}

    url = URL(r"https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba")
    url.clean_query()
    assert url.url == r"https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba"


def test_root_url():
    url = URL(r"https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?from=under_search")
    assert url.root_url == r"https://online.metro-cc.ru"


def test_clean_link():
    url = URL(r"https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?from=under_search")
    assert url.clean_link == "https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba"

    url = URL(r"https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba")
    assert url.clean_link == "https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba"


if __name__ == "__main__":
    pytest.main()
