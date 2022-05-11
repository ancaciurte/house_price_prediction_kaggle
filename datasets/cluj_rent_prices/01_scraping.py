from datetime import datetime
from pathlib import Path

import requests
import pandas as pd
from tqdm import tqdm

from src.data_sources.olx import get_olx_offers, extract_offer_meta, extract_offer_link
from src.data_sources.storia import extract_storia_apprtment_meta

def will_redirect(url):
    r = requests.get(url)
    return r.url != url

if __name__ == '__main__':
    base_url = 'https://www.olx.ro/imobiliare/apartamente-garsoniere-de-inchiriat'
    city = 'cluj-napoca'
    out_dir = Path('data/raw')
    max_pages = 1
    
    ''' TODOs
        * save offer posting date
        * implement multithreading
        * add support for non-storia posts
    '''
    out_dir.mkdir(exist_ok=True)

    parsed_offers = []
    for page_idx in range(max_pages):
        offers_url = f'{base_url}/{city}/?page={page_idx+1}'
        if will_redirect(offers_url) and page_idx > 0:
            break

        offers = get_olx_offers(offers_url)
        for offer in tqdm(offers):
            meta = extract_offer_meta(offer)
            if meta.get('partner_code', False) and meta['partner_code'] != 'storia':
                continue
            offer_link = extract_offer_link(offer)
            storia_meta = extract_storia_apprtment_meta(offer_link)
            meta = {**meta, **storia_meta}
            parsed_offers.append(meta)
        df = pd.DataFrame(parsed_offers)
        date = str(datetime.today().date())
        df.to_csv(out_dir/f'offers_{city}_{date}.csv', index=False)