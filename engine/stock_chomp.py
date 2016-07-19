from yahoo_finance import Share
from threading import Thread, Semaphore
from queue import Queue
import logging
import datetime
from functools import reduce

from engine.support_class import LogMaster


class StockChomper(LogMaster):

    stock = "IBM"
    stat = "Open"

    datefrom = datetime.date(year=1971, month=1, day=1)

    def __init__(self, loglevel=logging.DEBUG, workers=4, finishcback=None):
        self.setLogger(self.__class__.__name__, loglevel)
        self.semaphore = Semaphore(workers)
        self.temp_result_q = Queue()
        self.temp_results_list = []
        self.results = []
        self.finishcback = finishcback
        self.share = Share(self.stock)
        self.finished = False

    def generate_intervals(self):
        def formatdate(date):
            return date.isoformat()
        now = datetime.date.today()
        current_low = self.datefrom
        current_high = datetime.date(year=current_low.year+1, month=1, day=1)
        while current_high.year < now.year:
            now = datetime.date.today()
            val = (formatdate(current_low), formatdate(current_high))
            current_low = current_high
            current_high = datetime.date(year=current_low.year+1, month=1, day=1)
            yield val
        yield (formatdate(current_high), formatdate(now))
        return

    def fetch_worker(self, index, timecoord):
        self.logger.debug("Querying data for range %s..." % str(timecoord))
        hist_data = self.share.get_historical(*timecoord)
        self.temp_result_q.put((index, hist_data))
        self.semaphore.release()
        self.logger.debug("Aquired data for range %s!" % str(timecoord))

    def spawn_job(self, index, timecoord):
        t = Thread(target=self.fetch_worker, args=(index, timecoord))
        t.daemon = True
        t.start()

    def fetch_data(self):
        incr = 0
        for interval in self.generate_intervals():
            self.semaphore.acquire()
            self.spawn_job(incr, interval)
            incr += 1
        self.temp_result_q.put(None)

    def gather_received(self):
        while True:
            pair = self.temp_result_q.get()
            if pair is None:
                break
            npair = (pair[0], list(reversed(pair[1])))
            self.temp_results_list.append(npair)
            self.temp_results_list = sorted(self.temp_results_list, key=lambda pp: pp[0])  # sort by index
        self.results = reduce(lambda acc, item: acc + item[1], self.temp_results_list, [])  # discard indexes and concat
        self.results = list(map(lambda d: (d["Date"], d[self.stat]), self.results))
        self.finished = True
        if self.finishcback is not None:
            self.finishcback(self)

    def start(self):
        ft = Thread(target=self.fetch_data)
        gt = Thread(target=self.gather_received)
        ft.daemon = True
        gt.daemon = True
        ft.start()
        gt.start()
