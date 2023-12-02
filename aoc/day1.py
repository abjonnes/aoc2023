import re


DIGITS = {str(n): str(n) for n in range(1, 10)}
WORDS = dict(
    one="1",
    two="2",
    three="3",
    four="4",
    five="5",
    six="6",
    seven="7",
    eight="8",
    nine="9",
)


def get_num(line, token_dict):
    # use lookahead matching so we get overlapping words
    digits = re.findall(f"(?=({'|'.join(token_dict)}))", line)
    return int(token_dict[digits[0]] + token_dict[digits[-1]])


def part1(lines):
    return sum(get_num(line, DIGITS) for line in lines)


def part2(lines):
    return sum(get_num(line, dict(**DIGITS, **WORDS)) for line in lines)
