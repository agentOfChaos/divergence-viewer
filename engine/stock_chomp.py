from pandas_datareader.data import DataReader
import datetime
import logging

from engine.support_class import LogMaster


class StockChomper(LogMaster):

    stock = "IBM"
    stat = "Open"
    source = "yahoo"

    datefrom = datetime.date(year=1960, month=1, day=1)

    def __init__(self, loglevel=logging.DEBUG, workers=4, finishcback=None):
        self.setLogger(self.__class__.__name__, loglevel)
        self.finishcback = finishcback
        self.results = []
        self.finished = False

    def start(self):
        def dayfy(timestamp):
            return datetime.date(year=timestamp.year, month=timestamp.month, day=timestamp.day)
        now = datetime.date.today()
        ibm = DataReader(self.stock, self.source, self.datefrom, now)
        params = ibm.to_dict()
        openings = params[self.stat]
        temp_results = map(lambda k: (dayfy(k), openings[k]), openings.keys())
        sorted_temp_results = sorted(temp_results, key=lambda pair: pair[0])
        self.results = list(map(lambda pair: (pair[0].isoformat(), pair[1]), sorted_temp_results))
        self.finished = True
        if self.finishcback is not None:
            self.finishcback(self)

