#cython: language_level=3
#cython: boundscheck=False
#cython: nonecheck=False
import enum
import array 
from typing import List, Dict
import cython

#class OpCode(enum.IntEnum):
cdef enum OpCode:
    ADD = 1
    MUL = 2
    SAV = 3
    LOA = 4
    JIT = 5
    JIF = 6
    LT = 7
    EQ = 8
    VMOD = 97
    VNOP = 98
    FIN = 99
    UNK = -1

#class Mode(enum.IntEnum):
cdef enum Mode:
    POS = 0
    IMM = 1

cdef class Machine:
    cdef public cython.int io 
    iptr : cython.ulong 
    params_count : Dict[OpCode, int]
    mode : cython.int
    intcodes : cython.long[:]

    cdef OpCode opcode(self, v :cython.int):
        vs : str = str(v)
        return int(vs[-2:])

    cdef Mode param1(self, v :cython.int):
        vs : str = str(v)
        vs = '0'*(4-len(vs)) + vs 
        return int(vs[-3])
    
    cdef Mode param2(self, v : cython.int):
        vs : str = str(v)
        vs = '0'*(4-len(vs)) + vs 
        return int(vs[-4])

    def  __init__(self, intcodes: List[int], io=1):
        self.intcodes = array.array("l", intcodes)  # i can haz efficient
        self.mode : Mode = Mode.POS
        self.io = io
        self.iptr = -1 # instruction pointer
        self.params_count : Dict[OpCode, int] = {OpCode.ADD : 4, OpCode.MUL : 4, 
            OpCode.SAV : 2, OpCode.LOA : 2, 
            OpCode.JIT : 3, OpCode.JIF : 3, 
            OpCode.LT : 4, OpCode.EQ : 4,
            OpCode.FIN : 1, OpCode.UNK : 1}

    def process(self) -> None:
        # the instruction set is 4. 
        self.iptr = 0
        while self.iptr < len(self.intcodes):
        #for i in range(self.stride, len(self.intcodes), self.stride):
            op : cython.ulong  = self.intcodes[self.iptr]
            param1 : Mode  =  Mode.POS
            param2 : Mode  = Mode.POS 
            if op > 10:
                _op : OpCode = self.opcode(op)
                if self.params_count[_op] > 1:
                    param1 = self.param1(op)
                if self.params_count[_op] > 2:
                    param2  = self.param2(op)
                op = _op
                # convert to parameter mode or sh
            stride : cython.int = self.params_count[op]
            self.step(op, stride, param1, param2 ) # moves iptr
        self.iptr = 0

    cdef void step(self, opcode : cython.long, stride : cython.long, param1 : Mode,
    param2 : Mode ):
        ins: array.array = self.intcodes[self.iptr : self.iptr + stride]
        advance : bool  = True
        codes = self.intcodes
        if len(ins) != stride and len(ins) != 1:
            return
            #raise ValueError(f"uknown instr: {ins}, stride: {stride}")
        if opcode == OpCode.FIN:
            self.iptr = len(self.intcodes) # advance to the end
            return 
        if stride > 1:
            v1 : cython.int = ins[1] if param1 == Mode.IMM else codes[ins[1]]
        if stride > 2:
            v2 : cython.int = ins[2] if param2 == Mode.IMM else codes[ins[2]]
        if opcode == OpCode.ADD:
            loc = ins[3]
            codes[loc] = v1 + v2
        elif opcode == OpCode.MUL:
            loc = ins[3]
            codes[loc] = v1 * v2
        elif opcode == OpCode.SAV:
            loc = ins[1]
            codes[loc] = self.io
        elif opcode == OpCode.LOA:
            loc =ins[1]
            self.io = codes[loc] 
        elif opcode == OpCode.JIT:
            if v1 != 0:
                self.iptr = v2
                advance = False 
        elif opcode == OpCode.JIF:
            if v1 == 0:
                self.iptr = v2
                advance = False
        elif opcode == OpCode.EQ:
            loc = ins[3]
            if v1 == v2:
                codes[loc] = 1
            else:
                codes[loc] = 0
        elif opcode == OpCode.LT:
            loc = ins[3]
            if v1 < v2:
                codes[loc] = 1
            else:
                codes[loc] = 0
        else:
            #raise ValueError(f"uknown instr: {ins}, stride: {stride}")
            return
        if advance: 
            self.iptr += self.params_count[opcode] # advance by the instruction 

    @property
    def codes(self) -> List[int]:
        return list(self.intcodes)

    @codes.setter
    def codes(self, intcodes: List[int]) -> None:
        self.intcodes = array.array("l", intcodes)

