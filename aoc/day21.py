import collections


def run(lines, steps):
    size = len(lines)
    start = next(
        (r, c) for r, line in enumerate(lines) for c, char in enumerate(line) if char == "S"
    )
    # the logic below depends on a set of assumptions enumerated here
    # essentially, we require that the number of steps is equal to some half-integer multiple of
    # the (square) map side length, so that we can calculate the accessible plots as a sum of full-
    # or half- explored maps (actually, the complement of half-explored map, which is the accessible
    # plots in the corners).
    assert size == len(lines[0])  # square map
    assert size % 2 == 1  # odd side length
    assert start == (size // 2, size // 2)  # start is in the center

    # clear sight lines in all directions
    assert all(char in "S." for char in lines[size // 2])
    assert all(char in "S." for char in [line[size // 2] for line in lines])

    # distance traveled is a half-integer multiple of the side length (either side of the half)
    assert (steps % size == size // 2) or (steps % size == size // 2 - 1)

    rocks = {(r, c) for r, line in enumerate(lines) for c, char in enumerate(line) if char == "#"}

    seen = dict()
    queue = collections.deque()
    queue.append((start, 0))
    while queue:
        (r, c), t = queue.popleft()
        if (r, c) in seen and seen[r, c] <= t:
            continue
        seen[r, c] = t
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_r = r + dr
            new_c = c + dc
            if (
                not (0 <= new_r < size and 0 <= new_c < size)
                or (new_r, new_c) in rocks
                or ((new_r, new_c) in seen and seen[new_r, new_c] <= t + 1)
            ):
                continue

            queue.append(((new_r, new_c), t + 1))

    full = {parity: sum((r + c) % 2 == parity for r, c in seen) for parity in (0, 1)}
    exterior = {
        parity: sum((r + c) % 2 == parity for (r, c), t in seen.items() if t > size // 2)
        for parity in (0, 1)
    }

    n = steps // size
    parity = steps % 2
    return (
        (n + 1) ** 2 * full[parity]
        + n**2 * full[not parity]
        - (n + 1) * exterior[parity]
        + n * exterior[not parity]
    )


def part1(lines):
    return run(lines, 64)


def part2(lines):
    return run(lines, 26501365)
