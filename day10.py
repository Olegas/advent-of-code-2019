import numpy as np
import math
from aocd import get_data


day = 10
tests = [
    ("""#
.
#
.
#""", (2, (0, 2))),
    (""".#..#..#.""", (2, (4, 0))),
    (""".#..#
.....
#####
....#
...##""", (8, (3, 4))),
    ("""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""", (33, (5, 8))),
    (""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""", (210, (11, 13))),
    (get_data(day=day), (227, (11, 13)))
]


def find_asteroids(space):
    asteroids = set()
    for y, l in enumerate(space):
        for x, i in enumerate(l):
            if i == '#':
                asteroids.add((x, y))

    return asteroids


def find_all_seen(asteroids, station):
    sees = set()
    aim_data = set()

    for asteroid in asteroids:
        if asteroid == station:
            continue
        coords = (asteroid[0] - station[0], asteroid[1] - station[1])
        A = np.array([[0, 1], [coords[0], 1]])
        b = np.array([0, coords[1]])
        try:
            coef = np.linalg.solve(A, b)
            dir = 0 if asteroid[0] > station[0] else 1
            angle = math.atan(coef[0]) + dir * math.pi
            key = (angle, coef[1])
            if key not in sees:
                sees.add(key)
                aim_data.add((angle, coef[1], asteroid))
        except np.linalg.LinAlgError as e:
            angle = -math.pi/2 if asteroid[1] > station[1] else math.pi/2
            key = (angle, 0)
            if key not in sees:
                sees.add(key)
                aim_data.add((angle, 0, asteroid))

    return sees, aim_data


def convert_input_to_space(puzzle_input):
    return [list(l) for l in puzzle_input.splitlines()]


def solve_a(puzzle_input):
    space = convert_input_to_space(puzzle_input)
    asteroids = find_asteroids(space)
    all_seen = {}

    for possible_station in asteroids:
        seen, _ = find_all_seen(asteroids, possible_station)
        all_seen[possible_station] = seen

    counts = sorted([(len(v), k) for k, v in all_seen.items()], key=lambda i: i[0], reverse=True)
    return counts[0]


def solve_b(puzzle_input, station_at):

    count_vaporized = 0
    loop = 0
    space = convert_input_to_space(puzzle_input)

    while True:
        asteroids = find_asteroids(space)
        seen, aim_data = find_all_seen(asteroids, station_at)
        aim_data = [(angle if angle <= math.pi/2 else -angle, x, asteroid) for angle, x, asteroid in aim_data]
        aim_data = sorted(aim_data, key=lambda i: i[0], reverse=True)
        for angle, x, asteroid in aim_data:
            print('Fire at {}'.format(asteroid))
            space[asteroid[1]][asteroid[0]] = '.'
            count_vaporized += 1
            if count_vaporized == 200:
                return asteroid[0] * 100 + asteroid[1]
        print('Loop {}, vaporized {} asteroids'.format(loop, count_vaporized))
        loop += 1


for idx, test in enumerate(tests):
    res = solve_a(test[0])
    if res != test[1]:
        print("Test {}: FAILED {} != {}".format(idx, res, test[1]))
    else:
        print("Test {}: OK".format(idx))

puzzle = get_data(day=day)
asteroids_seen, station = solve_a(puzzle)
print(asteroids_seen, station)

answer_b = solve_b(puzzle, station)
print(answer_b)


