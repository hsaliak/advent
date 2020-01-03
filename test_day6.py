from day6 import *
orbits = {}
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
#orbits["YOU"] = "K"
#orbits["SAN"] = "I"

def test_day61():
    assert  sum(orbit_counts(i, orbits) for i in orbits.keys()) == 42

def test_day62():
    orbits_with_santa  = dict(orbits)
    orbits_with_santa["YOU"] = "K"
    orbits_with_santa["SAN"] = "I"
    assert traversal_count("YOU","SAN", orbits_with_santa) == 4

