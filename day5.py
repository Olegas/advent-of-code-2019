from aocd import get_data
from aocd import submit

day = 5
_input = get_data(day=day)
input = [int(i) for i in _input.split(',')]


def read_value(input, pos, mode):
    return input[input[pos]] if int(mode) == 0 else input[pos]


input=[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

pos = 0
input_reg = 0
output_reg = None
while True:
    opcode_block = str(input[pos])
    opcode = opcode_block[-2:]
    modes_block = opcode_block[0:-len(opcode)]
    paramter1_mode = modes_block[-1:] or '0'
    paramter2_mode = modes_block[-2:-1] or '0'

    opcode = int(opcode)

    if opcode == 1:
        cmd_size = 4
        arg1 = read_value(input, pos + 1, paramter1_mode)
        arg2 = read_value(input, pos + 2, paramter2_mode)
        out = input[pos + 3]
        input[out] = arg1 + arg2
    elif opcode == 2:
        cmd_size = 4
        arg1 = read_value(input, pos + 1, paramter1_mode)
        arg2 = read_value(input, pos + 2, paramter2_mode)
        out = input[pos + 3]
        input[out] = arg1 * arg2
    elif opcode == 3:
        write_pos = input[pos + 1]
        cmd_size = 2
        input[write_pos] = input_reg
    elif opcode == 4:
        read_pos = input[pos + 1]
        cmd_size = 2
        output_reg = input[read_pos]
    elif opcode == 5:
        arg1 = read_value(input, pos + 1, paramter1_mode)
        arg2 = read_value(input, pos + 2, paramter2_mode)
        cmd_size = 3
        if arg1 != 0:
            pos = arg2
            cmd_size = 0
    elif opcode == 6:
        arg1 = read_value(input, pos + 1, paramter1_mode)
        arg2 = read_value(input, pos + 2, paramter2_mode)
        cmd_size = 3
        if arg1 == 0:
            pos = arg2
            cmd_size = 0
    elif opcode == 7:
        arg1 = read_value(input, pos + 1, paramter1_mode)
        arg2 = read_value(input, pos + 2, paramter2_mode)
        write_to = input[pos + 3]
        cmd_size = 4
        input[write_to] = 1 if arg1 < arg2 else 0
    elif opcode == 8:
        arg1 = read_value(input, pos + 1, paramter1_mode)
        arg2 = read_value(input, pos + 2, paramter2_mode)
        write_to = input[pos + 3]
        cmd_size = 4
        input[write_to] = 1 if arg1 == arg2 else 0
    elif opcode == 99:
        break
    else:
        raise 'Incorrect opcode'

    pos += cmd_size

answer = output_reg
print(answer)
# submit(answer, day=day, part='a')


#submit(answer, day=day, part='b')
