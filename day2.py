# 1212 program alarm

# magic smoke escaped
# Intcode programs like gravity assist.

# Intcode == List of Integers separated by commas.
# 1) Look at first integer == is it an opcode 1, 2 or 99
# 2) 99 means program should halt.
# 1 adds together numbers from 2 positions and stores it in the third
# opcode 2 multiplies.
# once you are done with one opcode, move to the next one by stepping forward


import enum
from typing import List, Tuple
import attr
import logging
import itertools
import array
import numba as nb

logging.basicConfig(filename="day2.log", level=logging.DEBUG)


class OpCode(enum.IntEnum):
    ADD = 1
    MUL = 2
    FIN = 99
    UNK = -1


class Machine:
    def __init__(self, intcodes: List[int], stride: int):
        self.intcodes = array.array("l", intcodes)  # i can haz efficient
        self.stride = stride

    def process(self) -> None:
        for i in range(self.stride, len(self.intcodes), self.stride):
            code = self.step(i)
            if code == OpCode.UNK:
                print("Unable to process")
                return
            if code == OpCode.FIN:
                break

    def step(self, offset) -> int:
        ins: array.array = self.intcodes[offset - self.stride : offset]
        codes = self.intcodes
        if len(ins) != self.stride and len(ins) != 1:
            return OpCode.UNK
        if ins[0] == OpCode.FIN:
            return OpCode.FIN

        opcode, arg1, arg2, loc = ins
        if opcode == OpCode.ADD:
            codes[loc] = codes[arg1] + codes[arg2]
        elif opcode == OpCode.MUL:
            codes[loc] = codes[arg1] * codes[arg2]
        else:
            print("unknown instr:", opcode)
            opcode = OpCode.FIN
        return opcode

    @property
    def codes(self) -> List[int]:
        return self.intcodes.tolist()

    @codes.setter
    def codes(self, intcodes: List[int]):
        self.intcodes = array.array("l", intcodes)


def get_intcodes(fname: str) -> List[int]:
    vals: List[int] = []
    with open(fname) as f:
        line = f.readlines()[0]
        vals = [int(v) for v in line.split(",")]
    return vals


def day2_1(intcodes: List[int], v1: int, v2: int):
    intcodes[1] = v1
    intcodes[2] = v2
    m = Machine(intcodes, 4)
    m.process()


def day2_2(intcodes: List[int]) -> Tuple[int, int]:
    m = Machine(intcodes, 4)
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


if __name__ == "__main__":
    intcodes = get_intcodes("day2input")
    day2_1(intcodes[:], 12, 2)
    out = -1
    vs = day2_2(intcodes[:])
    print(vs)
