from __future__ import annotations # so that i can have forward ref
import itertools 
from typing import List  
from dataclasses import dataclass, field 

@dataclass
class Moon:
    pos : List[int]  = field(default_factory=list)
    vel : List[int]  = field (default_factory=list)

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
    def step(self):
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


# puzzle input
#<x=8, y=0, z=8>
#<x=0, y=-5, z=-10>
#<x=16, y=10, z=-5>
#<x=19, y=-10, z=-7>

def puzzle():
    m1 = Moon(pos=[8,0,8])
    m2 = Moon(pos=[0,-5,-10])
    m3 = Moon(pos=[16,10,-5])
    m4 = Moon(pos=[19,-10,-7])
    hb = HeavenlyBody([m1,m2,m3,m4])
    for i in range(1000):
        hb.step()
    print(hb.energy)

if __name__ == '__main__':
    puzzle()

