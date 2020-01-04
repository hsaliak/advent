from machine import Machine
from typing import List, Iterable, Tuple
from collections import deque
import itertools


def read_input(fname: str) -> List[int]:
    with open(fname) as f:
        line = f.read()
    return [int(i.strip()) for i in line.split(",")]


class Thruster:
    amplifiers: List[Machine]
    num_amps = 5

    def __init__(self, control_code: List[int]):
        self.amplifiers: List[Machine] = []
        for i in range(self.num_amps):
            self.amplifiers.append(Machine(control_code, []))

    def thruster_signal(self, phases: List[int]) -> int:
        p = list(reversed(phases))
        signal: int = 0
        if len(p) != self.num_amps:
            raise ValueError(f"expected {self.num_amps} amplifiers, got {len(p)}")
        for a in self.amplifiers:
            a.io = deque([p.pop(), signal])
            a.process()
            signal = a.io.pop()
        return signal


def thruster_signal(codes: List[int], sequence: List[int]) -> int:
    t = Thruster(codes)
    return t.thruster_signal(sequence)


signal_permutations: Iterable[Tuple[int, ...]] = itertools.permutations(range(0, 5), 5)


def max_signal(
    t: Thruster, perms: Iterable[Tuple[int, ...]] = signal_permutations
) -> int:
    max = 0
    maxperm: Tuple[int, ...]
    for p in perms:
        sig = t.thruster_signal(list(p))
        if sig > max:
            max = sig
            maxperm = p
    print(maxperm)
    return max


if __name__ == "__main__":
    codes: List[int] = read_input("day7input")
    t = Thruster(codes)
    print(max_signal(t))

