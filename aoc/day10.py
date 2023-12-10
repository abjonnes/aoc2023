def process_map(lines):
    """Process the map by finding the loop of pipe which contains the starting position, and return
    a dictionary of loop pipe tile positions to the type of pipe tile.
    """
    dir_opps = {"N": "S", "S": "N", "W": "E", "E": "W"}
    dir_deltas = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}

    direction_map = {
        "|": "NS",
        "-": "EW",
        "L": "NE",
        "J": "NW",
        "7": "SW",
        "F": "SE",
    }

    # for each position, store a dictionary of a pair of entrance-exit directions for the pipe
    map_directions = dict()

    start_r = start_c = 0
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "S":
                start_r, start_c = r, c

            if char not in direction_map:
                continue

            dir1, dir2 = direction_map[char]

            map_directions[r, c] = {dir1: dir2, dir2: dir1}

    start_dirs = list(
        dir_
        for dir_, (dr, dc) in dir_deltas.items()
        if (start_r + dr, start_c + dc) in map_directions
        and dir_opps[dir_] in map_directions[start_r + dr, start_c + dc]
    )
    start_tile_type = next(
        tile
        for tile, directions in direction_map.items()
        if sorted(start_dirs) == sorted(directions)
    )

    curr_r, curr_c = start_r, start_c
    next_dir = start_dirs[0]
    pipe_tiles = {(start_r, start_c): start_tile_type}

    while True:
        dr, dc = dir_deltas[next_dir]
        curr_r += dr
        curr_c += dc

        if (curr_r, curr_c) == (start_r, start_c):
            break

        pipe_tiles[curr_r, curr_c] = lines[curr_r][curr_c]
        next_dir = map_directions[curr_r, curr_c][dir_opps[next_dir]]

    return pipe_tiles


def part1(lines):
    pipe_tiles = process_map(lines)
    return len(pipe_tiles) // 2


def part2(lines):
    """Scan each row, keeping track of whether we're inside or outside of the loop by paying
    attention to when we cross the pipe.
    """

    pipe_tiles = process_map(lines)

    n_rows = len(lines)
    n_cols = len(lines[0])

    count = 0

    for r in range(n_rows):
        # we start outside the loop from the west
        inside = False

        for c in range(n_cols):
            pipe_tile = pipe_tiles.get((r, c))

            if not pipe_tile:
                count += inside

            # `|` is trivially crossing a pipe
            # otherwise, if we encounter pipes which lead to us running parallel along the pipe,
            # count a crossing when a pipe extends to the north (chosen arbitrarily), since by the
            # time we read the next pipeless tile, if we've passed an odd number off those tiles,
            # we've crossed from inside to out or vice versa
            elif pipe_tile in "|LJ":
                inside = not inside

    return count
