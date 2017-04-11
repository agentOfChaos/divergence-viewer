from pandas_datareader.data import DataReader
import datetime
import logging

from .support_class import LogMaster


class StockChomper(LogMaster):

    stock = "IBM"
    stat = "Open"
    source = "yahoo"

    datefrom = datetime.date(year=1962, month=1, day=2)

    def __init__(self, loglevel=logging.DEBUG):
        self.setLogger(self.__class__.__name__, loglevel)
        self.stock_cache = []

    def download(self):
        now = datetime.date.today()
        ibm = DataReader(self.stock, self.source, self.datefrom, now)
        params = ibm.to_dict()
        openings = params[self.stat]
        temp_results = map(lambda k: (self.dayfy(k), openings[k]), openings.keys())  # unsorted pairs (date(), float)
        sorted_temp_results = sorted(temp_results, key=lambda pair: pair[0])  # sort by date
        self.stock_cache = list(map(
            lambda pair: (pair[0].isoformat(), "%.2f" % pair[1]),  # important: float value is rounded here
            sorted_temp_results))  # date() -> String
        return self.stock_cache

    def dayfy(self, timestamp):
        return datetime.date(year=timestamp.year, month=timestamp.month, day=timestamp.day)

