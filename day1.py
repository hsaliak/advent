from typing import List 
# measurements from 50 stars. Collect stars by solving puzzles. 
# two puzzles each day. Second unlocked when you complete teh first. 

# Fuel Counter-Upper

# Fuel is based on mass. 
# mass / 3 , round down, subtract two 


def fuel_cost(mass : int ) ->  int:
    cost  : int = (mass // 3)  - 2
    return cost

def fuel_requirement(mass : int) -> int:
    total : int = 0
    cost : int = mass
    while cost > 0:
        cost =  fuel_cost(cost)
        if cost > 0:
            total += cost
    return total

def total_fuel_requirement(modules : List[int]) -> int:
    return sum([fuel_requirement(m) for m in modules])

def read_module_weights(filename : str) -> List[int]:
    modules:  List[int] = []
    with open(filename) as f:
        modules = [int(s) for s in f.readlines()]
    return modules
        
if __name__ == '__main__':
    inputs : List[int] = read_module_weights("./input")
    fuel : int = total_fuel_requirement(inputs)
    print(fuel)
