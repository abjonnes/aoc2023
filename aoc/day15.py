import functools
import re


@functools.cache
def get_idx(name):
    return sum(ord(char) * 17**idx for idx, char in enumerate(reversed(name), start=1)) % 256


def part1(data):
    return sum(get_idx(token) for token in data.strip().split(","))


def part2(data):
    def parse_token(token):
        m = re.match(r"(\w+)[-=]((?<==)\d+)?", token)
        name, op = m.groups()
        return get_idx(name), name, int(op) if op else None

    dicts = [dict() for _ in range(256)]
    for token in data.strip().split(","):
        idx, name, op = parse_token(token)
        if op is not None:
            dicts[idx][name] = op
        else:
            dicts[idx].pop(name, None)

    return sum(
        box_idx * sum(lens_idx * lens for lens_idx, lens in enumerate(box.values(), start=1))
        for box_idx, box in enumerate(dicts, start=1)
    )
