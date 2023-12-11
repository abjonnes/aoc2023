import itertools


def run(lines, multiplier):
    galaxies = [
        (r, c) for r, line in enumerate(lines) for c, char in enumerate(line) if char == "#"
    ]
    expanded_rows = set(range(len(lines))) - {r for r, _ in galaxies}
    expanded_cols = set(range(len(lines[0]))) - {c for _, c in galaxies}

    def get_distance(g1, g2):
        r1, c1 = g1
        r2, c2 = g2

        extra_rows = len(expanded_rows & set(range(min(r1, r2) + 1, max(r1, r2))))
        extra_cols = len(expanded_cols & set(range(min(c1, c2) + 1, max(c1, c2))))

        return (
            abs(r1 - r2)
            + extra_rows * (multiplier - 1)
            + abs(c1 - c2)
            + extra_cols * (multiplier - 1)
        )

    return sum(
        get_distance(galaxy1, galaxy2) for galaxy1, galaxy2 in itertools.combinations(galaxies, 2)
    )


def part1(lines):
    return run(lines, 2)


def part2(lines):
    return run(lines, 1000000)
