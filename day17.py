from aocd import get_data
import collections
import networkx as nx
import time
import math
from aocd import submit

day = 17
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


def get_boundaries(field: dict) -> tuple:
    all_x = {x for row in field.values() for x in row.keys()}
    all_y = set(field.keys())

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    return min_x, max_x, min_y, max_y


def draw_field(field: dict, pos: tuple = (-1, -1, '?')):
    min_x, max_x, min_y, max_y = get_boundaries(field)
    lines = []
    for idx, y in enumerate(range(min_y, max_y + 1)):
        lines.append(''.join([chr(field[y][x]) if (x, y) != pos[:2] else pos[2] for x in range(min_x, max_x + 1)]))
    print(chr(27) + "[2J" + '\n'.join(lines))
    time.sleep(0.002)


def explore(program: list, field: dict, mode=1, out_buf: list = None):
    robots = set()
    program[0] = mode
    g = run_intcode(Memory(program))
    out_pos = 0
    x = 0
    y = 0
    val = next(g)

    while True:
        if val == '?':
            val = g.send(out_buf[out_pos])
            out_pos += 1
        else:
            if mode == 1:
                if val == 10:
                    y += 1
                    x = 0
                else:
                    if val in (ord('<'), ord('>'), ord('^'), ord('v')):
                        robots.add((x, y, chr(val)))
                        val = ord('#')
                    field[y][x] = val
                    x += 1
            else:
                if val < 255:
                    print(chr(val), end='', flush=True)
                else:
                    print(val)

            try:
                val = next(g)
            except StopIteration as e:
                break

    return robots


def look_around(space, visited, crosses, pos):
    min_x, max_x, min_y, max_y = get_boundaries(space)
    x, y, _ = pos
    coords = {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} - (visited - crosses)
    coords = {i for i in coords if min_x <= x <= max_x and min_y <= y <= max_y}
    coords = {i for i in coords if space[i[1]][i[0]] == 35}
    return coords


def detect_crosses(space):
    min_x, max_x, min_y, max_y = get_boundaries(space)
    crosses = set()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            char = space[y][x]
            if char == 35:
                coords = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                around = {space[y][x] for x, y in coords if min_x <= x <= max_x and min_y <= y <= max_y}
                if around == {35}:
                    crosses.add((x, y))
    return crosses


def get_moves(pos, around):
    x, y, dir = pos
    moves = dict()
    if dir == '^':
        moves[(x, y - 1)] = 1, x, y-1, '^'
        moves[(x - 1, y)] = 'L', x, y, '<'
        moves[(x + 1, y)] = 'R', x, y, '>'
    elif dir == 'v':
        moves[(x, y + 1)] = 1, x, y+1, 'v'
        moves[(x + 1, y)] = 'L', x, y, '>'
        moves[(x - 1, y)] = 'R', x, y, '<'
    elif dir == '<':
        moves[(x - 1, y)] = 1, x-1, y, '<'
        moves[(x, y + 1)] = 'L', x, y, 'v'
        moves[(x, y - 1)] = 'R', x, y, '^'
    else:
        moves[(x + 1, y)] = 1, x+1, y, '>'
        moves[(x, y - 1)] = 'L', x, y, '^'
        moves[(x, y + 1)] = 'R', x, y, 'v'

    return {v[0]: v[1:] for k, v in moves.items() if k in around}


def next_direction(space, visited, crosses, pos):
    around = look_around(space, visited, crosses, pos)
    moves = get_moves(pos, around)

    if 1 in moves:
        # prefer forward
        return 1, moves[1]
    elif len(moves) > 0:
        # get first
        first = next(iter(moves))
        return first, moves[first]


def find_path(space, robot, crosses):
    pos = robot
    path = []
    visited = set()
    while True:
        move = next_direction(space, visited, crosses, pos)
        if move is None:
            break
        cmd, next_pos = move
        if type(cmd) == int:
            if type(path[-1]) == int:
                path[-1] += cmd
            else:
                path.append(cmd)
        else:
            path.append(cmd)
        visited.add((pos[0], pos[1]))
        pos = next_pos

    return path, pos


def serialize_program(program):
    strings = [str(c) if type(c) != str else c for c in program]
    spearate = ','.join(strings)
    return [ord(c) for c in spearate] + [10]


def solve():
    space = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    robots = explore(puzzle_input, space)
    robot = robots.pop()
    draw_field(space, robot)

    crosses = detect_crosses(space)
    checksum = sum([x * y for x, y in crosses])
    print(checksum)
    path, robot = find_path(space, robot, crosses)

    print(path)

    programs = {
        'Main': ['A', 'B', 'A', 'B', 'A', 'C', 'B', 'C', 'A', 'C'],
        'A': ['L', 10, 'L', 12, 'R', 6],
        'B': ['R', 10, 'L', 4, 'L', 4, 'L', 12],
        'C': ['L', 10, 'R', 10, 'R', 6, 'L', 4]
    }

    out_buf = serialize_program(programs['Main'])
    print('Main', programs['Main'])
    for prog in ['A', 'B', 'C']:
        print(prog, programs[prog])
        out_buf += serialize_program(programs[prog])
    out_buf += [ord('n'), 10]

    explore(puzzle_input, space, 2, out_buf)


solve()

