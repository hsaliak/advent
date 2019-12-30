from day5 import *


def test_machine():
    m = Machine([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    m.process()
    assert m.codes == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    m.codes = [1, 0, 0, 0, 99]
    m.process()
    assert m.codes == [2, 0, 0, 0, 99]

    m.codes = [2, 3, 0, 3, 99]
    m.process()
    assert m.codes == [2, 3, 0, 6, 99]

    m.codes = [2, 4, 4, 5, 99, 0]
    m.process()
    assert m.codes == [2, 4, 4, 5, 99, 9801]

    m.codes = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    m.process()
    assert m.codes == [30, 1, 1, 4, 2, 5, 6, 0, 99]
    m.codes = [1002, 4, 3, 4,33]
    m.process()
    assert m.codes[-1]  == 99

def test_programs():
    equal_to_8 = [ 3,9,8,9,10,9,4,9,99,-1,8]
    m = Machine(equal_to_8, 0)
    m.codes = equal_to_8
    m.io = 1
    m.process()
    assert m.io == 0
    m.codes = equal_to_8
    m.io = 8
    m.process()
    assert m.io == 1
    less_than_8 = [3,9,7,9,10,9,4,9,99,-1,8]
    m.codes = less_than_8
    m.io = 1
    m.process()
    assert m.io == 1
    m.codes = less_than_8
    m.io = 35
    m.process()
    assert m.io == 0
    equal_to_8_imm = [ 3,3,1108,-1,8,3,4,3,99]
    m.codes = equal_to_8_imm 
    m.io = 4
    m.process()
    assert m.io == 0
    m.codes = equal_to_8_imm 
    m.io = 8
    m.process()
    assert m.io == 1
    less_than_8_imm  = [3,3,1107,-1,8,3,4,3,99]
    m.codes = less_than_8_imm
    m.io = 4
    m.process()
    assert m.io == 1
    m.codes = less_than_8_imm
    m.io = 8
    m.process()
    assert m.io == 0
    m.io = 9
    m.process()
    assert m.io == 0
    m.io = 4
    m.process()
    assert m.io == 1

def test_large_program():
    prog = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    prog_imm = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    m = Machine(prog, 0)
    m.process()
    assert m.io == 0
    mm = Machine(prog_imm,0)
    mm.process()
    assert mm.io == 0
    m.io = 1
    m.codes = prog
    m.process()
    assert m.io == 1
    mm.io = 1
    mm.codes = prog_imm
    mm.process()
    assert mm.io == 1
  
   

