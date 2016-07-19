#!/usr/bin/python

import time
import datetime
import logging

from engine.stock_chomp import StockChomper
from engine.static_storage import save, conditional_load, NoHistoryFileExcption, OutdatedHistoryExcption
from engine.support_class import LogMaster
from engine.numeric import partition, hashify, get_partiton_representative
from engine.spiral import draw_spiral, pretty_print_grid
from engine.symbolic import hash2symbol

from engine.cliparse import parsecli


class DivergenceViewer(LogMaster):

    def __init__(self, cli, loglevel=logging.DEBUG):
        self.setLogger(self.__class__.__name__, loglevel)
        self.cli = cli
        self.openings = []
        self.hashlist = []

    def chomp_finished(self, chomp):
        self.openings = chomp.results
        save(chomp.results)

    def fetching(self):
        reload = False
        loaded = []
        try:
            loaded = conditional_load()
            self.logger.debug("Loaded stock openings from disk")
        except NoHistoryFileExcption as e:
            self.logger.warning("No history file found in \"%s\"; re-downloading" % str(e))
            reload = True
        except OutdatedHistoryExcption as e:
            self.logger.warning("History file out of date (was %s); re-downloading" % str(e))
            reload = True
        if cli.force:
            self.logger.debug("Forcing re-download")
            reload = True

        if reload:
            self.logger.debug("Fetching stock openings from the net...")
            chomp = StockChomper(finishcback=self.chomp_finished, loglevel=self.loglevel)
            chomp.start()
            while not chomp.finished:
                time.sleep(1.0)
        else:
            self.openings = loaded

    def start(self):
        def symbolify(pair):
            if isinstance(pair, tuple):
                return hash2symbol(pair[1], nihon=not cli.roman)
            else:
                return "()"
        self.fetching()
        big, medium, small = partition(len(self.openings))
        self.hashlist = hashify(self.openings)
        todraw = get_partiton_representative(self.hashlist, (big, medium, small), sep=("", ""))
        symbols = ["()"] + list(map(symbolify, todraw))
        grid = draw_spiral(symbols)
        visual = pretty_print_grid(grid, datetime.date.today().isoformat(), self.hashlist[-1][1][:8])
        print(visual)


if __name__ == "__main__":
    cli = parsecli()
    loglevel = logging.INFO
    if cli.debug:
        loglevel = logging.DEBUG
    div = DivergenceViewer(cli, loglevel=loglevel)
    div.start()
