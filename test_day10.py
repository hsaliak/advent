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


def test_target():
    p = Point(2,3)
    p2 = Point(4,5)
    t = target_from_point(p2, p)
    p2prime  = t.to_point(p)
    assert p2 == p2prime
    t1 = target_from_point(Point(2,3))
    t3 = target_from_point(Point(4,6))
    t4 = target_from_point(Point(1,0)) # 0 angle actually
    t5 = target_from_point(Point(0,100))
    t6 = target_from_point(Point(0,-0.01))
    assert t3 > t1  # grater  magnitude
    assert t4 > t1 #  this is a 90 degree
    assert  t6>  t3 > t1 >  t5
    print(sorted([t1,t3,t4,t5,t6]))

def test_map():
    m  = read_map("day10test")
    print(m)
    assert m == Map(xlen=5, ylen=5, asteroids={Point(x=1, y=0), Point(x=4, y=0), Point(x=0, y=2), Point(x=1, y=2), Point(x=2, y=2), Point(x=3, y=2), Point(x=4, y=2), Point(x=4, y=3), Point(x=3, y=4), Point(x=4, y=4)})
    
test_target()
