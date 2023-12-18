import heapq


def run(lines, allowed_dirs, min_straight=0):
    lines = [[int(x) for x in line] for line in lines]

    # min-heap where the elements are:
    #  1. heat loss prior to moving into next tile (used for ranking)
    #  2. (row, column) position of next tile
    #  3. (delta row, delta column) of how we got to the next tile
    #  4. number of straight steps we've taken to get to the next tile
    heap = [(0, (1, 0), (1, 0), 1), (0, (0, 1), (0, 1), 1)]

    target = (len(lines) - 1, len(lines[0]) - 1)
    seen = set()

    while heap:
        loss, (r, c), (dir_r, dir_c), n_straight = heapq.heappop(heap)

        # add in the heat loss for this tile
        loss += lines[r][c]

        # if we're required to move at least some number of tiles straight ahead, make sure we've
        # satified that minimum before reporting success
        if (r, c) == target and n_straight >= min_straight:
            return loss

        # keep track of states we've seen before
        if ((r, c), (dir_r, dir_c), n_straight) in seen:
            continue
        seen.add(((r, c), (dir_r, dir_c), n_straight))

        for dr, dc, new_straight in allowed_dirs(dir_r, dir_c, n_straight):
            # for each in-bounds allowed direction, add that new tile to the heap
            if (0 <= r + dr <= target[0]) and (0 <= c + dc <= target[1]):
                heapq.heappush(heap, (loss, (r + dr, c + dc), (dr, dc), new_straight))


def part1(lines):
    def allowed_dirs(dir_r, dir_c, n_straight):
        # always allow turns
        if dir_r:
            yield 0, 1, 1
            yield 0, -1, 1
        else:
            yield 1, 0, 1
            yield -1, 0, 1

        # only allow straight ahead if we haven't moved straight already for too long
        if n_straight < 3:
            yield dir_r, dir_c, n_straight + 1

    return run(lines, allowed_dirs)


def part2(lines):
    def allowed_dirs(dir_r, dir_c, n_straight):
        # allow _only_ straight if we hanve't moved 4 yet
        if n_straight < 4:
            yield dir_r, dir_c, n_straight + 1
            return

        # allow turns otherwise
        if dir_r:
            yield 0, 1, 1
            yield 0, -1, 1
        else:
            yield 1, 0, 1
            yield -1, 0, 1

        # allow straight if we haven't straight already for too long
        if n_straight < 10:
            yield dir_r, dir_c, n_straight + 1

    return run(lines, allowed_dirs, 4)
