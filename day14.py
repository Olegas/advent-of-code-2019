from aocd import get_data
from aocd import submit
import matplotlib
from fractions import Fraction as frac
import collections
import networkx as nx

day = 14
xxx = get_data(day=day).splitlines()
tests = [
    ("""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL""", 31),
    ("""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""", 165),
    ("""157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""", 13312),
    ("""2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF""", 180697),
    ("""171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""", 2210736)
]


def solve(puzzle_input):
    process_outputs = collections.defaultdict(int)
    process_outputs['ORE'] = 1
    g = nx.DiGraph()
    for line in puzzle_input.splitlines():
        src_str, tgt_str = line.split('=>')
        sources = []
        for item in src_str.split(', '):
            weight, name = item.strip().split(' ')
            sources.append((int(weight.strip()), name.strip()))
        weight, name = tgt_str.strip().split(' ')
        target = (int(weight), name)
        process_outputs[name] = int(weight)

        for source in sources:
            g.add_edge(source[1], target[1], weight=frac(source[0], target[0]))

    order = []
    print(list(reversed(list(nx.topological_sort(nx.line_graph(g))))))
    for item in reversed(list(nx.topological_sort(g))):
        for adj in g.predecessors(item):
            order.append((adj, item))

    print(order)
    requirements = collections.defaultdict(list)
    requirements['FUEL'] = [1]
    current_process = 'FUEL'
    production_finished = []

    for item in order:
        if item[0] != current_process:
            required = sum(requirements[current_process])
            min_output_per_process = process_outputs[current_process]
            full, leftover = divmod(required, min_output_per_process)
            requirements[current_process] = [(full + (1 if leftover > 0 else 0)) * min_output_per_process]
            production_finished.append(current_process)
            current_process = item[0]
        requirements[item[0]].append(requirements[item[1]][0] * g[item[0]][item[1]]['weight'])

    print(order)
    print(len(production_finished) == len(set(production_finished)), production_finished)
    return sum(requirements['ORE'])


for idx, test in enumerate(tests):
    print()
    res = solve(test[0])
    if res == test[1]:
        print('Test {}: OK'.format(idx))
    else:
        print('Test {}: Failed. {} != {}'.format(idx, res, test[1]))

