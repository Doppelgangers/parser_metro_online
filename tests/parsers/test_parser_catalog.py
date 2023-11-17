import requests

from parsers.parser_catalog import ParserCatalog

test_data = requests.get("https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?in_stock=1").text
parser_cat = ParserCatalog(test_data)


def test_address():
    assert len(parser_cat.address) >= 3


def test_pagination_list():
    assert type(parser_cat.pagination_list) == range


def test_items():
    items = parser_cat.items
    assert type(items) == list
    assert type(items[0]) == dict

    val = items[0]

    assert type(val.get("id")) == int
    assert type(val.get("title")) == str
    assert type(val.get("regular_price")) == float
    assert type(val.get("promo_price")) == float or None
    assert "/" in val.get("url")


def test_title():
    assert type(parser_cat.title) == str
    assert len(parser_cat.title) >= 2

