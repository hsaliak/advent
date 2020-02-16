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


def day1( b : Dict[str, Equation] ) -> None:
    #c = Chem("FUEL", 82892753)
    c = Chem("FUEL", 1)
    chain_reaction2(c, b)

def day2( maxore : int, b : Dict[str, Equation]) -> None:
    """ find the amount of FUEL that can be produced from 1t ore """ 
    findmaxfuel(b)
    # we double the number of fuel produced each time until the number
    # if the ore needed is less than 1 trillion 
    # we double the number of produced
    # if it is greater than 1 trillion
    # take the last value less than 1 trillion and current and average
    # the number of fuel and see what we get. 
      

def findmaxfuel(b : Dict[str, Equation]) -> int:

    # find the maximum amount of fuel that can be produced by 1t ore
    # we do this by doubling the amount of fuel produced. 
    # this is the lower bound
    # until we use more than 1 trillion ore.  this is the upper bound
    # once we have an upper and lower bound. 
    # we get midpoint. 
    # if the ore needed is > 1 trillion, we update upper bound with mp
    # if the ore needed is < 1 trillion we update lower bound with 1t
    # if upperbound - lowerbound = 1, we return the value of lower bound
    trillion : int = 1000000000000
    lowerbound : int  = 1
    upperbound : Optional[int] = None
    while (not upperbound) or ((upperbound - lowerbound) > 1):
        if upperbound:
            count = (lowerbound + upperbound) //2  # find avg
        else:
            count = lowerbound
        c = Chem("FUEL", count) 
        oreneeded = chain_reaction2(c, b)
        if oreneeded < trillion:
            if upperbound: # move up lower bound
                lowerbound = count
            else: 
                lowerbound = lowerbound * 2  #
        elif oreneeded > trillion: # overshot, 
            if not upperbound:
                lowerbound = count // 2
            upperbound = count  # bring in upper bound
        else: # found it 
            return c.count
    print(f"L{lowerbound}: U{upperbound} ore => {oreneeded} delta => {oreneeded - trillion}")
    return lowerbound
    


if __name__ == '__main__':
    chembook = parse_chembook("day14input")
    day1(chembook)
    trillion : int = 1000000000000
    day1(chembook)
    day2(trillion, chembook)
