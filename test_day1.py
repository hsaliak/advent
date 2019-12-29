from day1 import *


def test_fuel_cost():
    assert 2 == fuel_cost(12)
    assert 2 == fuel_cost(14)
    assert 654 == fuel_cost(1969)
    assert 33583 == fuel_cost(100756)


def test_fuel_requirement():
    assert 966 == fuel_requirement(1969)
    assert 50346 == fuel_requirement(100756)
