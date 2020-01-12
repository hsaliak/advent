import enum
import array
from typing import List, Dict, Deque, Iterable
from collections import deque
import logging
import math

# logging.basicConfig(filename="machine.log", level=logging.DEBUG)


class OpCode(enum.IntEnum):
    ADD = 1
    MUL = 2
    SAV = 3
    LOA = 4
    JIT = 5
    JIF = 6
    LT = 7
    EQ = 8
    REL = 9
    VMOD = 97
    VNOP = 98
    FIN = 99
    UNK = -1


class Mode(enum.IntEnum):
    POS = 0
    IMM = 1
    REL = 2


class Machine:
    def __init__(self, intcodes: List[int], io: Iterable[int] = [1]):
        self.intcodes: array.array[int] = array.array(
            "l", intcodes
        )  # i can haz efficient
        self.pagesize = len(self.intcodes) * 16
        self.factory_defaults: array.array[int] = array.array("l", self.intcodes)
        self.mode: Mode = Mode.POS
        self._io: Deque[int] = deque(io)
        self.iptr = 0  # instruction pointer
        self.relative_base = 0  # day 9, adding relative base
        self.halted: bool = False
        self.params_count: Dict[OpCode, int] = {
            OpCode.ADD: 4,
            OpCode.MUL: 4,
            OpCode.SAV: 2,
            OpCode.LOA: 2,
            OpCode.JIT: 3,
            OpCode.JIF: 3,
            OpCode.LT: 4,
            OpCode.EQ: 4,
            OpCode.REL: 2,
            OpCode.FIN: 1,
            OpCode.UNK: 1,
        }

    def restart(self) -> None:
        self.halted = False
        self.iptr = 0
        self.relative_base = 0
        self.io = deque([])
        self.intcodes = array.array("l", self.factory_defaults)

    def handle_page_fault(self, loc: int) -> None:
        """ handle page fault of location. page in that memory """
        # note: we are actually not using "pages", but just allocating
        # contingent chunks of memory
        # but this mechanism is intended for us to easily extend the
        # memory model into a paging based one if necessary.
        additional: int = loc - len(self.intcodes) + 1  # avoid zeros
        # print("handling page fault", loc, len(self.intcodes))
        if additional < 0:
            raise ValueError(
                f"unexpected fault, {loc} should be paged into memory of size {len(self.intcodes)}"
            )
        pagecount: int = math.ceil(additional / self.pagesize)
        self.intcodes.extend([0] * (self.pagesize * pagecount))
        # print(len(self.intcodes))

    def process(self) -> None:
        # the instruction set is 4.
        # self.iptr = 0
        while self.iptr < len(self.intcodes):
            op: int = self.intcodes[self.iptr]
            param1: Mode = Mode.POS
            param2: Mode = Mode.POS
            param3: Mode = Mode.POS
            if op > 10:
                _op: OpCode = self.opcode(op)
                if self.params_count[_op] > 1:
                    param1 = self.param1(op)
                if self.params_count[_op] > 2:
                    param2 = self.param2(op)
                if self.params_count[_op] > 3:
                    param3 = self.param3(op)
                op = _op
            op = OpCode(op)
            # convert to parameter mode or sh
            stride: int = self.params_count[op]
            self.step(op, stride, param1, param2, param3)  # moves iptr
            if op == OpCode.LOA:
                # logging.debug(f'yielding control {self._io}')
                return  # yeild control back to the caller,
        # logging.debug(f'halting control')
        # self.iptr = 0

    def step(
        self, opcode: OpCode, stride: int, param1: Mode, param2: Mode, param3: Mode
    ) -> None:
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
            v1: int = self.fetch(ins[1], param1)
            # v1: int = ins[1] if param1 == Mode.IMM else codes[ins[1]]
        if stride > 2:
            v2: int = self.fetch(ins[2], param2)

        if opcode == OpCode.ADD:
            loc = ins[3]
            self.store(v1 + v2, loc, param3)
        elif opcode == OpCode.MUL:
            loc = ins[3]
            self.store(v1 * v2, loc, param3)
        elif opcode == OpCode.SAV:
            loc = ins[1]
            self.store(self._io.popleft(), loc, param1)
        elif opcode == OpCode.LOA:
            loc = ins[1]
            self._io.append(self.fetch(loc, param1))
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
                self.store(1, loc, param3)
            else:
                self.store(0, loc, param3)
        elif opcode == OpCode.LT:
            loc = ins[3]
            if v1 < v2:
                self.store(1, loc, param3)
            else:
                self.store(0, loc, param3)
        elif opcode == OpCode.REL:
            # relative base instruction is always value based
            self.relative_base = self.relative_base + v1
        else:
            raise ValueError(f"uknown instr: {ins}, stride: {stride}")
        if advance:
            self.iptr += self.params_count[opcode]  # advance by the instruction

    def opcode(self, v: int) -> OpCode:
        vs: str = str(v)
        return OpCode(int(vs[-2:]))

    def param1(self, v: int) -> Mode:
        vs: str = str(v)
        vs = "0" * (5 - len(vs)) + vs
        return Mode(int(vs[-3]))

    def param2(self, v: int) -> Mode:
        vs: str = str(v)
        vs = "0" * (5 - len(vs)) + vs
        return Mode(int(vs[-4]))

    def param3(self, v: int) -> Mode:
        vs: str = str(v)
        vs = "0" * (5 - len(vs)) + vs
        return Mode(int(vs[-5]))

    def fetch(self, arg: int, param: Mode) -> int:
        "fetch a parameter from memory according to mode"
        if param == Mode.IMM:
            return arg  # just return the value
        elif param == Mode.REL:
            arg = arg + self.relative_base
        else:
            pass
        if arg >= len(self.intcodes):
            self.handle_page_fault(arg)
        # print(arg, len(self.intcodes))
        return self.intcodes[arg]

    def store(self, value: int, loc: int, param: Mode) -> None:
        if param == Mode.REL:
            loc = loc + self.relative_base
        if loc >= len(self.intcodes):
            self.handle_page_fault(loc)
        self.intcodes[loc] = value

    @property
    def io(self) -> Deque[int]:
        return self._io

    @io.setter
    def io(self, ios: Iterable[int]) -> None:
        self._io = deque(ios)

    @property
    def codes(self) -> List[int]:
        return self.intcodes.tolist()

    @codes.setter
    def codes(self, intcodes: List[int]) -> None:
        self.intcodes = array.array("l", intcodes)
