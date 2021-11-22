from intcode import Memory, run_intcode
from util import draw_field
import math
from fractions import Fraction
import collections
from aocd import get_data, submit


day = 19
code = [int(i) for i in get_data(day=day).split(',')]
space = collections.defaultdict(lambda: collections.defaultdict(int))


k = Fraction(34, 35)
b = 3 - 4 * k
F = lambda x: k * x + b
Fshtrih = lambda y: (y - b) / k


def is_inside(x, y):
    prog = run_intcode(Memory(code))
    next(prog)
    prog.send(x)
    return prog.send(y) == 1

# 42936 32203 (True, True, False)
x = 4
y = 3
while True:
    if not is_inside(x, y):
        raise Exception('!')

    if is_inside(x + 1, y):
        x += 1
    elif is_inside(x, y + 1):
        y += 1
    elif is_inside(x + 1, y + 1):
        x += 1
        y += 1
    else:
        raise Exception('Empty around')

    if x > 100 and y > 100:
        res = (is_inside(x, y), is_inside(x - 100, y), is_inside(x - 100, y + 100))
        if set(res) == {True}:
            # submit((x - 100) * 10000 + y, day=day, part='b')
            print((x - 100) * 10000 + y)
            break
        else:
            print(x, y, res)



#vis_map = {
#    0: '.',
#    1: '#'
#}
#draw_field(space, vis_map)
#submit(count_pull, day=day, part='a')