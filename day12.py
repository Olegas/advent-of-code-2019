from aocd import get_data
import itertools
from collections import defaultdict
from aocd import submit
import numpy as np
import copy

day = 12


def parse_line(line):
    line = line[1:-1]
    coords = [i.split('=') for i in line.split(', ')]
    coords = [int(i[1]) for i in coords]
    return {
        'pos': coords,
        'vel': [0, 0, 0]
    }


def parse_lines(lines):
    return [parse_line(line) for line in lines]


def apply_gravity(a, b):
    for i in range(0, 3):
        if a['pos'][i] < b['pos'][i]:
            a['vel'][i] += 1
            b['vel'][i] -= 1
        elif a['pos'][i] > b['pos'][i]:
            a['vel'][i] -= 1
            b['vel'][i] += 1


def apply_velocity(a):
    for i in range(0, 3):
        a['pos'][i] += a['vel'][i]


def calc_energy(system):
    energy = 0
    for planet in system:
        pot = sum([abs(k) for k in planet['pos']])
        kin = sum([abs(k) for k in planet['vel']])
        energy += pot * kin
    return energy


def solve_a(data, steps):
    puzzle_input = parse_lines(data)
    for iteration in range(0, steps):
        for i in itertools.combinations(range(0, len(puzzle_input)), 2):
            apply_gravity(puzzle_input[i[0]], puzzle_input[i[1]])

        for i in puzzle_input:
            apply_velocity(i)

    return calc_energy(puzzle_input)


def solve_b(data):
    puzzle_data = parse_lines(data)
    periods = []
    for j in range(3):
        puzzle = copy.deepcopy(puzzle_data)
        init = tuple([planet['pos'][j] for planet in puzzle])
        iter = 0
        while True:
            for i in itertools.combinations(range(0, len(puzzle)), 2):
                apply_gravity(puzzle[i[0]], puzzle[i[1]])

            for i in puzzle:
                apply_velocity(i)

            pos = tuple([planet['pos'][j] for planet in puzzle])
            vel = tuple([planet['vel'][j] for planet in puzzle])
            iter += 1

            if pos == init and vel == (0, 0, 0, 0):
                periods.append(iter)
                break

    return np.lcm.reduce(periods)


data = get_data(day=day)
print(solve_a(data.splitlines(), 1000))
print(solve_b(data.splitlines()))
