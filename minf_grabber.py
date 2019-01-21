import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like '
                  'Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

black_urls = {
    'USD': 'https://minfin.com.ua/currency/auction/usd/buy/kiev/',
    'EUR': 'https://minfin.com.ua/currency/auction/eur/buy/kiev/',
    'RUB': 'https://minfin.com.ua/currency/auction/rub/buy/kiev/'
}


def minfin_blck_mrck():

    result = []

    for currency in black_urls.keys():
        scrap_scrap = requests.get(black_urls[currency], headers=headers)
        more_scraping = BeautifulSoup(scrap_scrap.text.encode('utf-8'), features="html.parser")
        filings_pile = more_scraping.find_all('div', {'class': "au-mid-buysell"})

        ask_bid = {}
        for raw_data in filings_pile:
            grabbibg_rate = re.findall("(?<=\n)[0-9,]{5}", raw_data.text)
            if not grabbibg_rate:
                continue
            grabbibg_ops = re.findall('(?<=\n)Средняя \w+', raw_data.text)
            ask_bid[grabbibg_ops[0]] = float(grabbibg_rate[0].replace(',', '.'))

        result.append((
                currency,
                ask_bid['Средняя продажа'],
                ask_bid['Средняя покупка'],
                datetime.now()
            ))
    return result


if __name__ == '__main__':
    oppsp = minfin_blck_mrck()
    print(minfin_blck_mrck.__name__)
    for k in oppsp:
        print(k)

