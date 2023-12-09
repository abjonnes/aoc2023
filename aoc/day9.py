import math


def predict(seq, end):
    """Lagrange interpolating polynomial."""
    l = len(seq)
    return sum(
        round(y * math.prod(((l if end else -1) - k) / (x - k) for k in range(l) if k != x))
        for x, y in enumerate(seq)
    )


def run(lines, end):
    return sum(predict([int(x) for x in line.split()], end) for line in lines)


def part1(lines):
    return run(lines, True)


def part2(lines):
    return run(lines, False)
