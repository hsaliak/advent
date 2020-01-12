from machine import Machine
from typing import List, Iterable, Tuple, Sequence
from collections import deque
import itertools
import logging

logging.basicConfig(filename="day7.log", level=logging.DEBUG)


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

    def restart(self) -> None:
        for a in self.amplifiers:
            a.restart()

    def thruster_signal(self, phases: Sequence[int], restart: bool = True) -> int:
        if restart:
            self.restart()
        p = list(reversed(phases))
        signal: int = 0
        if len(p) != self.num_amps:
            raise ValueError(f"expected {self.num_amps} amplifiers, got {len(p)}")
        for a in self.amplifiers:
            a.io = deque([p.pop(), signal])
            a.process()
            signal = a.io.pop()
        # logging.debug(f"{phases}, {signal}")
        return signal

    def feedback_loop(self, phases: Sequence[int], restart: bool = True) -> int:
        if restart:
            self.restart()
        e: Machine = self.amplifiers[self.num_amps - 1]
        # set phases - first input instruction is the phase.
        # subsequent are signals
        p = list(reversed(phases))
        for a in self.amplifiers:
            a.io.append(p.pop())

        signal: int = 0
        while not e.halted:
            for a in self.amplifiers:
                a.io.append(signal)  # assume that its only linear forwarding
                if a.halted:
                    continue  # skip this amp
                # a.io.append(signal) # add the existing signal
                a.process()
                signal = a.io.popleft()  # grab the io from the back
        # logging.debug(f"{phases}, {signal}")
        return signal


signal_permutations: List[Tuple[int, ...]] = list(
    itertools.permutations(range(0, 5), 5)
)


def max_signal(
    t: Thruster, perms: Iterable[Tuple[int, ...]] = signal_permutations
) -> int:
    max = 0
    maxperm: Tuple[int, ...] = (0, 0, 0, 0, 0)
    for p in perms:
        sig = t.thruster_signal(list(p))
        if sig > max:
            max = sig
            maxperm = p
    return max


# output of E is connected back to A
# phase settings go from 5 to 9
# repeatedly take the input
# produce output many times before halting.
# start with the first input instruction, the rest  are for later.
# do not restart the amplifiers.
# continue receiving and sending signals until it halts.
# signals will be between pairs of amplifiers
# very first one is 0 to A
# last one is pulled from E
# find the largest signal from E

# an amplifier halts when it hits 99

feedback_permutations: List[Tuple[int, ...]] = list(
    itertools.permutations(range(5, 10), 5)
)


def max_feedback(t: Thruster) -> int:
    mf = 0
    for p in feedback_permutations:
        feedback = t.feedback_loop(p)
        if feedback > mf:
            mf = feedback
    return mf


example_codes: List[int] = [
    3,
    26,
    1001,
    26,
    -4,
    26,
    3,
    27,
    1002,
    27,
    2,
    27,
    1,
    27,
    26,
    27,
    4,
    27,
    1001,
    28,
    -1,
    28,
    1005,
    28,
    6,
    99,
    0,
    0,
    5,
]

if __name__ == "__main__":
    codes: List[int] = read_input("day7input")
    t = Thruster(codes)
    print(max_feedback(t))
