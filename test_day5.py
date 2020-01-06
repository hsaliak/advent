import machine
from day5 import *


def test_machine():
    m = Machine([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    m.process()
    assert m.codes == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    m.codes = [1, 0, 0, 0, 99]
    m.iptr = 0
    m.process()
    assert m.codes == [2, 0, 0, 0, 99]

    m.codes = [2, 3, 0, 3, 99]
    m.iptr = 0
    m.process()
    assert m.codes == [2, 3, 0, 6, 99]

    m.codes = [2, 4, 4, 5, 99, 0]
    m.iptr = 0
    m.process()
    assert m.codes == [2, 4, 4, 5, 99, 9801]

    m.codes = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    m.iptr = 0
    m.process()
    assert m.codes == [30, 1, 1, 4, 2, 5, 6, 0, 99]
    m.codes = [1002, 4, 3, 4, 33]
    m.iptr = 0
    m.process()
    assert m.codes[-1] == 99


def test_programs():
    equal_to_8 = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    m = Machine(equal_to_8, [1])
    m.process()
    assert m.io.pop() == 0
    m = Machine(equal_to_8, [8])
    m.process()
    assert m.io.popleft() == 1
    less_than_8 = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    m = Machine(less_than_8, [1])
    m.process()
    assert m.io.popleft() == 1
    m = Machine(less_than_8, [35])
    m.process()
    assert m.io.pop() == 0
    equal_to_8_imm = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    m = Machine(equal_to_8_imm, [4])
    m.process()
    assert m.io.pop() == 0
    m = Machine(equal_to_8_imm, [8])
    m.process()
    assert m.io.pop() == 1
    less_than_8_imm = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    m = Machine(less_than_8_imm, [4])
    m.process()
    assert m.io.pop() == 1
    m = Machine(less_than_8_imm, [8])
    m.process()
    assert m.io.popleft() == 0
    m = Machine(less_than_8_imm, [9])
    m.process()
    assert m.io.popleft() == 0
    m = Machine(less_than_8_imm, [4])
    m.process()
    assert m.io.pop() == 1


def test_large_program():
    prog = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    prog_imm = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    m = Machine(prog, [0])
    m.process()
    assert m.io.pop() == 0
    mm = Machine(prog_imm, [0])
    mm.process()
    assert mm.io.pop() == 0
    m = Machine(prog, [1])
    m.process()
    assert m.io.pop() == 1
    mm = Machine(prog_imm, [1])
    mm.process()
    assert mm.io.pop() == 1
