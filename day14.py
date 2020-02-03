from __future__ import annotations # to type OrderedDict
from typing import Dict
from collections import deque, OrderedDict
from typing import Deque, List , Union
from dataclasses import dataclass
from math import ceil



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
    assert len(ones) == len(set(ones.keys()))
    for chemical, count  in ones.items():
        base_chemicals = reaction(Chem(count, chemical), chembook )
        if  len(base_chemicals) != 1 or not isore(base_chemicals[0]):
            raise ValueError(f"{chemical} cannot be derived from ore")
        amt += ceil(base_chemicals[0].count)
    print(amt)
    return amt 
    
    
def chain_reaction2( c : Chem, chembook : Dict[str, Equation] = {} ) -> int:
    """ does a chain reaction and returns the amount of ore required """ 
    chemicals : OrderedDict[str, int] = OrderedDict(((e.elt, e.count) for e in reaction(c, chembook)))
    #oneoffs : Dict[str, int]  = {}
    while any(not isbase(x, chembook) for x in chemicals.keys()): 
        print(f" chemicals {chemicals} \n ")
        cname, counts = chemicals.popitem(last=False) # pop the first thing out 
        if isbase(cname, chembook ): # leave it alone
            chemicals[cname] = counts # reinsert
            continue
            #if cname in oneoffs:
            #    oneoffs[cname] += counts
            #else:
            #    oneoffs[cname] = counts
        else:
            base_chemicals = reaction(Chem(counts, cname), chembook) # get the reaction 
            for r in base_chemicals:
                if r.elt in chemicals: # 
                    chemicals[r.elt] += r.count
                else:
                    chemicals[r.elt] = r.count # insert into the ordered dictionary 
    # now its all base chemicals
    return orecount(chemicals, chembook)

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
    print(amt)
