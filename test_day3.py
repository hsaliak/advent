from day3 import *


example1: Tuple[str, str] = (
    "R75,D30,R83,U83,L12,D49,R71,U7,L72",
    "U62,R66,U55,R34,D71,R55,D58,R83",
)
example2 = ("R8,U5,L5,D3", "U7,R6,D4,L4")


def test_compute_dist():
    assert compute_dist(example1) == 159
    assert compute_dist(example2) == 6


def test_compute_signal():
    c = CircuitBoard(*example1)
    p = c.compute_signal_delay()
    assert c.signal_delays(p) == 610
    c2 = CircuitBoard(*example2)
    p2 = c2.compute_signal_delay()
    assert c2.signal_delays(p2) == 30
