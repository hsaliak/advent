import enum
import math
from dataclasses import dataclass, field
from collections import deque
from typing import Dict, DefaultDict, Optional
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

s = Robot(Point(0,0), turn, 1.0)


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

def paint() -> None:
    m = machine.Machine(get_intcodes("day11input"))
    pos : Point = Point(0,0)
    r = Robot(Point(0,0), turn, 1.0)
    c = Canvas()
    m.io = deque([c.color(pos)])
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
            break
    print(c.painted_grids)


paint()

