from machine import Machine
from day5 import get_intcodes


day9input = get_intcodes("day9input")

m = Machine(day9input, [1])

while not m.halted:
    m.process()
    print(m.io)

print(m.io.pop())
m2 = Machine(day9input, [2])
while not m2.halted:
    m2.process()
print(m2.io)

