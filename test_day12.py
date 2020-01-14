import pytest
from day12 import *


def test_moon() ->None:
    m1 : Moon = Moon(pos=[-1,0,2])
    m2 : Moon = Moon(pos=[2,-10,-7])
    m3 : Moon = Moon(pos=[4,-8,8])
    m4 : Moon = Moon(pos=[3,5,-1])
    hb = HeavenlyBody([m1,m2,m3,m4])
    hb.step()
    assert Moon(pos=[2,-1,1],vel=[3,-1,-1] in hb.celestials)
    hb.step()
    assert Moon(pos=[1,-2,2],vel=[-2,5,6] in hb.celestials)
    hb.step()
    assert Moon(pos=[2,1,-5],vel=[1,5,-4] in hb.celestials)


def test_energy() -> None:
    m1 : Moon = Moon(pos=[-1,0,2])
    m2 : Moon = Moon(pos=[2,-10,-7])
    m3 : Moon = Moon(pos=[4,-8,8])
    m4 : Moon = Moon(pos=[3,5,-1])
    hb = HeavenlyBody([m1,m2,m3,m4])
    for i in range(10):
        hb.step()
    assert hb.energy == 179

def test_steps() -> None:
    m1 : Moon = Moon([-1,0,2],[0,0,0])
    m2 : Moon = Moon([2,-10,-7], [0,0,0])
    m3 : Moon = Moon([4,-8,8],[0,0,0])
    m4 : Moon = Moon([3,5,-1], [0,0,0])
    hb = HeavenlyBody([m1,m2,m3,m4])
    nrepeats = hb.repeats()
    assert nrepeats == 2772
