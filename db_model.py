from peewee import Model, SqliteDatabase, CharField, DoubleField, DateTimeField
from rates_parser import Parsing
from minf_grabber import minfin_blck_mrck
from datetime import datetime, date


db = SqliteDatabase("rates.db")


class XRate(Model):
    class Meta:
        database = db
        db_table = "rates"
    source = CharField()
    cc = CharField()
    ask = DoubleField()
    bid = DoubleField()
    updated = DateTimeField()

    def __str__(self):
        return f"{self.updated} - {self.source}: {self.cc} Ask (продажа): {self.ask} Bid (покупка): {self.bid}"


# XRate.drop_table()
XRate.create_table()


def get_rates():  # TODO add grabber rates processing
    pass 


def update_rates(api_source, update_date=datetime.now()):

    def get_rates(api_source):
        if api_source in Parsing.api.keys():
            parsed = Parsing(api_source, update_date)
            parsed.processing()
            return parsed.data
        elif api_source == minfin_blck_mrck.__name__:
            return minfin_blck_mrck()

    for cc, ask, bid, updated in get_rates(api_source):
        updated = updated.replace(hour=0, minute=0, second=0, microsecond=0)
        existing = XRate.select().where(  # Check if there're already this query
            XRate.source == api_source,  # by a source
            XRate.cc == cc,  # by a currency
            XRate.updated == updated  # and by a date
        )
        if existing.exists():  # If it exists
            existing = existing.first()  # get this query and
            existing.ask = float(ask)  # update ask rate
            existing.bid = float(bid)  # and bid rate
            existing.save()
        else:
            XRate.create(  # If not, create new query
                source=api_source,
                cc=cc,
                ask=ask,
                bid=bid,
                updated=updated
            )


if __name__ == '__main__':

    dat = datetime(2019, 1, 13)
    # for each in Parsing.api.keys():
    #     update_rates(each, dat)

    for each in XRate.select().where(XRate.cc == 'USD', XRate.updated == dat).order_by(XRate.updated.desc()):
        print(each)

    distinct_list = XRate.select(XRate.source).distinct()
    for each in distinct_list:
        print(each.source)


db.close()

