from aocd import get_data
import collections
import networkx as nx
import time
import math
import heapq
from aocd import submit

day = 18
puzzle_input = get_data(day=day)
puzzle_input = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""


def reverse(direction: int):
    rev_dir = {
        1: 2,
        2: 1,
        3: 4,
        4: 3
    }
    return rev_dir.get(direction)


def plan_moves(direction: int):
    # north (1), south (2), west (3), and east (4)
    avail_moves = {1, 2, 3, 4}
    rev = reverse(direction)
    around = avail_moves - {rev, direction}
    return [direction, *around, rev]


def get_position(pos: tuple, dir: int) -> tuple:
    if dir == 1:
        return pos[0], pos[1] + 1
    elif dir == 2:
        return pos[0], pos[1] - 1
    elif dir == 3:
        return pos[0] - 1, pos[1]
    else:
        return pos[0] + 1, pos[1]


def get_boundaries(field: dict) -> tuple:
    all_x = {x for row in field.values() for x in row.keys()}
    all_y = set(field.keys())

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    return min_x, max_x, min_y, max_y


def draw_field(field: dict, pos: tuple = None):
    min_x, max_x, min_y, max_y = get_boundaries(field)
    lines = []
    for idx, y in enumerate(range(min_y, max_y + 1)):
        lines.append(''.join([field[y][x] if (x, y) != pos else 'D' for x in range(min_x, max_x + 1)]))
    print(chr(27) + "[2J" + '\n'.join(lines))
    time.sleep(0.002)


def load_field(data):
    keys = dict()
    doors = dict()
    entrance = None
    field = collections.defaultdict(lambda: collections.defaultdict(lambda: '?'))
    for y, l in enumerate(data.splitlines()):
        for x, c in enumerate(l):
            field[y][x] = c
            if c == '@':
                entrance = (x, y)
            elif c.isupper():
                doors[c] = (x, y)
            elif c.islower():
                keys[c] = (x, y)

    return field, keys, doors, entrance


def look_around(field, pos):
    x, y = pos
    positions = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1)
    ]
    return {pos for pos in positions if field[pos[1]][pos[0]] != '#'}


def explore(field: dict, start: tuple):
    atlas = nx.Graph()
    plan = [start]
    seen = set()

    while True:
        if len(plan) == 0:
            break
        now = plan[0]
        seen.add(now)
        around = look_around(field, now) - seen
        for next_pos in around:
            atlas.add_edge(now, next_pos)
        plan = list(around) + plan[1:]

    return atlas

state_cache = dict()


def close_doors(field, atlas, doors: dict, keys):
    hash_key = tuple(sorted(keys))
    if hash_key in state_cache:
        return state_cache[hash_key]
    new_atlas = nx.Graph(atlas)
    for door, door_pos in doors.items():
        if door.lower() not in keys:
            around = look_around(field, door_pos)
            for item in around:
                new_atlas.remove_edge(door_pos, item)
    state_cache[hash_key] = new_atlas
    return new_atlas


def short_way(field: dict, oxygen: tuple):
    distances = dict()
    sources = [(0, 0, 0)]
    while True:
        next_sources = []
        if len(sources) == 0:
            break
        for source in sources:
            neighbors = [get_position(source, d) for d in range(1, 5)]
            for item in neighbors:
                what = field[item[1]][item[0]]
                distance = distances.get((item[0], item[1]), math.inf)
                dist_next = source[2] + 1
                if distance > dist_next and what in (1, 2):
                    distances[(item[0], item[1])] = dist_next
                    next_sources.append((*item, dist_next))
                    field[item[1]][item[0]] = 5
        sources = next_sources
        draw_field(field)

    return distances[oxygen]


def oxygenify(atlas: nx.Graph, field: dict, oxygen: tuple):
    steps = -1
    sources = [oxygen]
    while True:
        next_sources = []
        if len(sources) == 0:
            break
        for source in sources:
            around = atlas.neighbors(source)
            for pos in around:
                what = field[pos[1]][pos[0]]
                if what in (1, 2, 5):
                    next_sources.append(pos)
                    field[pos[1]][pos[0]] = 4
        sources = next_sources
        draw_field(field)
        steps += 1

    return steps


def solve():
    field, keys, doors, entrance = load_field(puzzle_input)
    collected_keys = set()
    atlas = explore(field, entrance)
    closed_doors = close_doors(field, atlas, doors, set())
    pq = []
    for key, key_pos in keys.items():
        try:
            path = nx.shortest_path_length(closed_doors, entrance, key_pos)
            heapq.heappush(pq, (path, ((key, ), key_pos)))
            print('Key {} is at {}'.format(key, path))
        except nx.NetworkXNoPath:
            pass
            # print('Key {} is unreacehable'.format(key))

    max_k = 0
    while True:
        i = heapq.heappop(pq)
        l, data = i
        ckeys, pos = data
        if set(ckeys) == set(keys.keys()):
            print(l, ckeys)
            break
        if len(ckeys) > max_k:
            print(l, ckeys)
            max_k = len(ckeys)
        closed_doors = close_doors(field, atlas, doors, set(ckeys))
        for key, key_pos in keys.items():
            if key in ckeys:
                continue
            try:
                path = nx.shortest_path_length(closed_doors, pos, key_pos)
                heapq.heappush(pq, (path + l, ((*ckeys, key), key_pos)))
                # print('Key {} is at {}'.format(key, path))
            except nx.NetworkXNoPath:
                pass
                # print('Key {} is unreacehable'.format(key))



    # draw_field(field)


solve()
