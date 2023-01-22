import ssl
import requests

from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
from bs4 import BeautifulSoup


CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256
             -SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA """


class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)


session = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
session.mount("https://", adapter)


def extract_name_from_url(link):
    return link[(link.find('&q') + 3):link.find('&s')].replace('+', ' ')


def get_last_ad(url, limit=1):
    r = session.request('GET', url, headers={'Referer': 'https://www.avito.ru'}).text
    # реквест работает только при такой записи, разбираться не пробовал
    soup = BeautifulSoup(r, 'lxml')
    match limit:
        case 1:
            return soup.find('div', attrs={'data-marker': 'item'})
        case 0:
            return soup.find_all('div', attrs={'data-marker': 'item'})


def get_ad_values(ad: BeautifulSoup):  # возвращает словарь со значениями
    header = ad.find('h3', attrs={'itemprop': 'name'}).text
    price = ad.find('meta', attrs={'itemprop': 'price'})['content']  # доступ к содержимому атрибута
    url = f"https://www.avito.ru{ad.find('a')['href']}"
    picture = ad.find('img', attrs={'itemprop': 'image'})['src']
    return {"header": header, "price": int(price), "link": url, "image": picture}

