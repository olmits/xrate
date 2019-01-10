from collections import namedtuple
from datetime import datetime
from rates_parser import Parsing
from db_model import XRate, update_rates


def update_bd():
    actual_date = datetime.now()
    for each in Parsing.api.keys():
        update_rates(each, actual_date)


def get_last_updated_cc(source, cc):
    last_updated_date = XRate.select().where(XRate.source == source).order_by(XRate.updated.desc()).first().updated
    last_updated_cc = XRate.select().where(
        XRate.source == source,
        XRate.updated == last_updated_date,
        XRate.cc == cc
    )
    return last_updated_cc


def get_all_last_updated_cc(cc='USD'):
    records = []
    for an_api in Parsing.api.keys():
        for each in get_last_updated_cc(an_api, cc):
            records.append(each)
    return records


def filter_r(args):
    cc = args.get("cc")
    records = get_all_last_updated_cc(cc)
    return records


def create_tup(func):  # Create the list of namedtuple from the given function.
    # Each tuple consists of source, currency, ask and bid rates.
    query = namedtuple('query', ['source', 'cc', 'ask', 'bid'])
    tubs = [
        query(
            rate.source,
            rate.cc,
            round(float(rate.ask), 2),
            round(float(rate.bid), 2))
        for rate in func
    ]
    return tubs

