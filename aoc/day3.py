import re


def parse_numbers(lines):
    """Return a list of (number, position_set) tuples where number is the part number and
    position_set is a set of all coordinates either occupied by the part number itself, or are
    adjacent to the part number. (We're only interested in the adjacent positions, but including the
    occupied positions here doesn't cause any problems since there'll never be a part at those
    positions.)
    """
    numbers = list()
    for idx, line in enumerate(lines):
        for m in re.finditer(r"\d+", line):
            start, end = m.span()
            pos_set = {(idx + dr, x) for dr in (-1, 0, 1) for x in range(start - 1, end + 1)}
            numbers.append((int(m.group(0)), pos_set))
    return numbers


def part1(lines):
    numbers = parse_numbers(lines)
    symbols = {
        (r, c)
        for r, line in enumerate(lines)
        for c, char in enumerate(line)
        if not char.isnumeric() and char != "."
    }
    return sum(number for number, positions in numbers if positions & symbols)


def part2(lines):
    numbers = parse_numbers(lines)
    gear_parts = [
        [number for number, positions in numbers if (r, c) in positions]
        for r, line in enumerate(lines)
        for c, char in enumerate(line)
        if char == "*"
    ]
    return sum(p[0] * p[1] for p in gear_parts if len(p) == 2)
