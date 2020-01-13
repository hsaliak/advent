import enum
import math
from dataclasses import dataclass, field
from collections import deque
from typing import Dict, DefaultDict, Optional, List
import machine
from day5 import get_intcodes


@dataclass(eq=True, frozen=True, order=True)
class Point:
    x: float
    y: float

turn = { 0: -90 * math.pi/180, 1 : 90 * math.pi/180}

@dataclass
class Robot:
    position : Point 
    turn : Dict[int, float] = field(default_factory=dict)
    magnitude : float = 1.0
    angle : float = 0
    def move(self ) -> None:
        xmag = round(math.sin(self.angle) * self.magnitude, 4)
        ymag = round(math.cos(self.angle) * self.magnitude, 4)
        self.position = Point(self.position.x + xmag, self.position.y + ymag)

    def step(self, turn_input : int,   magnitude : float= 1.0) -> Point:
        angle : float = self.turn[turn_input]
        self.angle = angle + self.angle
        self.move()
        return self.position

class Color(enum.IntEnum):
    BLACK = 0
    WHITE = 1


@dataclass
class Canvas:
    canvas : Dict[Point, Color] = field(default_factory=dict)

    def color(self, p : Point) -> int:
        return int(self.canvas.get(p, Color.BLACK))

    def paint(self, p : Point, c : Color) -> Color:
            self.canvas[p] = c 
            return c 

    @property
    def painted_grids(self) -> int:
        return len(self.canvas)

    def painted(self, p : Point)-> bool:
        return p in self.canvas

def paint(start_color : Optional[int]= None) -> Dict[Point,Color]:
    m = machine.Machine(get_intcodes("day11input"))
    pos : Point = Point(0,0)
    r = Robot(Point(0,0), turn, 1.0)
    c = Canvas()
    if start_color:
        print(Color(start_color))
        c.paint(pos,Color(start_color))
    m.io = deque([c.color(pos)]) #
    while not m.halted:
        try:
            m.process() # compute color
            color = Color(m.io.popleft()) # what is the color to paint
            c.paint(pos, color)
            m.process() # compute turn
            tur = m.io.popleft()
            pos =  r.step(tur)
            m.io.append(c.color(pos))
        except IndexError:
            print("index error")
            break
    print(c.painted_grids)
    return c.canvas


from matplotlib import pyplot as plt
def display(d : Dict[Point, Color]):
    xs  = []
    ys  = []
    xb  = []
    yb  = []
    for (p, v) in d.items():
        if v == Color.WHITE:
            xs.append(p.x)
            ys.append(p.y)
        if v == Color.BLACK:
            xb.append(p.x)
            yb.append(p.y)

    plt.xlim(-20,50)
    plt.ylim(-20,20)
    plt.plot(xs,ys, 'rx-' )
    plt.plot(xb,yb, 'wo-' )
    plt.savefig('11_2.png')

points = paint(start_color=1)
display(points)



