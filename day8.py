import numpy as np
from typing import List, Tuple, Optional


def pixels_from_file(fname: str) -> List[int]:
    with open(fname) as f:
        line = f.readlines()[0]
    line = line.strip()
    vals = [int(v) for v in line]
    return vals


def to_pixels(l: List[int], width: int = 25, height: int = 6) -> np.ndarray:
    ar = np.array(l)
    ar.shape = (len(ar) // (width * height), width * height)
    return ar


def ones_and_twos_count(a: np.ndarray) -> int:
    count_ones = sum(a == 1)
    count_twos = sum(a == 2)
    return count_ones * count_twos


def zero_count(a: np.ndarray) -> int:
    return sum(a == 0)


def first_value(ars: np.ndarray) -> None:
    colcount = ars.shape[1]
    image = np.ndarray(150, dtype=int)
    for c in range(colcount):  # every element, every row, first column
        pcol = ars[:, c]
        image[c] = pcol[pcol != 2][0]
    image.shape = (6, 25)
    for i in range(0, 25, 5):
        print(image[:, i : i + 5])
        print("\n\n")


if __name__ == "__main__":
    vals = pixels_from_file("day8input")
    v = to_pixels(vals)
    zeros: Optional[int] = None
    zidx: Optional[int] = None
    for idx, elt in enumerate(v):
        rzero: int = zero_count(elt)
        if zeros is None or (rzero < zeros):
            zeros = rzero
            zidx = idx
    print(ones_and_twos_count(v[zidx]))
    first_value(v)
