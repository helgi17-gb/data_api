import os
import json
import requests
from time import sleep


class parse5ka:
    params = {
        'records_per_page': 100,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0",
    }
    def __init__(self, start_url, category_file):
        self.start_url = start_url
        self.category_file = category_file

    def parse(self):
        url = self.start_url
        params = self.params
        category = {}
        with open(self.category_file, "r") as cat_file:
            category = json.load(cat_file)
            print(category)

            params["categories"] = category['parent_group_code']

        category["products"] = []
        while url:
            response: requests.Response = requests.get(url, params=params,
                                                 headers = self.headers)
            data = response.json()
            if not data:
                sleep(.01)
                continue

            print(f'data {data}')
            url = data.get("next")
            if params:
                params = {}
#            for product in data.get('results', []):
#                print(f'product {product["id"]}')

            category["products"].extend(data.get('results', []))

        self.save_products(category)

    def save_products(self, product):
        with open(f'{self.category_file}', 'w', encoding='UTF-8') as file:
        #file.write(json.dumps(product))
            json.dump(product, file, ensure_ascii=False)

class parse5ka_category(parse5ka):
    def __init__(self, start_url, path):
        self.start_url = start_url
        self.path = path

    def parse(self):
        url = self.start_url
        params = self.params
        while url:
            response: requests.Response = requests.get(url, params=params,
                                               headers=self.headers)
            data = response.json()
            if not data:
                sleep(0.01)
                continue

            url = '' #data.get("next")
            if params:
                params = {}
            for category in data:
                self.save_category(category)
                print(f'product {category["parent_group_code"]}')

    def save_category(self, category):
        with open(f"{self.path}/category_{category['parent_group_code']}.json", "w") as group_file:
            json.dump(category, group_file, ensure_ascii=False)

if __name__ == '__main__':

    url = "https://5ka.ru/api/v2/special_offers/"
    url_cats = "https://5ka.ru/api/v2/categories/"
    path = 'products_by_category'

    parser = parse5ka_category(url_cats, path)
    parser.parse();

    for category_file in os.listdir(path+'/'):
        print(category_file+" processing ...")
        parser = parse5ka(url, path+"/"+category_file)
        parser.parse();
