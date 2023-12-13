import functools


def combinations(seq, groups):
    n_seq = len(seq)
    n_groups = len(groups)

    @functools.cache
    def process(seq_idx, group_idx, n_damaged):
        # process end of sequence - return 1 if we've used all the groups or if we're in the last
        # group and we have the correct number of damaged parts, otherwise 0
        if seq_idx == n_seq:
            return (group_idx == n_groups and not n_damaged) or (
                group_idx == n_groups - 1 and groups[group_idx] == n_damaged
            )

        result = 0

        if seq[seq_idx] in ".?":
            # not in a group
            if not n_damaged:
                result += process(seq_idx + 1, group_idx, 0)

            # at the end of a group - advance to next group and reset damage count
            elif group_idx < n_groups and groups[group_idx] == n_damaged:
                result += process(seq_idx + 1, group_idx + 1, 0)

            # at the end of a group but the count isn't right - dead end
            else:
                pass

        if seq[seq_idx] in "#?":
            # in the middle of a group - extend it
            result += process(seq_idx + 1, group_idx, n_damaged + 1)

        return result

    return process(0, 0, 0)


def run(lines, multiplier):
    result = 0
    for line in lines:
        seq, groups = line.split()
        seq = "?".join([seq] * multiplier)
        groups = [int(g) for g in groups.split(",")] * multiplier
        result += combinations(seq, groups)

    return result


def part1(lines):
    return run(lines, 1)


def part2(lines):
    return run(lines, 5)
