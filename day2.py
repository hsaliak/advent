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
import numba as nb
import array
import numpy as np

logging.basicConfig(filename='day2.log', level=logging.DEBUG)

class OpCode(enum.IntEnum):
    ADD = 1
    MUL = 2
    FIN = 99
    UNK = -1


machine_spec = [ 
    ('intcodes', nb.int64[:]),
    ('stride', nb.int64) ]

    
@nb.jitclass(machine_spec)
class _Machine:
    def __init__(self, intcodes : np.ndarray , stride :int ):
        self.intcodes = intcodes
        self.stride = stride

    def process(self):
        stride : int = self.stride
        for i in range(stride,len(self.intcodes), stride):
            code = self.step(self.intcodes[i-self.stride:i])
            if code == OpCode.UNK:
                print("Unable to process")
                return
            if code == OpCode.FIN:
                break

    def step(self,ins:List[int] ) -> int:
        if len(ins) != self.stride and len(ins) != 1:
            return OpCode.UNK
        if ins[0] == OpCode.FIN:
            return OpCode.FIN

        opcode, arg1, arg2, loc  = ins
        if opcode == OpCode.ADD:
            self.intcodes[loc] = self.intcodes[arg1] + self.intcodes[arg2]
        elif opcode == OpCode.MUL:
            self.intcodes[loc] = self.intcodes[arg1] * self.intcodes[arg2]
        else:
            print("unknown instr:",  opcode)
            opcode = OpCode.FIN
        return opcode
        
 
class Machine:
    def __init__(self, intcodes : List[int], stride : int):
        self.stride = stride
        self.intcodes = intcodes
        self._m = _Machine(np.array(intcodes), stride)

    def  process(self):
        logging.debug(f"initial intcodes: {self.intcodes}")
        self._m.process()
        self.intcodes = self._m.intcodes.tolist() # sync intcodes

    @property
    def codes(self) -> List[int]:
        return self.intcodes
    @codes.setter
    def codes(self, intcodes : List[int]):
        self.intcodes = intcodes
        self._m.intcodes = np.array(self.intcodes)


def get_intcodes(fname : str) -> List[int]:
    vals : List[int]  = []
    with open(fname) as f:
        line = f.readlines()[0]
        vals = [int(v) for v in line.split(',')]
    return vals

def day2_1(intcodes : List[int],v1 : int ,v2 : int):
    intcodes[1] = v1 
    intcodes[2] = v2
    m = Machine(intcodes, 4)
    m.process()
    print(m.codes)

def day2_2(intcodes: List[int]) -> Tuple[int,int]:
    m = Machine(intcodes, 4)
    for noun, verb in itertools.combinations(range(100),2):
        codes = intcodes[:] # make a copy
        codes[1] = noun
        codes[2] = verb
        m.codes = codes
        m.process()
        if m.codes[0] == 19690720:
            logging.debug(f"found {noun}, {verb}")
            return (noun,verb)
    return (-1,-1)

        
        
        
        
    

    
if __name__ == '__main__':
    intcodes = get_intcodes('day2input')
    day2_1(intcodes[:], 12,2)
    out = -1
    vs = day2_2(intcodes[:])
    print(vs)
