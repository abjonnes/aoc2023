from functools import reduce
import itertools
import re

from egcd import egcd


def parse_map(lines):
    map_ = dict()
    for line in lines:
        a, _, _, _, b, _, c, _ = re.split(r"[ =\(,\)]", line)
        map_[a] = {"L": b, "R": c}

    return map_


def part1(lines):
    instructions = itertools.cycle(lines[0])
    map_ = parse_map(lines[2:])

    loc = "AAA"
    for step, instruction in enumerate(instructions, start=1):
        loc = map_[loc][instruction]
        if loc == "ZZZ":
            return step


def part2(lines):
    map_ = parse_map(lines[2:])

    periods = list()
    offsets = list()

    def get_period_and_offsets(loc):
        seen = dict()
        new_offsets = list()
        for step, (instruction_idx, instruction) in enumerate(
            itertools.cycle(enumerate(lines[0])), start=1
        ):
            loc = map_[loc][instruction]
            if loc.endswith("Z"):
                new_offsets.append(step)
            if (loc, instruction_idx) in seen:
                periods.append(step - seen[loc, instruction_idx])
                offsets.append(new_offsets)
                return
            seen[loc, instruction_idx] = step

    def calculate(data1, data2):
        """Essentially finding greatest common divisor with offsets."""
        period1, offset1 = data1
        period2, offset2 = data2

        gcd, s, _ = egcd(period1, period2)
        lcm = period1 * period2 // gcd

        assert (offset1 - offset2) % gcd == 0
        m = s * (offset1 - offset2) // gcd

        output = (m * period1 - offset1) % lcm
        if not output:
            output = lcm

        return output, -output % lcm

    for loc in map_:
        if not loc.endswith("A"):
            continue
        get_period_and_offsets(loc)

    return min(
        reduce(calculate, zip(periods, offset_combination))
        for offset_combination in itertools.product(*offsets)
    )[0]
