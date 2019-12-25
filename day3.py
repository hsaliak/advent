# day 3 crossed wires 
# on way to venus - fuel management system was not installed.
# two wires connected to central port extend outward on a grid 
# they sometimes cross paths. 
# find intersection point closest to central port
# use manhattan distance - sum of length of projectiosn 
# d(p,q) == sum(x2 - x1, y2-y1)
# crossing at the central point where they start does not count



from typing import Tuple, List, Generator, Set
from collections import namedtuple


Point = namedtuple('Point', 'x y')
def manhattan_distance(p : Point):
    return abs(p.x) + abs(p.y)


# general strategy, find all the points traversed, and then 
# create a set of points for wire A , set of points for wire b 
# find intersect points
# find minimum


def generate_points(steps : List[str], start : Point, ) -> Generator[Point, None,None]:
    #yield start
    for step in steps:
        step = step.strip()
        direction : str = step[0]
        scale : int = int(step[1:])
        if direction not in ('R', 'U', 'D', 'L'):
           return 
           # raise ValueError(f"expected {direction} to be one of R U D L")
        if direction == 'R':
            for i in range(1, scale):
                yield Point(start.x + i, start.y)
            start = Point(start.x + scale, start.y)
        elif direction == 'L':
            for i in range(1, scale):
                yield Point(start.x - i, start.y)
            start = Point(start.x - scale, start.y)
        elif direction == 'U':
            for i in range(1, scale):
                yield Point(start.x , start.y + i)
            start = Point(start.x , start.y + scale)
        else: # D
            for i in range(1, scale):
                yield Point(start.x , start.y - i)
            start = Point(start.x , start.y - scale)
        

inputs : Tuple[str, str] = ('R75,D30,R83,U83,L12,D49,R71,U7,L72',
    'U62,R66,U55,R34,D71,R55,D58,R83')

def parse_inputs(ins : Tuple[str, str]) ->  Tuple[List[str], List[str]]:
   return (ins[0].split(','), ins[1].split(','))

def day3_i(fname : str) -> Tuple[str,str]:
    with  open(fname) as f :
        lines = f.readlines()
        assert len(lines) == 2 
    return (lines[0], lines[1])

day3inputs : Tuple [str, str]  = day3_i('day3input')

first_wire : Set[Point] = set(generate_points(parse_inputs(inputs)[0], Point(0,0)))
second_wire : Set[Point] = set(generate_points(parse_inputs(inputs)[1], Point(0,0)))
intersects = sorted(first_wire.intersection(second_wire), key=manhattan_distance)
print(intersects[0], manhattan_distance(intersects[0]))
    
fw : Set[Point] = set(generate_points(parse_inputs(day3inputs)[0], Point(0,0)))
sw  : Set[Point] = set(generate_points(parse_inputs(day3inputs)[1], Point(0,0)))
cross = sorted(fw.intersection(sw), key=manhattan_distance)
print(cross[0], manhattan_distance(cross[0]))

