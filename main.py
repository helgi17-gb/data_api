import dotenv
import requests
import bs4
from product import Product
from dbclient import MongoDbClient
import time

dotenv.load_dotenv('.env')


class RequestException(Exception):
    pass


class MagnitParser:
    def __init__(self, start_url):
        self.start_url = start_url
        self.db_client = MongoDbClient("parse_magnit", "magnit")

    def _get(self, url:str) -> bs4.BeautifulSoup:
        while True:
            try:
                response = requests.get(url)
                if response.status_code != requests.codes.ok:
                    raise RequestException
                time.sleep(0.1)
                return bs4.BeautifulSoup(response.text, "lxml")
            except RequestException:
                time.sleep(0.25)

    def run(self):
        soup = self._get(self.start_url)
        for product in self.parse(soup):
            self.save(product)

    def parse(self, soup:bs4.BeautifulSoup) -> dict:
        catalog = soup.find('div', attrs={'class': 'сatalogue__main'})

        for product in catalog.findChildren('a'):
            try:
                prod = Product(self.start_url, product)
                yield prod.get_data()
            except AttributeError:
                continue

    def save(self, data:dict):
        self.db_client.insert(data)

if __name__ == '__main__':
    parser = MagnitParser("https://magnit.ru/promo/?geo=moskva")
    parser.run()

