import asyncio
import json
import re
from copy import copy
from datetime import datetime

import aiohttp
import requests


from parsers.parser_catalog import ParserCatalog
from parsers.parser_product import ParserProduct
from utils.urls import URL
import settings


class MetroOnlineScraper:
    def __init__(self, uri: URL, metro_store_id: int, in_stock: bool = True):
        self._uri = uri
        self._in_stock = in_stock
        self._cookies = copy(settings.cookies)
        self._cookies['metroStoreId'] = f'{metro_store_id}'

    def get_page_category(self, page=None) -> str:
        local_url = URL(self._uri)
        if self._in_stock:
            local_url.update_query(in_stock=1)
        if page:
            local_url.update_query(page=page)
        return requests.get(local_url, cookies=self._cookies, headers=settings.headers).text

    @property
    def page_category(self, html_page: str = None):
        if not html_page:
            html_page = self.get_page_category()
        return ParserCatalog(html_page)

    def grab_all_items(self, pagination: range = None):
        if not pagination:
            page = self.get_page_category()
            parser = ParserCatalog(page)
            pagination = parser.pagination_list
        products = asyncio.run(self._create_tasks_grab_all_category_pages(pagination))
        # Преобразование списка  [[{}, {}, {}], [{}]] -> [{}, {}, {}, {}]
        return [d for sublist in products for d in sublist if d]

    async def _create_tasks_grab_all_category_pages(self, pagination):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for page in pagination:
                task = asyncio.create_task(self._get_products_in_page_category(session=session, page=page))
                tasks.append(task)
            return await asyncio.gather(*tasks)

    async def _get_products_in_page_category(self, session, page):
        url = URL(self._uri)
        url.update_query(page=page)
        if self._in_stock:
            url.update_query(in_stock=1)

        async with session.get(url=url.url, cookies=self._cookies, headers=settings.headers) as response:
            html_code = await response.text()
            parser_cat = ParserCatalog(html_code)
            return parser_cat.items

    def supplement_products(self, products_list: list[dict]):
        return asyncio.run(self._create_tasks_supplements(products_list=products_list))

    async def _create_tasks_supplements(self, products_list: list[dict]):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for product in products_list:
                task = asyncio.create_task(self._supplement_product_data(data_product=product, session=session))
                tasks.append(task)
            return await asyncio.gather(*tasks)

    async def _supplement_product_data(self, data_product, session=None):
        url = self._uri.root_url+data_product['url']
        async with session.get(url, cookies=self._cookies, headers=settings.headers) as response:
            html_page = await response.text()
            parser_product_page = ParserProduct(html_page)
            characteristics_table = parser_product_page.characteristics_table
            data_product['brand'] = characteristics_table["бренд"]
            return data_product

    def get_products_in_category(self):
        items = self.grab_all_items()
        items = self.supplement_products(items)
        return items


if __name__ == '__main__':
    """
    Получение данных от пользователя
    """
    uri = URL(input("Пример: https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?from=under_search\nВведите ссылку на категорию: "))
    shop_id = int(input("MetroSroreId можно найти в cookies на странице [online.metro-cc.ru]\nВведите metroStoreId: "))
    prefix = input("Введите префикс(он будет отображаться начале сохранённого файла): ")

    """
    Парсинг
    """
    scraper = MetroOnlineScraper(uri, 10)
    page_category = scraper.page_category
    products = scraper.get_products_in_category()

    """
    Путь сохранения файла и название
    """
    filename = f"{prefix}__{page_category.address}__{datetime.now().strftime('%d_%m_%Y__%H_%M')}.json"
    forbidden_characters = re.compile(r"[^\w\.\-_]")
    filename = forbidden_characters.sub("", filename)
    save_path = settings.SAVE_FOLDER / filename

    """
    Сохранение файла 
    """
    with open(save_path, "w") as f:
        json.dump(products, f)
