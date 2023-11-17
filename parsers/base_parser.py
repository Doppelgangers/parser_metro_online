from bs4 import BeautifulSoup


class BaseParser:

    def __init__(self, html_page=None, bs_tag=None):
        if html_page and bs_tag:
            raise AttributeError(f"html_page & bs_tag is None!")
        self.soup = BeautifulSoup(html_page, 'lxml') if html_page else bs_tag