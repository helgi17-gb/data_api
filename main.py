import requests
import bs4
from urllib.parse import urljoin, urlparse
import pymongo as pm



class MagnitParser:
    def __ini__(self, start_url):
        self.start_url = start_url
        mongo_client = pm.MongoClient('mongodb://localhost:27017')
        self.db = mongo_client['parse_11']

    def _get(self, url:str) -> bs4.BeautifulSoup:
        #todo обработка статусов и повторные запросы
        response = requests.get(url)
        return bs4.BeautifulSoup(response.text, "lxml")

    def run(self):
        soup = self._get(self.start_url)
        for product in self.parse(soup):
            self.save(product)

    def parse(self, soup:bs4.BeautifulSoup) -> dict:
        catalog = soup.find('div', attrs={'class': 'сatalogue__main'})

        for product in catalog.findChildren('a'):
            try:
                pr_data = {
                    'url': urljoin(self.start_url, product.attrs.get('href')),
                    'image': urljoin(self.start_url,
                                     product.find('img').attrs.get('data-src')),
                    'name': product.find('div', attrs={'class': 'cartd-sale__title'}).find('p').text
                }
                yield pr_data
            except AttributeError:
                continue

    def save(self, data:dict):
        collection = self.db['magnit']
        collection.save

        pass

url = "https://magnit.ru/promo/?geo=moskva"

response = requests.get(url)
url_p = urlparse(response.url)

#with open("magnit.html", "w", encoding='UTF-8') as file:
#    file.write(response.text)

soup = bs4.BeautifulSoup(response.text, "lxml")

if __name__ == '__main__':
    parser = MagnitParser("https://magnit.ru/promo/?geo=moskva")
    parser.run()

