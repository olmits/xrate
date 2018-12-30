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
        return f"{self.updated} - {self.source}: {self.cc} {self.ask}"


# XRate.drop_table()
XRate.create_table()


def update_rates(api_source, update_date=datetime.now()):

    parsed = Parsing(api_source, update_date)
    parsed.processing()
    # act_rate_info = func(update_date)
    for cc, ask, bid, updated in parsed.data:
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


db.close()

