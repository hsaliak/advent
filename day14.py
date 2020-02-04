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
    print(f"ores from {ones}")
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
    if isbase(frm, chembook):
        return None
        
    for eq in chembook.values():
        if len(eq.lhs) == 1:
            if eq.lhs[0].elt == frm:
                return eq.rhs.elt
    return None

def compactEquation(es : List[Chem] , chembook : Dict[str, Equation]) -> List[Chem]:
    ce = es[:]
    cni =  { v.elt : i for i , v in enumerate(es)}
    elts = cni.keys()
    for c in elts:
        t = transforms(c, chembook) # t is what it transforms to 
        if t and t in cni: # so we can compact
            tidx = cni[t]
            cidx = cni[c]
            elt2c = reaction(es[tidx], chembook)[0] # this is the transforms to 
            ce[cidx].count += elt2c.count
            ce.pop(tidx)
            cni =  { v.elt : i for i , v in enumerate(ce)} # reset dict
            
    return ce # no early return


def addto(d : OrderedDict[str, int], k : str, v : int) -> None:
    if k in d:
        d[k] += v
    else:
        d[k] = v

def chain_reaction2( c : Chem, chembook : Dict[str, Equation] = {} ) -> int:
    """ does a chain reaction and returns the amount of ore required """ 
    chemicals : OrderedDict[str, int] = OrderedDict(((e.elt, e.count) for e in reaction(c, chembook)))
    while any(not isbase(x, chembook) for x in chemicals.keys()): 
        print(f" chemicals {chemicals} \n ")
        cname, counts = chemicals.popitem(last=False) # pop the first thing out 
        if isbase(cname, chembook ): # leave it alone
            chemicals[cname] = counts # reinsert
            continue
        else: # it's not a base chemicals, do a reaction
            
            base_chemicals = reaction(Chem(counts, cname), chembook) # get the reaction 
            print(base_chemicals)
            base_chemicals = compactEquation(base_chemicals, chembook )
            print(base_chemicals)
            
            for r in base_chemicals:
                #t : Optional[str] = transforms(r.elt, chembook) # we can break this down
                #if t:
                #    tchems = reaction(r, chembook)
                #    for tc in tchems:
                #        addto(chemicals, tc.elt, tc.count)
                #else:
                addto(chemicals, r.elt, r.count) # add to catalog
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
