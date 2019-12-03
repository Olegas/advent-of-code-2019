from aocd import get_data
from aocd import submit

input = get_data(day=3).split('\n')
#input = ['R75,D30,R83,U83,L12,D49,R71,U7,L72',
#'U62,R66,U55,R34,D71,R55,D58,R83'
#]
#input = ['R8,U5,L5,D3', 'U7,R6,D4,L4']
print(input)

crosses = []
occupied = {}
distances = {}
def walk(path, wire):
    steps = path.split(',')
    pos = (0, 0)
    path_len = 0
    for step in steps:
        direction = step[0]
        dist = int(step[1:])
        for k in range(1, dist + 1):
            path_len += 1
            if direction == 'R':
                pos = (pos[0] + 1, pos[1])
            elif direction == 'L':
                pos = (pos[0] - 1, pos[1])
            elif direction == 'U':
                pos = (pos[0], pos[1] + 1)
            elif direction == 'D':
                pos = (pos[0], pos[1] - 1)
            distances[(wire, pos)] = path_len
            if occupied.get(pos) is None:
                occupied[pos] = wire
            elif occupied[pos] != wire:
                crosses.append(pos)


for idx, path in enumerate(input):
    walk(path, idx)


def dist(b):
    return abs(b[0]) + abs(b[1])


# submit(min([dist(i) for i in crosses]), day=3, part='a')

print(crosses)
print(min(distances))

cross_dist = []
for cross in crosses:
    dist_a = distances[(0, cross)]
    dist_b = distances[(1, cross)]
    cross_dist.append(dist_a + dist_b)

print(min(cross_dist))

# submit(min(cross_dist), day=3, part='b')
