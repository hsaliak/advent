# 1212 program alarm
# magic smoke escaped
# Intcode programs like gravity assist.

# Intcode == List of Integers separated by commas.
# 1) Look at first integer == is it an opcode 1, 2 or 99
# 2) 99 means program should halt.
# 1 adds together numbers from 2 positions and stores it in the third
# opcode 2 multiplies.
# once you are done with one opcode, move to the next one by stepping forward

# this is day5
# airconditioner needs to work by upgrading the ship computer to support 
# TEST 

# add OpCode 3, takes a single parameter as input and saves it
# to the poistion given by its only param. 3,50 => take input 3 and 
# save it to address 50. 

# OpCode 4 outputs it from 50


# 3, 0, 4, 0, 99 -- saves something to to 0 and then 4 0 and end.

# parameter modes. .. 
#position mode is parameter 0. .. 50 means address at 50.
# mode 1 is immediate mode. -- 50 means value is 50. 

# the modes, position or immediate is stored in the same value as 
# ins opcode. 
# opcode is 2 digit number. xy -> y is the ins. there can be multiple
# params.. one for each instruction. 
# 1002, 4, 3, 4, 33 

# opcode is 2 digits. 
# TEST diagnostic requesting from the user the ID of the system 
# inpyt -- provide 1 -- ID for air con. 
# output to 
import enum
from typing import List, Tuple, Dict
import attr
import logging
import itertools
import array
import numba as nb

logging.basicConfig(filename="day5.log", level=logging.DEBUG)

from machine import *


def get_intcodes(fname: str) -> List[int]:
    vals: List[int] = []
    with open(fname) as f:
        line = f.readlines()[0]
        vals = [int(v) for v in line.split(",")]
    return vals


def day2_1(intcodes: List[int], v1: int, v2: int):
    intcodes[1] = v1
    intcodes[2] = v2
    m = Machine(intcodes)
    m.process()


def day2_2(intcodes: List[int]) -> Tuple[int, int]:
    m = Machine(intcodes)
    for noun, verb in itertools.combinations(range(100), 2):
        codes = intcodes[:]  # make a copy
        codes[1] = noun
        codes[2] = verb
        m.codes = codes
        m.process()
        if m.codes[0] == 19690720:
            logging.debug(f"found {noun}, {verb}")
            return (noun, verb)
    return (-1, -1)

def day5_1(intcodes : List[int]) -> None:
    m = Machine(intcodes, 1)
    m.process()
    print(m.io)

def day5_2(intcodes : List[int]) -> None:
    m = Machine(intcodes, 5)
    m.process()
    print(m.io)

def equal_to_8():
    intcodes = [3,9,8,9,10,9,4,9,99,-1,8]
    m = Machine(intcodes, 1)
    m.process()
    print(m.io)
    m = Machine(intcodes, 8)
    m.process()
    print(m.io)
if __name__ == "__main__":
    intcodes = get_intcodes("day5input")
    #day2_1(intcodes[:], 4, 3)
    #day5_1(intcodes)
    #out = -1
    #vs = day2_2(intcodes[:])
    #print(vs)
    day5_2(intcodes)
