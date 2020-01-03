# day 3 crossed wires
# on way to venus - fuel management system was not installed.
# two wires connected to central port extend outward on a grid
# they sometimes cross paths.
# find intersection point closest to central port
# use manhattan distance - sum of length of projectiosn
# d(p,q) == sum(x2 - x1, y2-y1)
# crossing at the central point where they start does not count


from typing import Tuple, List, Iterator, Set, Dict
from collections import namedtuple
from dataclasses import dataclass, field
import logging

logging.basicConfig(filename="day3.log", level=logging.DEBUG)


Point = namedtuple("Point", "x y")


def manhattan_distance(p: Point) -> int:
    dist : int = abs(p.x) + abs(p.y)
    return dist 


# general strategy, find all the points traversed, and then
# create a set of points for wire A , set of points for wire b
# find intersect points
# find minimum


def generate_points(steps: List[str], start: Point = Point(0, 0),) -> Iterator[Point]:
    for step in steps:
        step = step.strip()
        direction: str = step[0]
        scale: int = int(step[1:])
        if direction not in ("R", "U", "D", "L"):
            raise ValueError(f"expected {direction} to be one of R U D L")
        yield start
        if direction == "R":
            for i in range(1, scale):
                yield Point(start.x + i, start.y)
            start = Point(start.x + scale, start.y)
        elif direction == "L":
            for i in range(1, scale):
                yield Point(start.x - i, start.y)
            start = Point(start.x - scale, start.y)
        elif direction == "U":
            for i in range(1, scale):
                yield Point(start.x, start.y + i)
            start = Point(start.x, start.y + scale)
        else:  # D
            for i in range(1, scale):
                yield Point(start.x, start.y - i)
            start = Point(start.x, start.y - scale)


def parse_inputs(ins: Tuple[str, str]) -> Tuple[List[str], List[str]]:
    return (ins[0].split(","), ins[1].split(","))


def day3_i(fname: str) -> Tuple[str, str]:
    with open(fname) as f:
        lines = f.readlines()
        assert len(lines) == 2
    return (lines[0], lines[1])


day3inputs: Tuple[str, str] = day3_i("day3input")


@dataclass
class CircuitBoard:
    wseq1: str
    wseq2: str
    intersects: List[Point] = field(default_factory=list)
    first_wire: Dict[Point, int] = field(default_factory=dict)
    second_wire: Dict[Point, int] = field(default_factory=dict)

    def compute_signal_delay(self) -> Point:
        w1p = self.wseq1.split(",")
        w2p = self.wseq2.split(",")
        logging.debug(f"{w1p},{w2p}")

        for c, p in enumerate(generate_points(w1p)):
            if p not in self.first_wire:
                self.first_wire[p] = c

        for c, p in enumerate(generate_points(w2p)):
            if p not in self.second_wire:
                self.second_wire[p] = c

        wire_points1 = set(self.first_wire.keys())
        wire_points2 = set(self.second_wire.keys())
        self.intersects = sorted(
            wire_points1.intersection(wire_points2), key=lambda x: self.signal_delays(x)
        )
        return self.intersects[1]

    def signal_delays(self, p: Point) -> int:
        return self.first_wire[p] + self.second_wire[p]


def compute_dist(inputs: Tuple[str, str]) -> int:
    first_wire: Set[Point] = set(generate_points(parse_inputs(inputs)[0], Point(0, 0)))
    second_wire: Set[Point] = set(generate_points(parse_inputs(inputs)[1], Point(0, 0)))
    intersects = sorted(first_wire.intersection(second_wire), key=manhattan_distance)
    return manhattan_distance(intersects[1])


c = CircuitBoard(*day3inputs)
print(c.signal_delays(c.compute_signal_delay()))
