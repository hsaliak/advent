from dataclasses import dataclass, field
from operator import attrgetter
from typing import List, Set
import math


@dataclass(eq=True, frozen=True, order=True)
class Point:
    x: float
    y: float


# unused
def unit_vector(p1: Point, p2: Point) -> Point:
    direction = Point(p2.x - p1.x, p2.y - p1.y)
    distance = math.sqrt(direction.x ** 2 + direction.y ** 2)
    unit: Point = Point(
        round(direction.x / distance, 4), round((direction.y / distance), 4)
    )
    return unit


@dataclass(eq=True, frozen=True, order=True)
class Target:
    angle: float
    magnitude: float

    def to_point(self, origin: Point) -> Point:
        xmag = round(math.sin(self.angle) * self.magnitude, 4)
        ymag = round(math.cos(self.angle) * self.magnitude, 4)
        return Point(origin.x + xmag, origin.y + ymag)


def target_from_point(dest: Point, origin: Point = Point(0, 0)) -> Target:
    dx = dest.x - origin.x
    dy = dest.y - origin.y
    magnitude = math.sqrt(dx ** 2 + dy ** 2)
    angle = math.atan2(dx, dy)  # angle from y axis
    return Target(angle, magnitude)


@dataclass
class Map:
    xlen: int
    ylen: int
    asteroids: Set[Point] = field(default_factory=set)

    def __str__(self) -> str:
        mapstr = ""
        for y in range(self.ylen):
            for x in range(self.xlen):
                if Point(x, y) in self.asteroids:
                    mapstr += "#"
                else:
                    mapstr += "."
            mapstr += "\n"
        return mapstr

    def visibles(self, p: Point, ignore: Set[Point]) -> Set[Target]:
        if p not in ignore:
            ignore.add(p)
        if p not in self.asteroids:
            raise ValueError(f"{p} not found in {self.asteroids}")
        others = set(self.asteroids)
        others.difference_update(ignore)
        targets: List[Target] = sorted((target_from_point(a, p) for a in others))
        visible_asteroids: Set[Target] = set()
        angles: Set[float] = set()
        for t in targets:
            if t.angle in angles:
                continue
            else:
                angles.add(t.angle)
                visible_asteroids.add(t)
        return visible_asteroids

    def sweep(self, p: Point) -> List[Target]:
        targets: List[Target] = list()
        ignore: Set[Point] = {p}
        sweep_targets = self.visibles(p, ignore=ignore)
        while sweep_targets:
            targets = targets + sorted(
                sweep_targets, key=attrgetter("angle"), reverse=True
            )
            ignore = set.union(ignore, (t.to_point(p) for t in sweep_targets))
            sweep_targets = self.visibles(p, ignore)
        return targets

    def viscount(self, p: Point) -> int:
        return len(self.visibles(p, set()))

    def max_visibles(self) -> int:
        return max(self.viscount(a) for a in self.asteroids)

    def station_location(self) -> Point:
        vcount: int = 0
        p: Point
        for a in self.asteroids:
            vc = self.viscount(a)  # how many
            if vc > vcount:
                vcount = vc
                p = a
        return p


def read_map(filename: str) -> Map:
    with open(filename) as f:
        lines = f.readlines()
    xlen: int = len(lines[0].strip())
    ylen: int = len(lines)
    asteroids: Set[Point] = set()
    for (y, line) in enumerate(lines):
        for (x, p) in enumerate(line):
            if p == "#":
                asteroids.add(Point(x, y))
    return Map(xlen, ylen, set(asteroids))


m: Map = read_map("day10input")
station = m.station_location()
print(station)
print(m.viscount(station))  # part 1
s = m.sweep(station)
p = s[199].to_point(station)
print(p.x * 100 + p.y)  # part 2
