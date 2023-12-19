import collections


def run(instructions):
    r = c = trench_sum = 0

    rows = collections.defaultdict(list)
    cols = collections.defaultdict(list)

    # iterate through the instructions, keeping track of trench area
    for dir_, n in instructions:
        trench_sum += n

        dr = dc = 0
        match dir_:
            case "U":
                dr = -n
            case "D":
                dr = n
            case "L":
                dc = -n
            case "R":
                dc = n

        new_r = r + dr
        new_c = c + dc

        # keep track of the rows and columns we encounter
        if dir_ in "LR":
            rows[r].append(range(min(c, new_c), max(c, new_c) + 1))
        if dir_ in "UD":
            # for columns, the logic below requires that we trim the final row in the range, so that
            # we only encounter "columns" extending downward when we are on a row containing a "row"
            cols[c].append(range(min(r, new_r), max(r, new_r)))

        r = new_r
        c = new_c

    # we're assuming we're ending up where we started
    assert r == c == 0

    # for each row containing a "row," also add in an int of where a "column" crosses the row
    # the values are now both `range`s and `int`s - a "row" is a `range` and a "column" is an `int`
    for c, r_ranges in cols.items():
        for r, r_list in rows.items():
            for r_range in r_ranges:
                if r in r_range:
                    r_list.append(c)

    # for each row, sort the values so we can iterate pairwise through neighbors
    for list_ in rows.values():
        list_.sort(key=lambda x: (x.start if isinstance(x, range) else x, isinstance(x, range)))

    # need to iterate through rows in ascending order
    sorted_rows = sorted(rows.items())

    #################################
    ### calculating interior area ###
    #################################

    interior_sum = 0
    for (r, data), (next_r, _) in zip(sorted_rows, sorted_rows[1:]):
        # first, calculate interior area for rows _not_ in our structure. in these regions, it's
        # the sum of space between pairs of "columns," multiplied by the distance between rows
        cols_only = [x for x in data if isinstance(x, int)]

        for col_a, col_b in zip(cols_only[::2], cols_only[1::2]):
            interior_sum += (col_b - col_a - 1) * (next_r - r - 1)

        # now iterate over pairs of neighboring elements in a row
        n_cols = 0  # how many (downward-extending) columns we've crossed
        for pair_a, pair_b in zip(data, data[1:]):
            a_is_col = isinstance(pair_a, int)
            b_is_col = isinstance(pair_b, int)

            if a_is_col:
                n_cols += 1

            # if we've crossed an even number of downward-extending columns, we're outside - skip
            if n_cols % 2 == 0:
                continue

            # now just add up the space between ranges and/or columns on this row
            # the `max` logic helps out in cases where a "free" "column" is adjacent to a "row"
            interior_sum += max(
                0,
                (pair_b if b_is_col else pair_b.start)
                - (pair_a if a_is_col else pair_a.stop - 1)
                - 1,
            )

    # the total area is sum of trench area and interior area
    return interior_sum + trench_sum


def part1(lines):
    instructions = list()
    for line in lines:
        dir_, n, _ = line.split()
        instructions.append((dir_, int(n)))

    return run(instructions)


def part2(lines):
    dir_map = {"0": "R", "1": "D", "2": "L", "3": "U"}
    instructions = list()
    for line in lines:
        _, _, code = line.split()
        instructions.append((dir_map[code[7]], int(code[2:7], 16)))

    return run(instructions)
