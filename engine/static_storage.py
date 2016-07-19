import pickle
import os
import datetime

save_location = "stock_history.dat"


class OutdatedHistoryExcption(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NoHistoryFileExcption(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def save(datalist):
    now = datetime.date.today()
    with open(save_location, "wb") as file:
        pickle.dump((now, datalist), file)


def load():
    if os.path.isfile(save_location):
        with open(save_location, "rb") as file:
            (date, datalist) = pickle.load(file)
            return datalist
    raise NoHistoryFileExcption(save_location)


def conditional_load():
    if os.path.isfile(save_location):
        with open(save_location, "rb") as file:
            (date, datalist) = pickle.load(file)
            if date < datetime.date.today():
                raise OutdatedHistoryExcption(date.isoformat())
            return datalist
    raise NoHistoryFileExcption(save_location)
