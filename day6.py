# landed on the moon 
# map of local orbit inputs is the puzzle input

# every object is an orbit around 1 other object. 
# AAA) BBB   or AAA : BBB  (BBB is in orbit around AAA)
# to verify this that the object is not corrupted, you need to do 
# checksums. 
# total number of direct orbits and indirect orbits. 
# A orbits B and B orbits C then A indirectly orbits C 
# like earth ) moon,  sun ) earth then sun ) moon 


from typing import Dict, DefaultDict, Optional, List
from collections import defaultdict
from functools import lru_cache

orbits : Dict[str, str] = {}

orbits["B"] = "COM"
orbits["C"] = "B"
orbits["D"] = "C"
orbits["E"] = "D"
orbits["F"] = "E"
orbits["G"] = "B"
orbits["H"] = "G"
orbits["I"] = "D"
orbits["J"] = "E"
orbits["K"] = "J"
orbits["L"] = "K"
orbits["YOU"] = "K"
orbits["SAN"] = "I"


def read_input(fname : str) -> Dict[str, str]:
    d = dict()
    with open(fname) as f :
        lines  : List[str] = f.readlines()
    for l in lines: 
        value, key = l.split(")")
        d[key.strip()] = value.strip()
    return d

orbits = read_input("day6input") # override test data


@lru_cache(10, typed=True)
def orbit_counts(celestial : str, d : Dict[str, str] = orbits)-> int:
    "return a count of distance to root node"
    count = 0
    try: 
        while celestial:
            celestial = orbits[celestial]
            count += 1
    except KeyError:
        return count
    return count


def orbital_distances(celest: str, 
    orbits : Dict[str,str] = orbits) -> Dict[str, int]:
    "return a dictionary of node:distance all the way to root"
    d : Dict[str, int]  = dict()
    count = 0
    c : Optional[str] = celest
    while c:
        c  = orbits.get(c)
        if c:
            d[c] = count  
            count += 1
        else: 
            break
    return d


def traversal_count(c1 :str , 
    c2 : str, orbits : Dict[str,str] = orbits) -> int :
    "compute distance between two objects, which is the jumps reqd"
    d1 = orbital_distances(c1)
    d2 = orbital_distances(c2)
    combined = set(d1.keys()).intersection(set(d2.keys()))
    traversals = min(d1[c] + d2[c] for c in combined)
    return  traversals
    
checksum = sum(orbit_counts(i) for i in orbits.keys() )
print(traversal_count("YOU", "SAN"))
