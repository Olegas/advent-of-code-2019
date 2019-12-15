from aocd import get_data
import collections
import networkx as nx
import time
import curses
from aocd import submit

day = 15
puzzle_input = [int(i) for i in get_data(day=day).split(',')]


class Memory(dict):

    def __init__(self, program: list):
        super().__init__()
        self.update(zip(range(len(program)), program))

    def __missing__(self, key):
        return 0

    def __getitem__(self, item):
        if type(item) == int:
            if item < 0:
                raise Exception('Accessing incorrect memory location: {}'.format(item))
            else:
                return super().__getitem__(item)
        else:
            raise TypeError('Incorrect memory address type: {}'.format(type(item)))


def run_intcode(code: dict):

    pos = 0
    relative_base = 0

    def _read_value(arg_idx, mode):
        offset = pos + arg_idx
        mode = int(mode)
        # Position mode
        if mode == 0:
            return code[code[offset]]
        # Immediate mode
        elif mode == 1:
            return code[offset]
        # Relative mode
        elif mode == 2:
            return code[code[offset] + relative_base]
        else:
            raise Exception('Incorrect mode {}'.format(mode))

    def _write_value(arg_idx, value, mode):
        mode = int(mode)
        offset = pos + arg_idx
        if mode == 0:
            code[code[offset]] = value
        elif mode == 1:
            raise Exception('Immediate mode for write operation is not possible')
        elif mode == 2:
            code[code[offset] + relative_base] = value
        else:
            raise Exception('Incorrect parameter mode')

    while True:
        opcode_block = str(code[pos])
        opcode = opcode_block[-2:]
        modes_block = opcode_block[0:-len(opcode)]
        paramter1_mode = modes_block[-1:] or '0'
        paramter2_mode = modes_block[-2:-1] or '0'
        paramter3_mode = modes_block[-3:-2] or '0'

        opcode = int(opcode)

        if opcode == 1:
            cmd_size = 4
            arg1 = _read_value(1, paramter1_mode)
            arg2 = _read_value(2, paramter2_mode)
            _write_value(3, arg1 + arg2, paramter3_mode)
        elif opcode == 2:
            cmd_size = 4
            arg1 = _read_value(1, paramter1_mode)
            arg2 = _read_value(2, paramter2_mode)
            _write_value(3, arg1 * arg2, paramter3_mode)
        elif opcode == 3:
            cmd_size = 2
            data = yield '?'
            _write_value(1, data, paramter1_mode)
        elif opcode == 4:
            cmd_size = 2
            yield _read_value(1, paramter1_mode)
        elif opcode == 5:
            arg1 = _read_value(1, paramter1_mode)
            arg2 = _read_value(2, paramter2_mode)
            cmd_size = 3
            if arg1 != 0:
                pos = arg2
                cmd_size = 0
        elif opcode == 6:
            arg1 = _read_value(1, paramter1_mode)
            arg2 = _read_value(2, paramter2_mode)
            cmd_size = 3
            if arg1 == 0:
                pos = arg2
                cmd_size = 0
        elif opcode == 7:
            arg1 = _read_value(1, paramter1_mode)
            arg2 = _read_value(2, paramter2_mode)
            _write_value(3, 1 if arg1 < arg2 else 0, paramter3_mode)
            cmd_size = 4
        elif opcode == 8:
            arg1 = _read_value(1, paramter1_mode)
            arg2 = _read_value(2, paramter2_mode)
            _write_value(3, 1 if arg1 == arg2 else 0, paramter3_mode)
            cmd_size = 4
        elif opcode == 9:
            cmd_size = 2
            arg1 = _read_value(1, paramter1_mode)
            relative_base += arg1
        elif opcode == 99:
            break
        else:
            raise Exception('Incorrect opcode {} at instruction {}'.format(opcode, opcode_block))

        pos += cmd_size


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


def draw_field(field: dict, pos: tuple, window):
    vis_map = {
        -1: '░',
        0: '#',
        1: '.',
        2: 'o',
        3: 'D',
        4: 'O'
    }
    min_x, max_x, min_y, max_y = get_boundaries(field)
    for idx, y in enumerate(range(min_y, max_y + 1)):
        window.addstr(idx, 0, ''.join([vis_map.get(field[y][x]) if (x, y) != pos else 'D' for x in range(min_x, max_x + 1)]))
    window.refresh()
    time.sleep(0.02)


def explore(program: list, field: dict, window):
    atlas = nx.Graph()
    plan = plan_moves(1)
    seen = set()
    g = run_intcode(Memory(program))
    pos = (0, 0)
    val = next(g)
    next_direction = None
    oxygen = None

    while True:
        if val == '?':
            next_direction = plan[0]
            plan = plan[1:]
            val = g.send(next_direction)
        elif val in range(3):
            new_pos = get_position(pos, next_direction)
            if val == 0:
                pass
            elif val == 1 or val == 2:
                if val == 2:
                    oxygen = new_pos
                if new_pos not in seen:
                    seen.add(new_pos)
                    atlas.add_edge(pos, new_pos)
                    plan = plan_moves(next_direction) + plan
                elif len(plan) == 0:
                    break
                pos = new_pos
            field[new_pos[1]][new_pos[0]] = val
            draw_field(field, pos, window)
            val = next(g)
        else:
            raise Exception('Incorrect result')

    return oxygen, atlas


def oxygenify(atlas: nx.Graph, field: dict, oxygen: tuple, window):
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
                if what in (1, 2):
                    next_sources.append(pos)
                    field[pos[1]][pos[0]] = 4
        sources = next_sources
        draw_field(field, None, window)
        steps += 1

    return steps


def solve(window):
    space = collections.defaultdict(lambda: collections.defaultdict(lambda: -1))
    oxygen, atlas = explore(puzzle_input, space, window)
    print(len(nx.shortest_path(atlas, (0, 0), oxygen)) - 1)

    print(oxygenify(atlas, space, oxygen, window))


curses.wrapper(solve)
