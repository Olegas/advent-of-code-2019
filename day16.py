from aocd import get_data
import collections
import networkx as nx
import numpy as np
import time
import math
from aocd import submit

day = 16
puzzle_input = get_data(day=day)

pattern_cache = dict()


def shift_pattern(pattern):
    return pattern[1:] + pattern[0:1]


def apply_pattern(numbers: list, pattern: list, step: int) -> int:
    result = 0
    ptr_len = len(pattern)
    for idx in range(step, len(numbers)):
        p_idx = idx % ptr_len
        p = pattern[p_idx]
        result += numbers[idx] * p
    return abs(result) % 10


def mutate_pattern(pattern, i):
    res = []
    for k in pattern:
        res += [k] * (i + 1)
    return res


def construct_new_input(numbers, base_pattern):
    res = []
    for i in range(len(numbers)):
        pattern = pattern_cache.get(i, None)
        if pattern is None:
            pattern = shift_pattern(mutate_pattern(base_pattern, i))
            pattern_cache[i] = pattern
        res.append(apply_pattern(numbers, pattern, i))
    return res


def run(numbers, iters, pattern):
    for i in range(iters):
        numbers = construct_new_input(numbers, pattern)
        if i % 10 == 0:
            print(i)
    return numbers


def to_list(s):
    return [int(i) for i in s]


def to_num(l):
    return ''.join([str(k) for k in l])


initial_pattern = [0, 1, 0, -1]
list_num = to_list(puzzle_input)
print(to_num(run(list_num, 100, initial_pattern)[:8]))

offset = int(to_num(list_num[:7]))
full_data = list_num * 10000
cut = full_data[offset:]

full, part = divmod(offset, 4)
cut_pattern = initial_pattern[part:] + initial_pattern[:part]
result = run(cut, 100, cut_pattern)
print(to_num(result[:8]))


