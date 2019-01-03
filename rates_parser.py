import requests
from datetime import datetime, date
from itertools import groupby
from xml.etree import ElementTree
from rates_app import log

currencies = ('USD', 'EUR', 'RUB')


class Parsing:

    api = {'nbu': "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange",  # NBU rate
           'minfin_mb': "http://api.minfin.com.ua/mb/6c913d55a2d11ac117dee65ac1c8ae538380eee6/",  # MB rate
           'minfin_av': "http://api.minfin.com.ua/summary/6c913d55a2d11ac117dee65ac1c8ae538380eee6/"
           # Average rate in banks
           }

    def __init__(self, source, update_date):
        self.source = source
        self.update_date = update_date
        self.data = []  # Creae empty list for each API response

    @classmethod
    def sending_request(cls, update_date, source):
        try:
            if update_date and source == 'nbu':  # Send request on NBU API
                return requests.get(cls.api[source], params={'date': update_date.strftime('%Y%m%d')})
            elif update_date and source != 'nbu':  # Send request to Minfin API to receive average or MB rates
                return requests.get(cls.api[source] + update_date.strftime('%Y-%m-%d'))
            else:  # Send a standard request without date specification
                return requests.get(cls.api[source])
        except requests.exceptions.RequestException as problem:
            log.debug(f'{source} API request error: {problem}')
            return None

    @staticmethod
    def status_code_checker(response, source):  # Verify response code
        if not response.status_code == requests.codes.ok:
            log.debug(f'{source} API invalid response: {response.status_code}')
            return False

    def processing(self):
        if self.source == "nbu":
            return self.nbu_processing()
        elif self.source == "minfin_mb":
            return self.minfin_mb_processing()
        elif self.source == "minfin_av":
            return self.minfin_av_processing()

    def nbu_processing(self):
        response = Parsing.sending_request(self.update_date, self.source)
        if not self.status_code_checker(response, self.source) is False:
            tree = ElementTree.fromstring(response.content)
            for leaf in tree:
                if leaf.find('cc').text in currencies:
                    self.data.append((leaf.find('cc').text, leaf.find('rate').text, leaf.find('rate').text,
                                      self.update_date))

    def minfin_mb_processing(self):
        response = Parsing.sending_request(self.update_date, self.source)
        if not self.status_code_checker(response, self.source) is False:
            response = response.json()
            raw_result = [(query['currency'].upper(), query['ask'], query['bid'],
                           datetime.strptime(query['pointDate'], '%Y-%m-%d %H:%M:%S'))
                          for query in response
                          if query['currency'].upper() in currencies]
            raw_result.sort(key=lambda tup: tup[0])
            for key, group in groupby(raw_result, key=lambda t: t[0]):
                items = list(group)
                self.data.append(sorted(items, key=lambda t: t[3], reverse=True)[0])

    def minfin_av_processing(self):
        response = Parsing.sending_request(self.update_date, self.source)
        if not self.status_code_checker(response, self.source) is False:
            response = response.json()
            for key, value in response.items():
                if key.upper() in currencies:
                    self.data.append((key.upper(), value['ask'], value['bid'], self.update_date))

