from aocd import get_data
import collections
import itertools
from aocd import submit

day = 11
puzzle_input = [int(i) for i in get_data(day=day).split(',')]


class Memory(dict):

    def __init__(self, program):
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


panels = collections.defaultdict(lambda: collections.defaultdict(int))


def solve(program, start_panel):
    colored_panels = set()
    position = (0, 0)
    panels[position[1]][position[0]] = start_panel
    direction = 0
    g = run_intcode(Memory(program))
    try:
        while True:
            last_value = next(g)
            if last_value == '?':
                last_value = g.send(panels[position[1]][position[0]])
                if last_value not in (0, 1):
                    raise Exception('Incorrect color {}'.format(last_value))
                colored_panels.add(position)
                panels[position[1]][position[0]] = last_value
            elif type(last_value) == int:
                if last_value == 1:
                    # 1 - 90 left
                    direction = (direction - 1) % 4
                elif last_value == 0:
                    # 0 - 90 right
                    direction = (direction + 1) % 4
                else:
                    raise Exception('Incorrect robot output {}'.format(last_value))

                # 0 - up, 1 - right, 2 - down, 3 - left
                if direction == 0:
                    position = (position[0], position[1] + 1)
                elif direction == 1:
                    position = (position[0] + 1, position[1])
                elif direction == 2:
                    position = (position[0], position[1] - 1)
                elif direction == 3:
                    position = (position[0] - 1, position[1])
                else:
                    raise Exception('Incorrect direction {}'.format(direction))
    except StopIteration:
        """do nothing"""

    return colored_panels


part_a = len(solve(puzzle_input, 0))
print(part_a)
#submit(part_a, day=day, part='a')

all_panels_visited = solve(puzzle_input, 1)

all_x = [i[0] for i in all_panels_visited]
all_y = [i[1] for i in all_panels_visited]

min_x = min(all_x)
max_x = max(all_x)
min_y = min(all_y)
max_y = max(all_y)

for y in range(min_y, max_y + 1):
    print(''.join(['*' if panels[y][x] == 1 else ' ' for x in range(min_x, max_y + 1)]))


