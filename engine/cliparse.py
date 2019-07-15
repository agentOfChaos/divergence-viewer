import argparse

from .stock_chomp import StockChomper


default_datefrom = '1962-01-02'


def parsecli():
    parser = argparse.ArgumentParser(description="Remote server for the MoonrabbitOS filesystem protocol.")
    parser.add_argument('--roman', '-r', help='Roman mode (suppress japanese output)', action="store_true")
    parser.add_argument('--color', '-c', help='Colorize output (default off)', action="store_true")
    parser.add_argument('--debug', '-d', help='Enables debug messages', action="store_true")
    parser.add_argument('--quiet', '-q', help='Suppresses all messages except errors', action="store_true")
    parser.add_argument('--image-output', '-i', metavar='filename',
                        help='Do not output to stdout, generate an image instead', type=str, default='no')
    parser.add_argument('--font', '-f', help='Font to use in the image (see -i)', type=str,
                        default='NotoSansMonoCJKjp-Regular.otf')
    parser.add_argument('--beginning', '-b', help='Initial date to start gathering historical data from', type=str, default=default_datefrom)
    return parser.parse_args()
