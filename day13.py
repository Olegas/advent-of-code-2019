from aocd import get_data
import collections
import math
from pynput.keyboard import Key, Listener
import time
import threading
import itertools
from aocd import submit

day = 13
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


field_creator = run_intcode(Memory(puzzle_input))
field = collections.defaultdict(lambda: collections.defaultdict(int))
outputs = []
blocks = 0
while True:
    try:
        outputs.append(next(field_creator))
        if len(outputs) == 3:
            x, y, tile = outputs
            field[y][x] = tile
            outputs = []
            if tile == 2:
                blocks += 1
    except StopIteration:
        break

# submit(blocks, day=day, part='a')

all_x = {x for row in field.values() for x in row.keys()}
all_y = set(field.keys())

min_x = min(all_x)
max_x = max(all_x)
min_y = min(all_y)
max_y = max(all_y)

vis_map = {
    0: ' ',
    1: '▌',
    2: '█',
    3: '_',
    4: '•'
}


class Planner:
    ball = None
    paddle = None
    moves = []

    def paddle_position(self, pos):
        if self.paddle != pos:
            self.paddle = pos

    def ball_position(self, pos):
        if self.ball is None:
            self.ball = pos
        elif self.ball != pos:
            dx = pos[0] - self.ball[0]
            next_turn_x = pos[0] + dx
            if self.paddle[0] == pos[0] and self.paddle[1] == pos[1] + 1:
                # ball is directly over paddle, do nothing
                pass
            elif self.paddle[0] == next_turn_x:
                # paddle at correct location
                pass
            else:
                # follow the ball
                paddle_dx = -1 if self.paddle[0] > next_turn_x else 1
                self.moves.append(paddle_dx)
            self.ball = pos

    def get(self):
        ret = 0
        if len(self.moves) > 0:
            ret = self.moves[0]
            self.moves = self.moves[1:]
        return ret


puzzle_input[0] = 2
field_creator = run_intcode(Memory(puzzle_input))
field = collections.defaultdict(lambda: collections.defaultdict(int))
outputs = []
planner = Planner()
blocks = 0
score = 0
while True:
    critical_change = False
    try:
        val = next(field_creator)
        if val == '?':
            next_move = planner.get()
            val = field_creator.send(next_move)
        outputs.append(val)
        if len(outputs) == 3:
            x, y, tile = outputs
            if x == -1:
                score = tile
            else:
                field[y][x] = tile
                if tile == 4:
                    planner.ball_position((x, y))
                    critical_change = True
                elif tile == 3:
                    planner.paddle_position((x, y))
                    critical_change = True
                else:
                    critical_change = False
            outputs = []
    except StopIteration:
        break

    lines = []
    for y in range(min_y, max_y + 1):
        lines.append(''.join([vis_map.get(field[y][x]) for x in range(min_x, max_x + 1)]))
    print(chr(27) + "[2J" + '\n'.join(lines) + '\nScore: {}'.format(score))
    if critical_change:
        time.sleep(0.03)
