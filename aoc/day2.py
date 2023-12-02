from collections import defaultdict
from math import prod


def get_maxes(cubes):
    maxes = defaultdict(int)
    for cube_part in cubes.split(";"):
        for info in cube_part.split(","):
            num, color = info.split()
            maxes[color] = max(maxes[color], int(num))
    return maxes


def part1(lines):
    limits = defaultdict(int)
    limits["red"] = 12
    limits["green"] = 13
    limits["blue"] = 14

    def parse_lines():
        for line in lines:
            game, cubes = line.strip().split(":")
            if all(max_ <= limits[color] for color, max_ in get_maxes(cubes).items()):
                _, game_number = game.split()
                yield int(game_number)

    return sum(parse_lines())


def part2(lines):
    return sum(prod(get_maxes(cubes).values()) for _, cubes in [line.split(":") for line in lines])
