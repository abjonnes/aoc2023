def run(lines, start_pos, start_dir):
    n_rows = len(lines)
    n_cols = len(lines[0])
    queue = [(start_pos, start_dir)]
    seen = set()
    while queue:
        next_ = queue.pop()
        (r, c), (dr, dc) = next_
        if next_ in seen or not (0 <= r < n_rows) or not (0 <= c < n_cols):
            continue
        seen.add(next_)

        char = lines[r][c]

        if char == "." or (char == "-" and dc) or (char == "|" and dr):
            queue.append(((r + dr, c + dc), (dr, dc)))
        if char == "-" and dr:
            queue.append(((r, c - 1), (0, -1)))
            queue.append(((r, c + 1), (0, 1)))
        if char == "|" and dc:
            queue.append(((r - 1, c), (-1, 0)))
            queue.append(((r + 1, c), (1, 0)))
        if char == "/":
            dr, dc = -dc, -dr
            queue.append(((r + dr, c + dc), (dr, dc)))
        if char == "\\":
            dr, dc = dc, dr
            queue.append(((r + dr, c + dc), (dr, dc)))

    return len(set(pos for pos, _ in seen))


def part1(lines):
    return run(lines, (0, 0), (0, 1))


def part2(lines):
    n_rows = len(lines)
    n_cols = len(lines[0])
    top = [((0, x), (1, 0)) for x in range(n_cols)]
    bottom = [((n_rows - 1, x), (-1, 0)) for x in range(n_cols)]
    left = [((x, 0), (0, 1)) for x in range(n_rows)]
    right = [((x, n_cols - 1), (0, -1)) for x in range(n_rows)]
    return max(run(lines, pos, dir_) for pos, dir_ in top + bottom + left + right)
