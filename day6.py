from aocd import get_data
from aocd import submit
from collections import defaultdict

day = 6
_input = get_data(day=day)
lines = _input.split('\n')

particles = set()
forward = defaultdict(list)
backward = {}
weights = defaultdict(int)
sum_paths = 0
for line in lines:
    center, particle = line.split(')')
    forward[center].append(particle)
    backward[particle] = center
    particles.add(particle)

answer = 0
for particle in particles:
    len_path = -1
    while particle:
        len_path += 1
        particle = backward.get(particle, None)
    answer += len_path

#print(answer)

#submit(answer, day=day, part='a')


def common(a, b):
    res = set()
    while a:
        res.add(a)
        a = backward.get(a, None)
    while b:
        next = backward.get(b, None)
        if next in res:
            return next
        else:
            b = next
    return None


def path(a, b = 'COM'):
    res = []
    while a:
        next = backward.get(a, None)
        if next == b:
            return res
        else:
            res.append(next)
            a = next
    return res


cmn = common('SAN', 'YOU')
a = path('SAN', cmn)
b = path('YOU', cmn)

answer = len(a) + len(b)

# print(answer)


# submit(answer, day=day, part='b')
