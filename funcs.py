from collections import namedtuple
from db_model import XRate


def get_r():
    last_updated = XRate.select().order_by(XRate.updated.desc()).first().updated  # Get the last updated date.
    records = XRate.select().where(XRate.updated == last_updated)  # Get actual rates records.
    return records


def filter_r(args):
    cc = args.getlist("cc")
    records = get_r().where(XRate.cc == cc)
    return records


def create_tup(func):  # Create the list of namedtuple from the given function.
    # Each tuple consists of source, currency, ask and bid rates.
    query = namedtuple('query', ['source', 'cc', 'ask', 'bid'])
    tubs = [
        query(
            rate.source,
            rate.cc,
            round(float(rate.ask), 3),
            round(float(rate.bid), 3))
        for rate in func
    ]
    return tubs


