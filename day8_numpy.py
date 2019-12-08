from aocd import get_data
import itertools
import numpy as np
from collections import defaultdict
from aocd import submit

"""
Inspired by https://github.com/wimglenn/advent-of-code-wim/blob/master/aoc_wim/aoc2019/q08.py
"""

day = 8
w = 25
h = 6
i = np.reshape(np.fromiter(get_data(day=day), int), (-1, h, w))
less_zero_layer = min(i, key=lambda i: (i == 0).sum())
part_a = (less_zero_layer == 1).sum() * (less_zero_layer == 2).sum()

print(part_a)
# submit(part_a, day=day, part='a')

image = np.ones_like(less_zero_layer) * 2
for layer in i:
    np.copyto(image, layer, where=(image == 2))

print(image)
for line in image:
    print(''.join(['*' if c == 1 else ' ' for c in line]))

# submit(part_b, day=day, part='b')
