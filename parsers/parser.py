from bs4 import BeautifulSoup


class BaseParser:

    def __init__(self, html_page=None, bs_tag=None):
        if html_page and bs_tag:
            raise AttributeError(f"html_page & bs_tag is None!")
        self.soup = BeautifulSoup(html_page, 'lxml') if html_page else bs_tag


class ParserCatalog(BaseParser):
    def __init__(self, html_page=None):
        super().__init__(html_page=html_page)

    @property
    def address(self):
        return self.soup.find(class_="header-address__receive-address").text.strip()

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
    def characteristics_table(self) -> dict:
        table = self.soup.find(class_="product-attributes__list style--product-page-full-list").find_all(
            class_="product-attributes__list-item")
        table = [x.text.replace("\n", "").strip().split("   ") for x in table]
        table = [sublist[0:1] + sublist[-1:] for sublist in table]
        return {k.strip().lower(): v.strip() for (k, v) in table}



