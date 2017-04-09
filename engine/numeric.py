import math
from hashlib import sha256


def partition(length, bigsize=250, mediumsize=25):
    """
    Shrink a list in a smart way
    :param length: length of the list to be partitioned
    :param bigsize:
    :param mediumsize:
    :return: (big_part, medium_part, small_part): lists of indices of elements to be placed in each partition
    """
    big_part, medium_part, small_part = [], [], []

    bigs = int(math.floor((length-1) / bigsize))
    remainders = length - (bigs * bigsize)
    mediums = int(math.floor((remainders-1) / mediumsize))
    remainders -= (mediums * mediumsize)

    if mediums == 0 and bigs > 0:  # to look nicer
        bigs -= 1
        remainders = length - (bigs * bigsize)
        mediums = int(math.floor((remainders-1) / mediumsize))
        remainders -= (mediums * mediumsize)

    cursor = 0

    for big_step in range(bigs):
        big_part.append(cursor)
        cursor += bigsize
    for medium_step in range(mediums):
        medium_part.append(cursor)
        cursor += mediumsize
    for small_step in range(remainders):
        small_part.append(cursor)
        cursor += 1

    return big_part, medium_part, small_part


def hashchain(mylist):
    worklist = [("start", "start")] + mylist
    hashlist = []

    def string_hash(mystring):
        return sha256(mystring.encode("utf-8")).hexdigest()

    def stepfun(index):
        elem = worklist[index]
        value = elem[1]
        return string_hash(hashlist[index-1] + "#" + value)

    hashlist.append(string_hash("start"))
    for index in range(len(mylist)):
        hashlist.append(stepfun(index+1))

    return hashlist

