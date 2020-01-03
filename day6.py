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



def read_input(fname : str) -> Dict[str, str]:
    d = dict()
    with open(fname) as f :
        lines  : List[str] = f.readlines()
    for l in lines: 
        value, key = l.split(")")
        d[key.strip()] = value.strip()
    return d


def orbit_counts(celestial : str, orbits : Dict[str, str] = {})-> int:
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
    orbits : Dict[str,str] = dict()) -> Dict[str, int]:
    "return a dictionary of node:distance all the way to root"
    d : Dict[str, int]  = dict()
    count = 0
    try: 
        while celest: 
            celest = orbits[celest] 
            d[celest] = count
            count += 1
    except KeyError:
        return d
    return d


def traversal_count(c1 :str , 
    c2 : str, orbits : Dict[str,str] = dict()) -> int :
    "compute distance between two objects, which is the jumps reqd"
    d1 = orbital_distances(c1,orbits)
    d2 = orbital_distances(c2, orbits)
    combined = set(d1.keys()).intersection(set(d2.keys()))
    traversals = 0
    try:
        traversals = min(d1[c] + d2[c] for c in combined)
    except ValueError:
        print("no overlapping orbits")
    return traversals

def day6_1() -> None:
    orbs : Dict[str, str] = read_input("day6input")
    checksum = sum(orbit_counts(i, orbs ) for i in orbs.keys() )
    print(checksum)

def day6_2() -> None:
    orbs : Dict[str, str] = read_input("day6input")
    print(traversal_count("YOU", "SAN", orbs))

day6_1()
day6_2()
