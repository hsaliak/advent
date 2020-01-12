from machine import *


def test_day9():
    codes = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    m = Machine(codes, io=[])
    while not m.halted:
        m.process()

    assert [i for i in m.io] == codes
    codes2 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    m2 = Machine(codes2, io=[])
    m2.process()
    len(str(m2.io.pop())) == 16
    codes3 = [104, 1125899906842624, 99]
    m3 = Machine(codes3, io=[])
    m3.process()
    assert m3.io.pop() == 1125899906842624


test_day9()
