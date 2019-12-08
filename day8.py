from aocd import get_data
import itertools
from collections import defaultdict
from aocd import submit

day = 8
_input = get_data(day=day)
#_input = '123456789012'
#_input = '0222112222120000'
w = 25
h = 6
layer_size = w * h

layers = defaultdict(list)
for idx, pixel in enumerate(_input):
    pixel = int(pixel)
    layers[idx // layer_size].append(pixel)

target_layer = None
min_count_zero = layer_size + 1
for idx, layer in layers.items():
    zero_count = len([i for i in layer if i == 0])
    if zero_count == 0:
        continue
    if zero_count < min_count_zero:
        min_count_zero = zero_count
        target_layer = layer

sums = defaultdict(int)
for c in target_layer:
    sums[c] += 1

# part_a = sums[1] * sums[2]
# submit(part_a, day=day, part='a')

image = [None for k in range(0, layer_size)]
layer_list = list(layers.values())
layer_list.reverse()
for layer in layer_list:
    for idx, c in enumerate(layer):
        if image[idx] is None or c != 2:
            image[idx] = c


while len(image):
    row = image[:w]
    row = ['*' if p == 1 else ' ' for p in row]
    print(''.join(row))
    image = image[w:]

# submit(part_b, day=day, part='b')
