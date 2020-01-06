from day7 import *


def test_max_signal():
    codes = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    sequence = [4, 3, 2, 1, 0]
    t = Thruster(codes)
    assert max_signal(t) == 43210


def test_thruster_output():
    codes = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    t = Thruster(codes)
    sequence = [4, 3, 2, 1, 0]
    assert t.thruster_signal(sequence) == 43210
    codes = [
        3,
        23,
        3,
        24,
        1002,
        24,
        10,
        24,
        1002,
        23,
        -1,
        23,
        101,
        5,
        23,
        23,
        1,
        24,
        23,
        23,
        4,
        23,
        99,
        0,
        0,
    ]
    t = Thruster(codes)
    seq = [0, 1, 2, 3, 4]
    assert t.thruster_signal(seq) == 54321
    codes = [
        3,
        31,
        3,
        32,
        1002,
        32,
        10,
        32,
        1001,
        31,
        -2,
        31,
        1007,
        31,
        0,
        33,
        1002,
        33,
        7,
        33,
        1,
        33,
        31,
        31,
        1,
        32,
        31,
        31,
        4,
        31,
        99,
        0,
        0,
        0,
    ]
    seq = [1, 0, 4, 3, 2]
    t = Thruster(codes)
    assert t.thruster_signal(seq) == 65210


def test_feedback_loop():
    example_codes : List[int]= [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    t = Thruster(example_codes)
    assert t.feedback_loop([9,8,7,6,5]) == 139629729
    c2 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    assert max_feedback(t) == 139629729
    t2 = Thruster(c2)
    assert t2.feedback_loop([9,7,8,5,6]) == 18216
   # assert max_feedback(t2) == 18216


