from pandas_datareader.data import DataReader
import datetime
import logging
from threading import Thread, Lock

from engine.support_class import LogMaster


class ChomperInterface(LogMaster):

    """
    To allow for various backends, the ChomperInterface must be implemented:
    1) the data acquisition is initiated by callind the start() method
    1.1) calling start() is non-blocking
    2) the data will be available only after finished is set to True
    3) if specified, finishcback il called passing the chomper object as parameter
    4) results is built as an array of tuples ("iso date string", "floating point value")
    """

    def __init__(self, loglevel=logging.DEBUG, finishcback=None):
        self.setLogger(self.__class__.__name__, loglevel)
        self.finishcback = finishcback
        self.results = []
        self.finished = False

    def start(self):
        self.finished = True
        if self.finishcback is not None:
            self.finishcback(self)


class StockChomper(ChomperInterface):

    stock = "IBM"
    stat = "Open"
    source = "yahoo"

    datefrom = datetime.date(year=1962, month=1, day=2)

    def __init__(self, loglevel=logging.DEBUG, finishcback=None):
        super().__init__(loglevel, finishcback)
        self.working = Lock()

    def _worker(self):
        def dayfy(timestamp):
            return datetime.date(year=timestamp.year, month=timestamp.month, day=timestamp.day)

        now = datetime.date.today()
        ibm = DataReader(self.stock, self.source, self.datefrom, now)
        params = ibm.to_dict()
        openings = params[self.stat]
        temp_results = map(lambda k: (dayfy(k), openings[k]), openings.keys())  # unsorted pairs (date(), float)
        sorted_temp_results = sorted(temp_results, key=lambda pair: pair[0])  # sort by date
        self.results = list(map(lambda pair: (pair[0].isoformat(), pair[1]), sorted_temp_results))  # date() -> String
        super().start()
        self.working.release()

    def start(self):
        self.working.acquire()
        t = Thread(target=self._worker)
        t.daemon = True
        t.start()
