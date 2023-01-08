import ssl
import requests

from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
from bs4 import BeautifulSoup

CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256
             -SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA """
url = 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty-ASgBAgICAkTGB~pm7gmmZw?cd=1&q=rtx+3070&s=104 '


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
r = session.request('GET', url).text

soup = BeautifulSoup(r, 'lxml')


def get_last_ad(page: BeautifulSoup):
    return page.find('div', attrs={'data-marker': 'item'})


def get_values(ad: BeautifulSoup):
    header = ad.find('h3', attrs={'itemprop': 'name'}).text
    price = ad.find('meta', attrs={'itemprop': 'price'})['content']  # доступ к содержимому атрибута
    link = f"https://www.avito.ru{ad.find('a')['href']}"
    picture = ad.find('img', attrs={'itemprop': 'image'})['src']
    return {"header": header, "price": price, "link": link, "image": picture}


get_values(get_last_ad(soup))
