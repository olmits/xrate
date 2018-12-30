# TODO отрефакторить под rates_parser


from peewee import Model, SqliteDatabase, CharField, DoubleField, DateTimeField
from rates_parser import Parsing
from datetime import datetime


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
        return f"{self.updated.strftime('%Y-%m-%d')} - {self.source}: {self.cc} {self.ask}"


# XRate.drop_table()
XRate.create_table()


class Updating:

    def processing(self):





def update_rates(source, update_date=datetime.now()):

    source = Parsing(source, update_date)
    source.

    act_rate_info = func(update_date)  # Send API request and get records
    for cc, ask, bid, updated in act_rate_info:
        updated = updated.replace(hour=0, minute=0, second=0, microsecond=0)
        existing = XRate.select().where(  # Check if there're already this query
            XRate.source == func.__name__,  # by a source
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
                source=func.__name__,
                cc=cc,
                ask=ask,
                bid=bid,
                updated=updated
            )


if __name__ == '__main__':
    dat = datetime(2018, 12, 26)

    res = Parsing('nbu', dat)
    res.nbu_processing()
    update_rates(res.data, dat)

    # update_rates(mb, dat)
    r0 = XRate.select()
    r = r0.where(XRate.cc == 'USD').order_by(XRate.updated.asc())
    for each in r:
        print(each)

db.close()

