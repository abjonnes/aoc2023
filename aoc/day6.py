import math


def valid_times(time, record):
    """Calculate the number of button-holding times that result in beating the record. This amounts
    to solving a quadratic equation and calculating the difference in solutions (accounting for
    integer solutions!).
    """
    min_ = (time - math.sqrt(time**2 - 4 * record)) / 2
    min_int = math.ceil(min_)
    if min_ == min_int:
        min_int += 1

    max_ = (time + math.sqrt(time**2 - 4 * record)) / 2
    max_int = math.floor(max_)
    if max_ == max_int:
        max_int -= 1

    return max_int - min_int + 1


def part1(lines):
    races = zip((int(x) for x in lines[0].split()[1:]), (int(x) for x in lines[1].split()[1:]))

    return math.prod(valid_times(*race) for race in races)


def part2(lines):
    time = int("".join(lines[0].split()[1:]))
    record = int("".join(lines[1].split()[1:]))

    return valid_times(time, record)
