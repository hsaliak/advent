from day10 import *


def test_points():
    p1 = Point(0,0)
    p2 = Point(1,0)
    p3 = Point(2,0)
    assert unit_vector(p1,p2) == unit_vector(p2,p3) == unit_vector(p1,p3)

    nv = unit_vector(p1,p2)
    p  = Point(-nv.x, -nv.y)
    assert p == unit_vector(p2,p1)
    #assert len(s) == 1


def test_map():
    m  = read_map("day10test")
    print(m)
    assert m == Map(xlen=5, ylen=5, asteroids={Point(x=1, y=0), Point(x=4, y=0), Point(x=0, y=2), Point(x=1, y=2), Point(x=2, y=2), Point(x=3, y=2), Point(x=4, y=2), Point(x=4, y=3), Point(x=3, y=4), Point(x=4, y=4)})
    
