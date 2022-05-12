import requests
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter


def get_olx_offers(url):
    offers = None
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        offers_table = soup.find('table', class_='fixed offers breakword redesigned')
        offers = offers_table.find_all('tr', class_='wrap')
    return offers

def extract_offer_link(offer_html):
    return offer_html.a.attrs['href']

def convert_currency(value:int, currency:str, new_currency='EUR'):
    c = CurrencyConverter()
    new_value = value
    if currency != 'EUR':
        new_value = int(c.convert(value, currency, new_currency))
    return new_value, new_currency

def extract_offer_meta(offer_html):
    meta = {}
    if 'data-features' in offer_html.attrs:
        txt_dict = offer_html.attrs['data-features']
        txt_dict = txt_dict.replace('true', 'True').replace('false', 'False')
        meta = eval(txt_dict)

        value, currency = convert_currency(meta['ad_price'], meta['price_currency'])
        meta['ad_price'], meta['price_currency'] = value, currency
    return meta