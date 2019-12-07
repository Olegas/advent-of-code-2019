from aocd import get_data
import networkx as nx

day = 6
_input = get_data(day=day)
lines = _input.split('\n')

sum = 0
g = nx.Graph([item.split(')') for item in lines])
for node in g.nodes:
    sum += nx.shortest_path_length(g, node, 'COM')

part_a = sum
part_b = nx.shortest_path_length(g, 'SAN', 'YOU') - 2
print(part_a, part_b)