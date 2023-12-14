import itertools


def rotate(map_, n=1):
    for _ in range(n):
        map_ = tuple(zip(*reversed(map_)))
    return map_


def process_row(row):
    result = ""
    count = 0
    last = 0
    for idx, char in enumerate(row):
        if char == "O":
            count += 1
        if char == "#":
            spots = idx - last
            result += "." * (spots - count) + "O" * count + "#"
            last = idx + 1
            count = 0
    spots = idx - last + 1
    result += "." * (spots - count) + "O" * count
    return result


def roll_right(map_):
    return tuple(process_row(row) for row in map_)


def load(map_):
    return sum(idx * row.count("O") for idx, row in enumerate(reversed(map_), start=1))


def part1(lines):
    map_ = roll_right(rotate(lines))
    return load(rotate(map_, 3))


def part2(lines):
    map_ = tuple(lines)
    seen = dict()
    for idx in itertools.count():
        if idx % 4 == 0:
            if map_ in seen:
                first = seen[map_]
                last = idx // 4
                break
            seen[map_] = idx // 4
        map_ = roll_right(rotate(map_))

    period = last - first
    target_idx = (1000000000 - first) % period + first
    target_map = next(k for k, v in seen.items() if v == target_idx)
    return load(target_map)
