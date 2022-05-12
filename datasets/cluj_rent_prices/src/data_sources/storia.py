import re
import requests
from bs4 import BeautifulSoup


mappings = {
    'Suprafata construita': 'surface',
    'Numarul de camere': 'rooms',
    'Etaj': 'floor',
    'Numarul de bai': 'bathrooms',
    'Stare': 'state'
}

def extract_storia_apprtment_meta(url):
    meta = {}
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        meta_table = extract_meta_from_table(soup)
        meta_zone_aria = extract_zone_from_aria(soup)
        meta_zone_text = extract_zone_from_text(soup)
        meta = {**meta_table, **meta_zone_aria, **meta_zone_text}
    return meta

def extract_meta_from_table(soup: BeautifulSoup, na_placeholder='cere informatii') -> dict:
    meta = {key: None for key in mappings.values()}
    prez = soup.find('div', attrs={"data-testid":"ad.top-information.table"})
    if not prez:
        return meta
    for key, value in mappings.items():
        text = prez.find('div', attrs={"aria-label": key}).text
        text = text.replace(key, '').replace(na_placeholder, '')
        text = text.replace('m²', '')
        meta[value] = text
    return meta

def extract_zone_from_aria(soup: BeautifulSoup) -> dict:
    meta = {'zone_aria': None}
    rez = soup.find('a', attrs={"aria-label":"Abordare"})
    if not rez:
        return meta
    meta['zone_aria'] = rez.text.split(',')[-1].strip()
    return meta

def extract_zone_from_text(soup: BeautifulSoup) -> dict:
    meta = {'zone_text': None}
    rez = soup.find('div', attrs={"data-cy":"adPageAdDescription"})
    if not rez:
        return meta
    results = re.findall(r"(?<=\b(?i)\bzona\b\s).*?(?=[.,:!?\\-]|\\z)", rez.text)
    if len(results) == 0:
        return meta
    meta['zone_text'] = " ".join(re.findall(r"\b[A-Z][a-z]+", results[0]))
    return meta