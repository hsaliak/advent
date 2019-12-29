from typing import List, Iterator
import numpy as np
import numba as nb
from numba import jit_module


def to_digits(n: int) -> List[int]:
    d: int = 0
    l :List[int] = []
    while n >= 10:
        n, d = divmod(n, 10)
        l.append(d)
    l.append(n)
    l.reverse()
    return l

def is_six_digit(ds : List[int]) -> bool:
    return len(ds) == 6

def in_range(n : int, hi = 843212, lo = 353096) -> bool:
    return (n >= lo) and (n <= hi)

def repeated_adjacents(ds : List[int]) -> bool:
    d = np.array(ds)
    return not(np.all(d[:-1] - d[1:]))

def increasing_digits(ds : List[int]) -> bool:
    d = np.array(ds)
    return np.all(d[1:] - d[:-1] >= 0)

def pass_criteria(n:int)->bool:
    ds : List[int]= to_digits(n) 
    return  increasing_digits(ds) and repeat_criteria(ds)


def numbers_in_range(lo = 353096, hi = 843212)-> int:
    count = 0
    for i in range(lo, hi+1):
        if pass_criteria(i):
            count += 1
    return count


def repeat_criteria(ds : List[int]) -> bool:
    vals = ds[:]
    prev = -2
    repeats = False
    adjacents = True
    while len(vals) >  0:
        tmp = vals.pop() # last item.
        if tmp == prev:
            if repeats == False:  
                repeats = True # continue scanning
            else: #repeats == True, toggle it and move on
                repeats = False # dont count
                adjacents = True
        else: #tmp != prev
            if repeats == True: # 123444 case, we are at 
                if adjacents == True:
                    repeats = False
                    adjacents = False
                else:
                    return True
            if prev != -1:
                adjacents = False
            prev = tmp
    return repeats and not adjacents
jit_module(nogil=True, cache=True)
print(numbers_in_range())
