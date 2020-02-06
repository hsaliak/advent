from __future__ import annotations # to type OrderedDict
from typing import Dict, Optional
from collections import deque, OrderedDict
from typing import Deque, List , Union
from dataclasses import dataclass, field
from math import ceil
from itertools import permutations
from heapq import heappush
import operator




@dataclass(order=True, eq = True)
class Chem:
    elt : str
    count : int 
    weight : Optional[int]  = None

    def get_weight(self, book : Dict[str, Equation]):
        if not self.weight:
            eq  : Equation = book[self.elt]
            if eq.isbase:
                self.weight = 1
            else:
                self.weight = sum(c.get_weight(book) for c in eq.lhs)  + 1
        return self.weight


@dataclass
class Equation:
    lhs : List[Chem]
    rhs : Chem

    @property 
    def isbase(self) -> bool:
        if len(self.lhs) == 1 and self.lhs[0].elt == "ORE":
            return True
        else:
            return False


def reaction( c : Chem, chembook : Dict[str, Equation] ) -> List[Chem]:
    """ if i want 2 WZLFW, i will need 36 QNWRZ and 14 RLFSK """ 
    num = c.count # 10 A , so i look for A 
    elt = c.elt
    equation : Equation  = chembook[elt] # rhs is the 2A or 5A or similar, i want 10A
    nreactions : int  = 0
    nreactions =  ceil(num/equation.rhs.count )  # 10 / 2 is 5 so i run the equation 5 times
    chems =  [Chem(c.elt, c.count * nreactions) for c in equation.lhs]  # c
    if not equation.isbase:
        chems.sort(key=operator.methodcaller('get_weight', chembook))
    return chems

def isore(c : Chem) -> bool:
    return c.elt == "ORE"

def isbase(s : str, chembook : Dict[str, Equation]) -> bool:
    return chembook[s].isbase

def orecount(ones : Dict[str, int], chembook : Dict[str, Equation])-> int:
    amt : int = 0
    assert len(ones) == len(set(ones.keys()))
    for chemical, count  in ones.items():
        base_chemicals = reaction(Chem(chemical, count), chembook )
        if  len(base_chemicals) != 1 or not isore(base_chemicals[0]):
            raise ValueError(f"{chemical} cannot be derived from ore")
        amt += ceil(base_chemicals[0].count)
    return amt 

def addto(chemicals : List[Chem], c : Chem) -> None:
    eltidx = {x.elt: idx for idx, x in enumerate(chemicals)}
    if c.elt in eltidx:
        chemicals[eltidx[c.elt]].count += c.count
    else:
        chemicals.append(c)

def chain_reaction2( c : Chem, chembook : Dict[str, Equation] = {} ) -> int:
    """ does a chain reaction and returns the amount of ore required """ 
    chemicals = reaction(c, chembook)
    basechems : Dict[str, int] =  {}
    while chemicals: 
        c = chemicals.pop()
        if isbase(c.elt, chembook):
            if c.elt not in basechems:
               basechems[c.elt] = c.count
            else:
                basechems[c.elt] += c.count
        else: # it's not a base chemicals, do a reaction
            base_chemicals = reaction(c , chembook)  # this is sorted now
            for r in base_chemicals:
                addto(chemicals, r)
            chemicals.sort(key=operator.methodcaller('get_weight', chembook))
    return  orecount(basechems, chembook)

def parse_chembook(fname : str) -> Dict[str, Equation]:
    with open(fname) as f:
        lines : List[str] = f.readlines()
    chembook = {}
    for l in lines:
        lhsstr, rhsstr = l.split("=>")
        rhscounts, rhschem = rhsstr.strip().split(" ")
        rhs = Chem(rhschem, int(rhscounts))
        lhs = []
        reagents = lhsstr.split(",")
        for p in reagents:
            count, cname = p.strip().split(" ")
            chem = Chem(cname, int(count))
            lhs.append(chem)
        # now we are ready to append to the dictionary
        chembook[rhs.elt] = Equation(lhs, rhs)
    return chembook


    
if __name__ == '__main__':
    chembook = parse_chembook("day14input")
    c = Chem("FUEL", 1)
    print(chain_reaction2(c, chembook))
