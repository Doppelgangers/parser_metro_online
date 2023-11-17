import re
from parsers.base_parser import BaseParser


class ParserCatalog(BaseParser):

    class ParserProductTag(BaseParser):

        def __init__(self, bs_tag=None):
            super().__init__(bs_tag=bs_tag)

        @property
        def id(self) -> int:
            return int(self.soup['data-sku'])

        @property
        def title(self) -> str:
            return self.soup.find(class_='product-card-name__text').text.strip()

        @property
        def price(self) -> tuple[float | None, float | None]:
            prices_actual = self.soup.find(class_="product-unit-prices__actual-wrapper")
            prices_old = self.soup.find(class_="product-unit-prices__old-wrapper")
            actual = self.validate_price(prices_actual)
            old = self.validate_price(prices_old)
            return actual, old

        @staticmethod
        def validate_price(tag) -> float | None:
            try:
                rub = tag.find(class_="product-price__sum-rubles").text
                rub = re.sub(r"[^\d\.]", '', rub)
                penny = tag.find(class_="product-price__sum-penny")
                penny = penny.text if penny else ""
                return float(f"{rub}{penny}")
            except (ValueError, AttributeError) as e:
                return None


        @property
        def link(self) -> str:
            return self.soup.find(class_="product-card-photo__link").get("href")

    def __init__(self, html_page=None):
        super().__init__(html_page=html_page)

    @property
    def address(self):
        return self.soup.find(class_="header-address__receive-address").text.strip()

    @property
    def title(self):
        return self.soup.find(class_="subcategory-or-type__heading-title").text

    @property
    def pagination_list(self) -> range:
        try:
            items_pagination = self.soup.select("ul.catalog-paginate.v-pagination")[0].findAll('li')
            items_pagination = map(lambda x: x.text, items_pagination)
            items_pagination = [int(x) for x in items_pagination if x.isdigit()]
            return range(min(items_pagination), max(items_pagination) + 1)
        except IndexError:
            return range(1, 2)

    @property
    def items(self):
        products = self.soup.find_all('div', attrs={'data-sku': True})

        list_product = []

        for product in products:
            product = self.ParserProductTag(product)
            actual_price, old_price = product.price
            obj_product = {
                'id': product.id,
                'title': product.title,
                'url': product.link,
                'regular_price': old_price if old_price else actual_price,
                'promo_price': actual_price if old_price else None,
            }
            list_product.append(obj_product)
        return list_product
