import datetime
import logging
import requests
import csv
from io import StringIO

from .support_class import LogMaster
from .numeric import custom_round


class StockChomper(LogMaster):

    stock = "IBM"
    api_endpoint = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%d&period2=%d&interval=1d&events=history&crumb=%s"
    crumb = "iKh0KK.2Lmu"
    cookies = {"B": "0gp97shec33u5&b=3&s=4f"}
    useragent = "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"

    def __init__(self, datefrom, loglevel=logging.DEBUG):
        self.setLogger(self.__class__.__name__, loglevel)
        self.datefrom = datefrom
        self.stock_cache = []

    @staticmethod
    def validate_row(row):
        return row[1] != "null"

    def download(self):
        query_url = self.api_endpoint % (self.stock, 
                                         self.convert_time_period(self.datefrom), 
                                         self.convert_time_period(datetime.date.today()), 
                                         self.crumb)
        self.logger.debug("Downloading stock data from: %s" % query_url)
        fp = StringIO(requests.get(query_url, cookies=self.cookies, headers={"User-Agent": self.useragent}).text)
        self.logger.debug("Download complete, beginning parsing")
        
        reader = csv.reader(fp, delimiter=",")
        next(reader, None)
        
        temp_results = []
        for row in reader:
            temp_results.append((
                datetime.datetime.strptime(row[0], "%Y-%m-%d"),
                row[1]
                ))
        
        sorted_temp_results = sorted(temp_results, key=lambda pair: pair[0])  # sort by date
        self.stock_cache = list(map(
            lambda pair: (pair[0].isoformat(), custom_round(pair[1], 2)),  # important: float value is rounded here
            filter(lambda pair: self.validate_row(pair),
                   sorted_temp_results)))  # date() -> String
        self.logger.debug("Parsing complete")
        return self.stock_cache

    def convert_time_period(self, dateobj):
        delta = dateobj - datetime.date(1970, 1, 1)
        return delta.days*60*60*24

