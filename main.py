import asyncio
from copy import copy

import aiohttp
import requests
from bs4 import BeautifulSoup

from parsers.parser import ParserCatalog
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

    def grab_all_items(self, pagination: range):
        page = self.get_page_category()
        parser = ParserCatalog(page)
        pagination = parser.pagination_list
        products = asyncio.run(self._create_tasks_grab_all_category_pages(pagination))

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

        async with session.get(url=url.url, cookies=self.cookies, headers=settings.headers) as response:
            pass
            
            # soup = BeautifulSoup(await response.text(), "lxml")

            # products = soup.find_all('div', attrs={'data-sku': True})
            # i = 0
            # list_product = []
            # for product in products:
            #     product = ParserProductTag(product)
            #     actual_price, old_price = product.price
            #     i += 1
            #     obj_product = {
            #         'id': product.id,
            #         'title': product.title,
            #         'url': f"{url.root_url}" + product.link,
            #         'regular_price': old_price if old_price else actual_price,
            #         'promo_price': actual_price if old_price else None,
            #         'brand': None
            #     }
            #     list_product.append(obj_product)
            # logging.info(f"[INFO] - парсинг страницы - {page} (собрано {i} товаров)")
            # return list_product



if __name__ == '__main__':
    uri = URL(r"https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?from=under_search")
    x = MetroOnlineScraper(uri, 15)
    x.get_page_category()

