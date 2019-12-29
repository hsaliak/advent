from day2 import *


def test_machine():
    m = Machine([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], 4)
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
