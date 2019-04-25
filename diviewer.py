#!/bin/python

import logging
import datetime

if __name__ == "__main__":
    from engine.support_class import LogMaster
    from engine.stock_chomp import StockChomper
    from engine.cliparse import parsecli
    from engine import numeric, symbolic
    from engine.spiral import draw_spiral, pretty_print_grid
    from engine.img_gen import string_to_png
else:
    from .engine.support_class import LogMaster
    from .engine.stock_chomp import StockChomper
    from .engine.cliparse import parsecli
    from .engine import numeric, symbolic
    from .engine.spiral import draw_spiral, pretty_print_grid
    from .engine.img_gen import string_to_png


class DivergenceViewer(LogMaster):

    def __init__(self, cli, loglevel=logging.DEBUG):
        self.setLogger(self.__class__.__name__, loglevel)
        self.cliparams = cli

        self.datefrom = datetime.datetime.strptime(cli.beginning, "%Y-%m-%d").date()
        self.stocksource = StockChomper(datefrom=self.datefrom, 
                                        loglevel=loglevel)
        self.hashlist = []
        self.symbolist = []

    @property
    def stockdata(self):
        return self.stocksource.stock_cache

    def load_stock_data(self):
        self.logger.debug("Loading stock data")

        self.stocksource.download()

        for datum in self.stockdata:
            self.logger.debug(str(datum))

    def hash_to_symbol(self, digest):
        return symbolic.hash2symbol(digest, nihon=not self.cliparams.roman, color=self.cliparams.color)

    def extend_symbol_list(self, symbolist, hashlist):
        symbolist.append(symbolic.separator)
        symbolist.extend(list(map(self.hash_to_symbol, hashlist)))

    def partitionize(self):
        self.logger.debug("Building hash-chain")

        self.hashlist = numeric.hashchain(self.stockdata)

        for digest in self.hashlist:
            self.logger.debug(digest)

        self.logger.debug("Partitioning")

        big_part, medium_part, small_part = numeric.partition(len(self.stockdata))

        self.logger.debug("(big/medium/small): (%d / %d / %d)" % (len(big_part), len(medium_part), len(small_part)))

        self.symbolist = []
        self.extend_symbol_list(self.symbolist, map(lambda index: self.hashlist[index], big_part))
        self.extend_symbol_list(self.symbolist, map(lambda index: self.hashlist[index], medium_part))
        self.extend_symbol_list(self.symbolist, map(lambda index: self.hashlist[index], small_part))

    def calculate(self):
        self.load_stock_data()
        if len(self.stockdata) == 0:
            self.logger.critical("Could not load stock data (the initial date is %s, try setting a more recent one.)" % self.datefrom.isoformat())
            exit(-1)
        self.partitionize()

    def gen_visual_string(self):
        grid = draw_spiral(self.symbolist)
        return pretty_print_grid(grid,
                                 self.datefrom.isoformat(),
                                 datetime.date.today().isoformat())  # [last element][first 8 characters]

    def visualize(self):
        print(self.gen_visual_string())

    def visualize_png(self):
        string_to_png(self.gen_visual_string(), self.cliparams.image_output, font=self.cliparams.font)


class objectview():
    def __init__(self, d):
        self.__dict__ = d


if __name__ == "__main__":
    cli = parsecli()

    loglevel = logging.INFO
    if cli.debug:
        loglevel = logging.DEBUG
    elif cli.quiet:
        loglevel = logging.ERROR

    div = DivergenceViewer(cli, loglevel=loglevel)
    div.calculate()
    if cli.image_output != "no":
        div.visualize_png()
    else:
        div.visualize()
