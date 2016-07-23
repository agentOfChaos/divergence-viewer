import romkan


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


def hash2symbol(hashval, nihon=True):
    num = int(hashval, 16)
    symbol = kana[num % len(kana)]
    if not nihon:
        symbol = romkan.to_kunrei(symbol)
        if len(symbol) == 1:
            symbol = symbol + symbol
    return symbol
