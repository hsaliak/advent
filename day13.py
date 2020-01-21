from typing import List, Iterable, Deque, Optional
from dataclasses import dataclass
import machine
from enum import IntEnum
from collections import deque
import array


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

    def from_triple(self,  triple : List[int])-> 'Position':
        if len(triple) != 3:
            raise ValueError(f"expected iterable of len 3, got iterable of length {len(triple)}")
        x, y, tile = triple
        return Position(x, y, Tile(tile))


class Movement(IntEnum):
    LEFT = -1
    RIGHT = 1
    NEUTRAL = 0

class Cabinet:
    m : machine.Machine # supply an initialized machine
    gamecodes : List[int] 
    joystick : 'Joystick'
    def __init__(self, gamecodes : List[int] = arcade_game)->None:
        self.m = machine.Machine(gamecodes, [])
        self.gamecodes = gamecodes
        self.m.restart()
        self.joystick = Joystick(self)
        self.m.attach(self.joystick)


    def gameloop(self) -> None:
        m : machine.Machine= self.m
        m.restart()
        m.intcodes[0] = 2
        m.io = deque([])
        while not m.halted:
            ios : List[int]
            m.process() 
            # see if the score needs to be printed
    
    def display(self, clear : bool  = True) -> None:
        output : List[int] =  list(self.m.io)
        ncols : int  = max(output[0::3]) +1  # zero idx
        nrows : int = max(output[1::3]) +1  # zero idx 
        # build a char array of tiles
        tiles : array.array[int] = array.array('b', [0] * (nrows * ncols))
        score : Optional[int] = None 
        empty_tile = int.from_bytes(b' ', byteorder='little')
        wall_tile = int.from_bytes(b'W', byteorder='little')
        block_tile = int.from_bytes(b'.', byteorder='little')
        paddle_tile = int.from_bytes(b'-', byteorder='little')
        ball_tile = int.from_bytes(b'o', byteorder='little')

        for i in range(0, len(output), 3):
            col = output[i]
            row = output[i+1]
            tile = output[i+2]
            if col == -1 and row == 0:
                score = tile
                continue
            if tile ==  Tile.EMPTY:
                tiles[row * ncols + col] =  empty_tile
            elif tile == Tile.WALL:
                tiles[row * ncols + col] = wall_tile
            elif tile == Tile.BLOCK:
                tiles[row * ncols + col] =   block_tile
            elif tile == Tile.HPADDLE:
                tiles[row * ncols + col] =  paddle_tile
            elif tile == Tile.BALL:
                tiles[row * ncols + col] =  ball_tile

        for i in range(0, nrows):
            print(tiles[i*ncols: (i+1) *ncols].tobytes().decode())

        if score:
            print(f"SCORE {score}")

        if clear:
            self.m.io.clear()

    def count_blocks(self)->int:
        self.m.restart()
        while not self.m.halted:
            self.m.process()
        res : List[int] = list(self.m.io)
        tiles = res[2::3]
        return tiles.count(Tile.BLOCK) 

@dataclass
class Joystick(machine.InputPeripheral):
    c : Cabinet
    def get_input(self) -> Movement:
        while True:
            try:
                i : str = input()
                if i not in 'jkl':
                    raise ValueError
                if i == 'j':
                   return  Movement.LEFT
                elif i == 'k':
                    return Movement.NEUTRAL
                else: 
                    return Movement.RIGHT 
            except ValueError:
                print(f"{i} is an invalid input, try again")

    def get(self) -> int:
        self.c.display(clear=False)
        return int(self.get_input())

if __name__ == '__main__':
    c : Cabinet = Cabinet()
    #nblocks : int = c.count_blocks()
    c.gameloop()


        
