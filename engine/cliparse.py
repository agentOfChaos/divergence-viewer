import argparse

from engine.stock_chomp import StockChomper


def parsecli():
    parser = argparse.ArgumentParser(description="Display a visual \"hash\" of the current timeline, by aggregating"
                                                 " data from stock history. It will not work prior to %s" %
                                                 StockChomper.datefrom.isoformat())
    parser.add_argument('--roman', '-r', help='Roman mode (suppress japanese output)', action="store_true")
    parser.add_argument('--color', '-c', help='Colorize output (default off)', action="store_true")
    parser.add_argument('--debug', '-d', help='Enables debug messages', action="store_true")
    parser.add_argument('--quiet', '-q', help='Suppresses all messages except errors', action="store_true")
    return parser.parse_args()
