from day4 import *


def test_to_digits():
    digits1 = [i for i in to_digits(1234)]
    digits2 = [i for i in to_digits(-1)]
    digits3 = [i for i in to_digits(1)]
    digits4 = [i for i in to_digits(10)]

    assert digits1 == [1, 2, 3, 4]
    assert digits2 == [-1]
    assert digits3 == [1]
    assert digits4 == [1, 0]


def test_pass():
    assert pass_criteria(111111) == False
    assert pass_criteria(555541) == False
    assert pass_criteria(223450) == False
    assert pass_criteria(123789) == False


def d(n):
    ds = to_digits(n)
    l = list()
    for i in ds:
        l.append(i)
    return l


def test_repeat_criteria():
    assert repeat_criteria(d(112233)) == True
    assert repeat_criteria(d(123444)) == False
    assert repeat_criteria(d(111133)) == True
    assert repeat_criteria(d(555541)) == False
    assert repeat_criteria(d(111111)) == False
    assert repeat_criteria(d(777888)) == False
    assert repeat_criteria(d(789999)) == False
