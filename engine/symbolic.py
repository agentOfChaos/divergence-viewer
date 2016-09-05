import romkan
from colorama import Style, Fore


kana = "アイウエオ" \
       "カキクケコ" \
       "サシスセソ" \
       "タチツテト" \
       "ナニヌネノ" \
       "ハヒフヘホ" \
       "マミムメモヤユヨ" \
       "ラリルレロワ" \
       "ガギグゲゴ" \
       "ザジズゼゾダデド" \
       "バビブベボ" \
       "パピプペポ"

colors = [col + style for col in (Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW)
          for style in (Style.DIM, Style.NORMAL, Style.BRIGHT)]


def hash2symbol(hashval, nihon=True, color=False):
    num = int(hashval, 16)
    symbol = kana[num % len(kana)]
    if not nihon:
        symbol = romkan.to_kunrei(symbol)
        if len(symbol) == 1:
            symbol = symbol + symbol
    if color:
        symbol = colors[num % len(colors)] + symbol + Style.RESET_ALL + Fore.RESET
    return symbol
