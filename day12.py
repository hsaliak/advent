from __future__ import annotations # so that i can have forward ref
import itertools 
from itertools import chain
from typing import List, Set  , Tuple, Dict
from dataclasses import dataclass, field
from math import gcd
from functools import reduce, lru_cache

def lcm(v1 : int, v2 : int) -> int :
    return v1 * v2 // gcd(v1, v2)

@dataclass
class Moon:
    pos : List[int]  = field(default_factory=list)
    vel : List[int]  = field (default_factory=list)

    def reset(self)->None:
        self.pos = self.starting_pos
        self.vel = [0] * len(self.pos)

    def __post_init__(self)->None:
        self.starting_pos = self.pos
        self.starting_vel  = [0] * len(self.pos)

    def _step_value(self, val: int, otherval: int) -> int:
        if  val < otherval:
            return 1
        elif val > otherval:
            return -1
        else:
            return 0

    def step_velocity(self, other : Moon) -> None:
        if not self.vel:
            self.vel : List[int] = [0] * len(self.pos)
        for i, v in enumerate(zip(self.pos, other.pos)):
            self.vel[i] += self._step_value(v[0], v[1])  
               
    def step_position(self) -> None:
        # apply deltas to velocity
        self.pos = [p + v for (p, v) in zip(self.pos, self.vel)]

@dataclass
class HeavenlyBody:
    celestials : List[Moon] = field(default_factory=list)
    def reset(self)-> None:
        for c in self.celestials:
            c.reset()

    def step(self) ->None:
        for c1,c2 in itertools.combinations(self.celestials, 2):
            c1.step_velocity(c2)
            c2.step_velocity(c1)
        for c in self.celestials:
            c.step_position()

    @property
    def energy(self) -> int:
        te = 0
        for m in self.celestials:
            pe = sum([abs(e) for e in m.pos])
            ke = sum([abs(e) for e in m.vel])
            te += pe * ke
        return te 

    def axis_repeats(self, idx : int) -> int:
        # all celestial bodies are at the same 
        # position and velocity along an axis 
        self.reset()
        initial_pairs =tuple((c.pos[idx], c.vel[idx]) for c in self.celestials) 

        step : int = 0
        while True:
            self.step()
            step += 1
            pairs = tuple((c.pos[idx], c.vel[idx]) for c in self.celestials)
            if pairs == initial_pairs:
                break

        print(pairs, initial_pairs)
        return step


    def repeats(self)-> int:
        naxis = 3
        rotations = [self.axis_repeats(i) for i in range(naxis)]
        print(rotations)
        return reduce(lcm, rotations)



# puzzle input
#<x=8, y=0, z=8>
#<x=0, y=-5, z=-10>
#<x=16, y=10, z=-5>
#<x=19, y=-10, z=-7>

def puzzle() -> None:
    m1 = Moon(pos=[8,0,8])
    m2 = Moon(pos=[0,-5,-10])
    m3 = Moon(pos=[16,10,-5])
    m4 = Moon(pos=[19,-10,-7])
    hb = HeavenlyBody([m1,m2,m3,m4])
    for i in range(1000):
        hb.step()
    print(hb.energy)

# Google about n-body Isochronous systems 
def puzzle2()-> int:
    #m1 : Moon = Moon([-1,0,2],[0,0,0])
    #m2 : Moon = Moon([2,-10,-7], [0,0,0])
    #m3 : Moon = Moon([4,-8,8],[0,0,0])
    #m4 : Moon = Moon([3,5,-1], [0,0,0])
    m1 = Moon(pos=[8,0,8])
    m2 = Moon(pos=[0,-5,-10])
    m3 = Moon(pos=[16,10,-5])
    m4 = Moon(pos=[19,-10,-7])
    #m1 = Moon(pos=[-8,-10,0])
    #m2 = Moon(pos=[5,5,10])
    #m3 = Moon(pos=[2,-7,3])
    #m4 = Moon(pos=[9,-8,-3])
    hb = HeavenlyBody([m1,m2,m3,m4])
    nrepeats = hb.repeats()
    return nrepeats


if __name__ == '__main__':
    puzzle()
    print(puzzle2())

