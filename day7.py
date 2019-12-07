from aocd import get_data
from aocd import submit

day = 7
_input = get_data(day=day)
program = [int(i) for i in _input.split(',')]


def _read_value(input, pos, mode):
    return input[input[pos]] if int(mode) == 0 else input[pos]


def run_intcode(code: list):
    pos = 0
    output_reg = None
    while True:
        opcode_block = str(code[pos])
        opcode = opcode_block[-2:]
        modes_block = opcode_block[0:-len(opcode)]
        paramter1_mode = modes_block[-1:] or '0'
        paramter2_mode = modes_block[-2:-1] or '0'

        opcode = int(opcode)

        if opcode == 1:
            cmd_size = 4
            arg1 = _read_value(code, pos + 1, paramter1_mode)
            arg2 = _read_value(code, pos + 2, paramter2_mode)
            out = code[pos + 3]
            code[out] = arg1 + arg2
        elif opcode == 2:
            cmd_size = 4
            arg1 = _read_value(code, pos + 1, paramter1_mode)
            arg2 = _read_value(code, pos + 2, paramter2_mode)
            out = code[pos + 3]
            code[out] = arg1 * arg2
        elif opcode == 3:
            write_pos = code[pos + 1]
            cmd_size = 2
            code[write_pos] = yield
        elif opcode == 4:
            read_pos = code[pos + 1]
            cmd_size = 2
            yield code[read_pos]
        elif opcode == 5:
            arg1 = _read_value(code, pos + 1, paramter1_mode)
            arg2 = _read_value(code, pos + 2, paramter2_mode)
            cmd_size = 3
            if arg1 != 0:
                pos = arg2
                cmd_size = 0
        elif opcode == 6:
            arg1 = _read_value(code, pos + 1, paramter1_mode)
            arg2 = _read_value(code, pos + 2, paramter2_mode)
            cmd_size = 3
            if arg1 == 0:
                pos = arg2
                cmd_size = 0
        elif opcode == 7:
            arg1 = _read_value(code, pos + 1, paramter1_mode)
            arg2 = _read_value(code, pos + 2, paramter2_mode)
            write_to = code[pos + 3]
            cmd_size = 4
            code[write_to] = 1 if arg1 < arg2 else 0
        elif opcode == 8:
            arg1 = _read_value(code, pos + 1, paramter1_mode)
            arg2 = _read_value(code, pos + 2, paramter2_mode)
            write_to = code[pos + 3]
            cmd_size = 4
            code[write_to] = 1 if arg1 == arg2 else 0
        elif opcode == 99:
            break
        else:
            raise 'Incorrect opcode'

        pos += cmd_size

    return output_reg


def solve(code, phase_from, phase_to):
    max = 0
    max_inputs = None
    for a in range(phase_from, phase_to + 1):
        for b in range(phase_from, phase_to + 1):
            for c in range(phase_from, phase_to + 1):
                for d in range(phase_from, phase_to + 1):
                    for e in range(phase_from, phase_to + 1):
                        if len({a, b, c, d, e}) != 5:
                            continue

                        ga = run_intcode(code.copy())
                        gb = run_intcode(code.copy())
                        gc = run_intcode(code.copy())
                        gd = run_intcode(code.copy())
                        ge = run_intcode(code.copy())

                        init_value = 0
                        thurst_value = 0

                        next(ga)
                        next(gb)
                        next(gc)
                        next(gd)
                        next(ge)
                        while True:
                            try:
                                ga.send(a)
                                val_a = ga.send(init_value)

                                gb.send(b)
                                val_b = gb.send(val_a)

                                gc.send(c)
                                val_c = gc.send(val_b)

                                gd.send(d)
                                val_d = gd.send(val_c)

                                ge.send(e)

                                thurst_value = init_value = ge.send(val_d)
                            except StopIteration:
                                break

                        if thurst_value > max:
                            max = thurst_value
                            max_inputs = (a,b,c,d,e)

    print(max, max_inputs)
    return max


part_a = solve(program, 0, 4)

part_b = solve(program, 5, 9)

# submit(part_a, day=day, part='a')
# submit(part_b, day=day, part='b')
