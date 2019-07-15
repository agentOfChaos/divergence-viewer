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


def custom_round(number, precision):
    (integer, decimal) = number.split(".")
    
    integers = list(map(lambda d: int(d), integer))
    decimals = list(map(lambda d: int(d), decimal))
    
    rounded_decimals = []
    rounded_integers = []
    
    carry = 0
    for index,digit in reversed(list(enumerate(decimals))):
        digit = digit + carry
        carry = 0
        if digit >= 10:
            digit = 0
            carry = 1
            
        if index >= precision:
            if digit >= 5: carry = 1
        else:
            rounded_decimals.insert(0, digit)
            
    for index,digit in reversed(list(enumerate(integers))):
        digit = digit + carry
        carry = 0
        if digit >= 10:
            digit = 0
            carry = 1
        rounded_integers.insert(0, digit);
    if carry > 0:
        rounded_integers.insert(0, 1);
            
    return "".join(list(map(lambda n: str(n), rounded_integers))) + "." + "".join(list(map(lambda n: str(n), rounded_decimals)))
            

def hashchain(mylist):
    worklist = [("start", "start")] + mylist
    hashlist = []
    
    #print(" 0.00,",end="")

    def string_hash(mystring):
        return sha256(mystring.encode("utf-8")).hexdigest()

    def stepfun(index):
        elem = worklist[index]
        value = elem[1]
        #print("\"" + hashlist[index-1] + "#" + value + "\" = " + string_hash(hashlist[index-1] + "#" + value))
        #print("%5.2f" % float(value) ,end=',')
        #print("%5s" % value,end=',')
        return string_hash(hashlist[index-1] + "#" + value)

    hashlist.append(string_hash("start"))
    for index in range(len(mylist)):
        hashlist.append(stepfun(index+1))

    return hashlist

