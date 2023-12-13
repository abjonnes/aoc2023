def find_horizontal_mirror(map_, differences):
    n_rows = len(map_)
    for i in range(n_rows - 1):
        if (
            sum(
                sum(a != b for a, b in zip(map_[i - j], map_[i + 1 + j]))
                for j in range(min(i + 1, n_rows - i - 1))
            )
            == differences
        ):
            return i + 1


def score(map_, differences):
    result = find_horizontal_mirror(map_, differences)
    if result is not None:
        return 100 * result
    return find_horizontal_mirror(list(zip(*map_)), differences)


def run(data, differences):
    maps = [segment.split("\n") for segment in data.strip().split("\n\n")]
    return sum(score(map_, differences) for map_ in maps)


def part1(data):
    return run(data, 0)


def part2(data):
    return run(data, 1)
