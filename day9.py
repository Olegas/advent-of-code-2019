from aocd import get_data
import collections
import itertools
from aocd import submit

day = 9
puzzle_input = [int(i) for i in get_data(day=day).split(',')]

tests = [
    ([3,9,8,9,10,9,4,9,99,-1,8], 8, 1),
    ([3,9,8,9,10,9,4,9,99,-1,8], 7, 0),
    ([3,9,8,9,10,9,4,9,99,-1,8], 9, 0),
    ([3,9,7,9,10,9,4,9,99,-1,8], 7, 1),
    ([3,9,7,9,10,9,4,9,99,-1,8], 8, 0),
    ([3,9,7,9,10,9,4,9,99,-1,8], 9, 0),
    ([3,3,1108,-1,8,3,4,3,99], 8, 1),
    ([3,3,1108,-1,8,3,4,3,99], 7, 0),
    ([3,3,1108,-1,8,3,4,3,99], 9, 0),
    ([3,3,1107,-1,8,3,4,3,99], 7, 1),
    ([3,3,1107,-1,8,3,4,3,99], 8, 0),
    ([3,3,1107,-1,8,3,4,3,99], 9, 0),
    ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0, 0),
    ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], -1, 1),
    ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 1, 1),
    ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0, 0),
    ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], -1, 1),
    ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 1, 1),
    ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 8, 1000),
    ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 7, 999),
    ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 9, 1001),
    ([int(i) for i in get_data(day=5).split(',')], 1, 12896948),
    ([int(i) for i in get_data(day=5).split(',')], 5, 7704130),
    ([104,1125899906842624,99], None, 1125899906842624),
    ([1102,34915192,34915192,7,4,7,99,0], None, 1219070632396864),
    ([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], None, 99, [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]),
    ([int(i) for i in get_data(day=9).split(',')], 1, 3780860499),
    ([int(i) for i in get_data(day=9).split(',')], 2, 33343),
]


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


def solve(program, i, stdout):
    g = run_intcode(Memory(program))
    last_value = None
    try:
        while True:
            if last_value == '?':
                last_value = g.send(i)
            else:
                last_value = next(g)
            stdout.append(last_value)
    except StopIteration:
        """do nothing"""

    return last_value


ok = True
for idx, test in enumerate(tests):
    try:
        output = []
        result = solve(test[0], test[1], output)
        if result == test[2]:
            if 3 in test:
                if test[3] == output:
                    print('Test {}: OK'.format(idx))
                    continue
                else:
                    print('Test {}: FAILED. Output mismatch\nExpected: {}\nActual: {}'.format(idx, test[3], output))
            else:
                print('Test {}: OK'.format(idx))
                continue
        else:
            print('Test {}: FAILED {} != {}'.format(idx, result, test[2]))
        ok &= False
    except Exception as e:
        print('Text {}: EXCEPTION {}'.format(idx, e))

print('Tests passed' if ok else 'Tests failed')

# submit(part_a, day=day, part='a')
# submit(part_b, day=day, part='b')
