import enum
import array
from typing import List, Dict, Deque, Iterable
from collections import deque
import logging

#logging.basicConfig(filename="machine.log", level=logging.DEBUG)


class OpCode(enum.IntEnum):
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


class Mode(enum.IntEnum):
    POS = 0
    IMM = 1


class Machine:
    def opcode(self, v: int) -> OpCode:
        vs: str = str(v)
        return OpCode(int(vs[-2:]))

    def param1(self, v: int) -> Mode:
        vs: str = str(v)
        vs = "0" * (4 - len(vs)) + vs
        return Mode(int(vs[-3]))

    def param2(self, v: int) -> Mode:
        vs: str = str(v)
        vs = "0" * (4 - len(vs)) + vs
        return Mode(int(vs[-4]))

    def __init__(self, intcodes: List[int], io: Iterable[int] = [1]):
        self.intcodes: array.array[int] = array.array( "l", intcodes)  # i can haz efficient
        self.factory_defaults: array.array[int] = array.array( "l", self.intcodes)
        self.mode: Mode = Mode.POS
        self._io: Deque[int] = deque(io)
        self.iptr =  0  # instruction pointer
        self.halted : bool= False
        self.params_count: Dict[OpCode, int] = {
            OpCode.ADD: 4,
            OpCode.MUL: 4,
            OpCode.SAV: 2,
            OpCode.LOA: 2,
            OpCode.JIT: 3,
            OpCode.JIF: 3,
            OpCode.LT: 4,
            OpCode.EQ: 4,
            OpCode.FIN: 1,
            OpCode.UNK: 1,
        }

    def restart(self) -> None:
        self.halted = False
        self.iptr = 0
        self.io = deque([])
        self.intcodes = array.array("l", self.factory_defaults)

    def process(self) -> None:
        # the instruction set is 4.
        #self.iptr = 0
        while self.iptr < len(self.intcodes):
            # for i in range(self.stride, len(self.intcodes), self.stride):
            op: int = self.intcodes[self.iptr]
            param1: Mode = Mode.POS
            param2: Mode = Mode.POS
            if op > 10:
                _op: OpCode = self.opcode(op)
                if self.params_count[_op] > 1:
                    param1 = self.param1(op)
                if self.params_count[_op] > 2:
                    param2 = self.param2(op)
                op = _op
            op = OpCode(op)
            # convert to parameter mode or sh
            stride: int = self.params_count[op]
            self.step(op, stride, param1, param2)  # moves iptr
            if op == OpCode.LOA:
                #logging.debug(f'yielding control {self._io}')
                return # yeild control back to the caller, 
        #logging.debug(f'halting control')
        #self.iptr = 0

    def step(self, opcode: OpCode, stride: int, param1: Mode, param2: Mode) -> None:
        ins: array.array[int] = self.intcodes[self.iptr : self.iptr + stride]
        # ins  = self.intcodes[self.iptr : self.iptr + stride]
        advance: bool = True
        codes = self.intcodes
        if len(ins) != stride and len(ins) != 1:
            raise ValueError(f"uknown instr: {ins}, stride: {stride}")
        if opcode == OpCode.FIN:
            self.iptr = len(self.intcodes)  # advance to the end
            self.halted = True
            return
        if stride > 1:
            v1: int = ins[1] if param1 == Mode.IMM else codes[ins[1]]
        if stride > 2:
            v2: int = ins[2] if param2 == Mode.IMM else codes[ins[2]]
        if opcode == OpCode.ADD:
            loc = ins[3]
            codes[loc] = v1 + v2
        elif opcode == OpCode.MUL:
            loc = ins[3]
            codes[loc] = v1 * v2
        elif opcode == OpCode.SAV:
            loc = ins[1]
            codes[loc] = self._io.popleft()
        elif opcode == OpCode.LOA:
            loc = ins[1]
            self._io.append(codes[loc])
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
            raise ValueError(f"uknown instr: {ins}, stride: {stride}")
        if advance:
            self.iptr += self.params_count[opcode]  # advance by the instruction

    @property 
    def io(self) -> Deque[int]:
        return self._io
    @io.setter
    def io(self, ios : Iterable[int]) -> None:
        self._io = deque(ios)

    @property
    def codes(self) -> List[int]:
        return self.intcodes.tolist()

    @codes.setter
    def codes(self, intcodes: List[int]) -> None:
        self.intcodes = array.array("l", intcodes)

