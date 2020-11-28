import datetime
from urllib.parse import urljoin, urlparse


class Product:
    def __init__(self, start_url, product):
        self.month_dict = {
            'янв': '01',
            'фев': '02',
            'мар': '03',
            'апр': '04',
            'май': '05',
            'мая': '05',
            'июн': '06',
            'июл': '07',
            'авг': '08',
            'сен': '09',
            'окт': '10',
            'ноя': '11',
            'дек': '12',
        }
        self.start_url = start_url
        self.product = product
        self.url = self._get_url()
        self.promo_name = self._get_promo_name()
        self.product_name = self._get_product_name()
        self.image_url = self._get_image_url()
        self.old_price = self._get_old_price()
        self.new_price = self._get_new_price()
        (self.date_from, self.date_to) = self._get_date_from_to()

    def get_data(self):
        pr_data = {
            'url': self.url,
            'promo_name': self.promo_name,
            'product_name': self.product_name,
            'old_price': self.old_price,
            'new_price': self.new_price,
            'image_url': self.image_url,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return pr_data

    def _get_url(self):
        return urljoin(self.start_url, self.product.attrs.get('href'))

    def _get_promo_name(self):
        return self.product.find(
            'div',
            attrs={'class': 'card-sale__header'}).find('p').text

    def _get_product_name(self):
        return self.product.find(
            'div',
            attrs={'class': 'card-sale__title'}).find('p').text

    def _get_old_price(self):
        [int_old_price, dec_old_price] = \
            self.product.find(
                'div',
                attrs={'class': 'label__price_old'}). \
                findChildren('span')
        return float(int_old_price.text + "." + dec_old_price.text)

    def _get_new_price(self):
        [int_new_price, dec_new_price] = \
            self.product.find(
                'div',
                attrs={'class': 'label__price_new'}). \
                findChildren('span')
        return float(int_new_price.text + "." + dec_new_price.text)

    def _get_image_url(self):
        return urljoin(self.start_url,
                       self.product.find('img').attrs.get('data-src'))

    def _get_date_from_to(self):
        [from_date_str, to_date_str] = self.product.find(
            'div',
            attrs={'class': 'card-sale__date'}).findChildren('p')
        from_date = from_date_str.text.split()[1:]
        to_date = to_date_str.text.split()[1:]
        year = str(datetime.date.today().year)
        date_from = datetime.datetime.strptime(
            year + '-' +
            self.month_dict[from_date[1][:3]] + '-' + from_date[0],
            "%Y-%m-%d")
        date_to = datetime.datetime.strptime(
            year + '-' +
            self.month_dict[to_date[1][:3]] + '-' + to_date[0] +
            " 23:59:59",
            "%Y-%m-%d %H:%M:%S")
        return (date_from, date_to)
