import time
import collections


def get_boundaries(field: dict) -> tuple:
    all_x = {x for row in field.values() for x in row.keys()}
    all_y = set(field.keys())

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    return min_x, max_x, min_y, max_y


def draw_field(field: dict, vis_map):
    min_x, max_x, min_y, max_y = get_boundaries(field)
    if vis_map is None:
        vis_map = collections.defaultdict(lambda k: k)
    lines = []
    for idx, y in enumerate(range(min_y, max_y + 1)):
        lines.append(''.join([vis_map[field[y][x]] for x in range(min_x, max_x + 1)]))
    print(chr(27) + "[2J" + '\n'.join(lines))
    time.sleep(0.002)