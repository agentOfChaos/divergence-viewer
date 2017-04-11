import argparse

from .stock_chomp import StockChomper


def parsecli():
    parser = argparse.ArgumentParser(description="Display a visual \"hash\" of the current timeline, by aggregating"
                                                 " data from stock history. It will not work prior to %s" %
                                                 StockChomper.datefrom.isoformat())
    parser.add_argument('--roman', '-r', help='Roman mode (suppress japanese output)', action="store_true")
    parser.add_argument('--color', '-c', help='Colorize output (default off)', action="store_true")
    parser.add_argument('--debug', '-d', help='Enables debug messages', action="store_true")
    parser.add_argument('--quiet', '-q', help='Suppresses all messages except errors', action="store_true")
    parser.add_argument('--image-output', '-i', metavar='filename',
                        help='Do not output to stdout, generate an image instead', type=str, default='no')
    parser.add_argument('--font', '-f', help='Font to use in the image (see -i)', type=str,
                        default='NotoSansMonoCJKjp-Regular.otf')
    return parser.parse_args()
