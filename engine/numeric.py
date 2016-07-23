import math
from hashlib import sha1


bigsize = 250
mediumsize = 25
smallsize = 1


def partition(length):
    big = int(math.floor((length-1) / bigsize))
    remainder = length - (big * bigsize)
    medium = int(math.floor((remainder-1) / mediumsize))
    remainder -= (medium * mediumsize)

    if medium == 0 and big > 0:  # to look nicer
        big -= 1
        remainder = length - (big * bigsize)
        medium = int(math.floor((remainder-1) / mediumsize))
        remainder -= (medium * mediumsize)

    return big, medium, remainder


def hashify(resultlist):
    def step(aprevhash, elem):
        date = elem[0]
        hashed = sha1((aprevhash[1] + "#" + str(elem[1])).encode("utf-8")).hexdigest()
        return date, hashed

    hashlist = []
    prevhash = ("", "start")
    for item in resultlist:
        currhash = step(prevhash, item)
        hashlist.append(currhash)
        prevhash = currhash

    return hashlist


def get_partiton_representative(alist, apartition, sep=(None, None)):
    repres = []
    (big, medium, small) = apartition
    curs = 0
    for b in range(big):
        curs += bigsize
        repres.append(alist[curs-1])

    if sep[0] is not None:
        repres.append(sep[0])

    for m in range(medium):
        curs += mediumsize
        repres.append(alist[curs-1])

    if sep[1] is not None:
        repres.append(sep[1])

    for s in range(small):
        curs += smallsize
        repres.append(alist[curs-1])

    return repres
