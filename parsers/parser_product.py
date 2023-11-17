from parsers.base_parser import BaseParser


class ParserProduct(BaseParser):

    def __init__(self, html_page=None):
        super().__init__(html_page=html_page)

    @property
    def characteristics_table(self) -> dict:
        """
        Таблица Характеристики
        :return: Возвращает таблицу Характеристики из страницы продукта где ключом является его имя с маленькой буквы
        """
        table = self.soup.find(class_="product-attributes__list style--product-page-full-list").find_all(
            class_="product-attributes__list-item")
        table = [x.text.replace("\n", "").strip().split("   ") for x in table]
        table = [sublist[0:1] + sublist[-1:] for sublist in table]
        return {k.strip().lower(): v.strip() for (k, v) in table}
