from typing import List, Iterable, Deque
from dataclasses import dataclass
import machine
from enum import IntEnum


arcade_game : List[int] = machine.get_intcodes("day13input")

class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HPADDLE  = 3 # indestructible
    BALL = 4

@dataclass 
class Position:
    x : int # position from the left 
    y : int # position from the top -- 0, 0 is top left.
    t : Tile 

    def from_triple(self,  triple : List[int]):
        if len(triple) != 3:
            raise ValueError(f"expected iterable of len 3, got iterable of length {len(triple)}")
        x, y, tile = triple
        return Position(x, y, Tile(tile))

@dataclass
class Cabinet:
    m : machine.Machine # supply an initialized machine
    def __post_init__(self):
        m.restart()

    def run_game(self) -> List[int]:
        while not m.halted:
            m.process()
        output = list(m.io)
        return output
   
    def count_blocks(self)->int:
        res : List[int] = self.run_game()
        tiles = res[2::3]
        return tiles.count(Tile.BLOCK) 

if __name__ == '__main__':
    gamecode : List[int]= machine.get_intcodes("day13input")
    m : machine.Machine= machine.Machine(gamecode, [])
    c : Cabinet = Cabinet(m)
    nblocks : int = c.count_blocks()
    print(nblocks)


        
