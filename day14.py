from __future__ import annotations # to type OrderedDict
from typing import Dict, Optional
from collections import deque, OrderedDict
from typing import Deque, List , Union
from dataclasses import dataclass
from math import ceil
from itertools import permutations



base : str = 'ORE'


@dataclass
class Chem:
    count : int 
    elt : str

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
    chems =  [Chem(c.count * nreactions, c.elt) for c in equation.lhs]  # c
    return chems



def isore(c : Chem) -> bool:
    return c.elt == "ORE"

def isbase(s : str, chembook : Dict[str, Equation]) -> bool:
    return chembook[s].isbase

def orecount(ones : Dict[str, int], chembook : Dict[str, Equation])-> int:
    amt : int = 0
    #print(f"ores from {ones}")
    assert len(ones) == len(set(ones.keys()))
    for chemical, count  in ones.items():
        base_chemicals = reaction(Chem(count, chemical), chembook )
        if  len(base_chemicals) != 1 or not isore(base_chemicals[0]):
            raise ValueError(f"{chemical} cannot be derived from ore")
        amt += ceil(base_chemicals[0].count)
    print(amt)
    return amt 
    
def isreagent(c: str, e : Equation) -> bool:
    reagents = set(x.elt for x in e.lhs)
    if c in reagents:
        return True
    return False

def transforms(frm : str, chembook: Dict[str, Equation] ) -> Optional[str]:
    for eq in chembook.values():
        if len(eq.lhs) == 1:
            if eq.lhs[0].elt == frm:
                return eq.rhs.elt
    return None

def decompose(to : str, chembook : Dict[str, Equation]) -> Optional[str]:
    eq = chembook[to]
    if len(eq.lhs) == 1 and eq.lhs[0].elt != "ORE":
        return eq.lhs[0].elt
    return None

def compactEquation(es : List[Chem] , chembook : Dict[str, Equation]) -> List[Chem]:
    # for each item in the equation, check if it can be transformed into another present
    # if it can be, then remove it from the list and add it. 
    # maybe do an ordered Dict of Key and Value
    esd : OrderedDict[str, int]  = OrderedDict()
    for x in es:
        if x.elt in esd:
            esd[x.elt] += x.count
        else:
            esd[x.elt] = x.count
    esdi = esd.copy()
    for e in esdi.keys():
        if e == "ORE":
            print("here is some ore ")
            continue
        t = decompose(e, chembook)
        if t and t in esd: # so we can compact
            print(f"compacting {es} by decomposing {e} to  {t}")
            reagent = reaction(Chem(esd[e], e), chembook)[0] 
            print(reagent.elt, e, ":", t)
            esd[reagent.elt] += reagent.count # bmbpt
            esd.pop(e) # get rid of it  -- this now has bmbt only
            print(esd)
            return compactEquation([Chem(v,k) for k,v in esd.items()], chembook)
            
    return [Chem(v,k) for k,v in esd.items()] 


def addto(chemicals : List[Chem], c : Chem) -> None:
    if c in chemicals:
        chemicals[chemicals.index(c)].count += c.count
    else:
        chemicals.append(c)

def chain_reaction2( c : Chem, chembook : Dict[str, Equation] = {} ) -> int:
    """ does a chain reaction and returns the amount of ore required """ 
    chemicals = reaction(c, chembook)
    chemicals = compactEquation(chemicals, chembook) # compact the equation
    basechems : Dict[str, int] =  {}
    oreamt = 0
    while  chemicals: 
        c = chemicals.pop()
        if isore(c): # leave it alone
            oreamt += c.count
        elif isbase(c.elt, chembook):
            if c.elt not in basechems:
                basechems[c.elt] = c.count
            else:
                basechems[c.elt] += c.count
        else: # it's not a base chemicals, do a reaction
            base_chemicals = reaction(c , chembook) 
            base_chemicals = compactEquation(base_chemicals, chembook )
            for r in base_chemicals:
                if isore(r):
                    oreamt += r.count
                else:
                    chemicals.append(r)
                    chemicals = compactEquation(chemicals, chembook)
    return oreamt + orecount(basechems, chembook)

def parse_chembook(fname : str) -> Dict[str, Equation]:
    with open(fname) as f:
        lines : List[str] = f.readlines()
    chembook = {}
    for l in lines:
        lhsstr, rhsstr = l.split("=>")
        rhscounts, rhschem = rhsstr.strip().split(" ")
        rhs = Chem(int(rhscounts), rhschem)
        lhs = []
        reagents = lhsstr.split(",")
        for p in reagents:
            count, cname = p.strip().split(" ")
            chem = Chem(int(count), cname)
            lhs.append(chem)
        # now we are ready to append to the dictionary
        chembook[rhs.elt] = Equation(lhs, rhs)
    return chembook

    
if __name__ == '__main__':
    fuel : Chem = Chem(1, "FUEL")
    chembook = parse_chembook("testinput5")
    amt = chain_reaction2(fuel, chembook)
    print(f"final {amt}")
