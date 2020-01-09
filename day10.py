from dataclasses import dataclass,  field
from typing import List, Set
import math




@dataclass(eq=True, frozen=True, order=True)
class Point:
    x : float
    y : float

def unit_vector(p1 : Point, p2 : Point) -> Point:
    direction = Point(p2.x - p1.x, p2.y - p1.y)
    distance = math.sqrt(direction.x ** 2 + direction.y **2 )
    unit : Point = Point(round(direction.x / distance, 4), round((direction.y / distance), 4))
    return unit


@dataclass
class Map:
    xlen : int
    ylen : int
    asteroids : Set[Point] = field(default_factory=set)

    def __str__(self) -> str :
        mapstr = ''
        for y in range(self.ylen):
            for x in range(self.xlen):
                if Point(x,y) in self.asteroids:
                    mapstr += '#'
                else:
                    mapstr += '.'
            mapstr += '\n'
        return mapstr

    def visibles(self, p : Point) -> Set[Point]:
        if p not in self.asteroids:
            raise ValueError(f"{p} not found in {self.asteroids}")
        
        others = set(self.asteroids)
        others.discard(p)
        units : Set[Point] = set()
        for a in others:
            units.add(unit_vector(a, p))

        #print(f"{p}:  {len(units)}")
        return units

    def viscount(self, p : Point) -> int:
        return len(self.visibles(p))

    def max_visibles(self)->int:
        return max(self.viscount(a) for a in self.asteroids)

    def station_location(self) -> Point:
        vcount : int = 0
        p : Point
        for a in self.asteroids:
            visibles : Set[Point] = self.visibles(a)
            if len(visibles) > vcount:
                vcount = len(visibles)
                p = a
        return a      

def angle(p :Point):
    return math.atan2(p.y, p.x) # we want to measure against y axis
            

def read_map(filename : str) -> Map:
    with open(filename) as f:
        lines = f.readlines()
    xlen : int = len(lines[0].strip())
    ylen : int = len(lines)
    asteroids : Set[Point] = set()
    for (y, line) in enumerate(lines):
        for(x, p) in enumerate(line):
            if  p == '#':
                asteroids.add(Point(x,y))
    return Map(xlen, ylen, set(asteroids))


m : Map = read_map("day10test")
#print(m)
#print(m.visibles(Point(x=1, y = 0)))
print(m.max_visibles())
station = m.station_location()

vectors =  sorted((a for a in m.visibles(station)), key = angle)
print(vectors)

