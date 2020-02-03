from day14 import *
chembook  = {}

def test_day14inputs():
    cbook1 = parse_chembook("testinput")
    cbook2 = parse_chembook("testinput2")
    cbook3 = parse_chembook("testinput3")
    cbook4 = parse_chembook("testinput4")
    cbook5 = parse_chembook("testinput5")
    fuel = Chem(1, "FUEL")
    #chembook = cbook1
    #assert chain_reaction2(fuel, cbook1) == 31
    #chembook = cbook2
    #assert chain_reaction2(fuel, cbook2) == 165
    #chembook = cbook3
    #assert chain_reaction2(fuel, cbook3) == 13312
    #chembook = cbook4
    #assert chain_reaction2(fuel, cbook4) == 180697
    chembook = cbook5
    assert chain_reaction2(fuel, cbook5) == 2210736

