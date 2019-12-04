from aocd import get_data
from aocd import submit

input = get_data(day=4).split('-')
min_p = int(input[0])
max_p = int(input[1])


def never_decreased(password):
    s = str(password)
    n = 0
    for c in s:
        if int(c) < n:
            return False
        n = int(c)

    return True


def has_double(password):
    prev = ''
    group_count = 1
    has_at_least_one = False
    for c in str(password):
        if c == prev:
            group_count += 1
        else:
            if group_count == 2:
                has_at_least_one = True
            group_count = 1
            prev = c

    if group_count == 2:
        return True

    return has_at_least_one


matched = []
for password in range(min_p, max_p + 1):
    if has_double(password) and never_decreased(password):
        matched.append(password)

#print(has_double(123789))
#print(never_decreased(123789))

# submit(len(matched), day=4, part='a')

print(has_double(112233))
print(has_double(123444))
print(has_double(111122))

# submit(len(matched), day=4, part='b')
