import datetime
import logging
import requests
from bs4 import BeautifulSoup

from .support_class import LogMaster


class StockChomper(LogMaster):

    stock = "IBM"
    api_endpoint = "https://www.investopedia.com/markets/api/partial/historical/"
    api_date_req_format = "%b+%d%%2C+%Y"
    api_date_resp_format = "%b %d, %Y"

    def __init__(self, datefrom, loglevel=logging.DEBUG):
        self.setLogger(self.__class__.__name__, loglevel)
        self.datefrom = datefrom
        self.stock_cache = []

    def download(self):
        query_url = self.api_endpoint + "?Symbol=" + self.stock + \
                                        "&Type=Historical+Prices" + \
                                        "&Timeframe=Daily" + \
                                        "&StartDate=" + self.datefrom.strftime(self.api_date_req_format) + \
                                        "&EndDate=" + datetime.date.today().strftime(self.api_date_req_format)
        self.logger.debug("Downloading stock data from: %s" % query_url)
        rawhtml = requests.get(query_url).text
        self.logger.debug("Download complete, beginning parsing")
        soup = BeautifulSoup(rawhtml, "html.parser")
        data_items = soup.find_all("tr", attrs={"class": "in-the-money"})
        temp_results = []
        for dataitem in data_items:
            try:
                date_cell = dataitem.find("td", attrs={"class": "date"})
                open_cell = dataitem.find("td", attrs={"class": "num"})
                temp_results.append((
                    self.dayfy(datetime.datetime.strptime(date_cell.getText(), self.api_date_resp_format)),
                    float(open_cell.getText())
                ))
            except AttributeError:
                continue

        sorted_temp_results = sorted(temp_results, key=lambda pair: pair[0])  # sort by date
        self.stock_cache = list(map(
            lambda pair: (pair[0].isoformat(), "%.2f" % pair[1]),  # important: float value is rounded here
            sorted_temp_results))  # date() -> String
        self.logger.debug("Parsing complete")
        return self.stock_cache

    def dayfy(self, timestamp):
        return datetime.date(year=timestamp.year, month=timestamp.month, day=timestamp.day)

