from day2 import * 
if __name__ == '__main__':
    intcodes = get_intcodes('day2input')
    day2_1(intcodes[:], 12,2)
    out = -1
    vs = day2_2(intcodes[:])
    print(vs)
