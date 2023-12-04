def matches(card):
    _, numbers = card.split(":")
    winning, chosen = numbers.split("|")
    return len(set(winning.split()) & set(chosen.split()))


def part1(lines):
    def score(card):
        n_matches = matches(card)
        if not n_matches:
            return 0
        return 2 ** (n_matches - 1)

    return sum(score(line) for line in lines)


def part2(lines):
    copies = [1] * len(lines)
    for idx, line in enumerate(lines):
        n_matches = matches(line)
        for new_copy_idx in range(idx + 1, idx + 1 + n_matches):
            copies[new_copy_idx] += copies[idx]

    return sum(copies)
