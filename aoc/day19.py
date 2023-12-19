import collections
import math
import re


def build_graph(workflow_data):
    """Builds a returns a graph of the workflows. The edges between workflows contain the valid
    ranges for each score type.
    """
    edges = collections.defaultdict(list)
    for plan in workflow_data.split():
        m = re.match(r"(\w+)\{(.+)\}", plan)
        name = m.group(1)

        # start with all valid score values
        ranges = {score: range(1, 4001) for score in "xmas"}

        for score, comparison, value, target in re.findall(
            r"(?:([xmas])([<>])(\d+):)?(\w+)", m.group(2)
        ):
            if value:
                value = int(value)

            # make a copy of the ranges for the edge to the new node before we modify them
            edge_ranges = dict(ranges)

            # step through each comparison in the workflow, adding any restriction to the new edge
            # ranges, and its _complement_ to the current set of ranges
            match comparison:
                case ">":
                    edge_ranges[score] = range(
                        max((value + 1, ranges[score].start)), ranges[score].stop
                    )
                    ranges[score] = range(ranges[score].start, min((value + 1, ranges[score].stop)))
                case "<":
                    edge_ranges[score] = range(
                        ranges[score].start, min((value, ranges[score].stop))
                    )
                    ranges[score] = range(max((value, ranges[score].start)), ranges[score].stop)
                case _:
                    pass

            edges[name].append((edge_ranges, target))

    return edges


def part1(data):
    workflow_data, part_data = data.split("\n\n")
    edges = build_graph(workflow_data)

    parts = [
        {score: int(value) for score, value in re.findall(r"([xmas])=(\d+)", part)}
        for part in part_data.split()
    ]

    def recurse(name, part):
        if name == "A":
            return sum(part.values())
        if name == "R":
            return 0

        for edge_ranges, edge_name in edges[name]:
            if all(part[score] in edge_range for score, edge_range in edge_ranges.items()):
                return recurse(edge_name, part)

    return sum(recurse("in", part) for part in parts)


def part2(data):
    workflow_data, _ = data.split("\n\n")
    edges = build_graph(workflow_data)

    def combine_ranges(ranges1, ranges2):
        new_ranges = dict()
        for score in "xmas":
            r1 = ranges1[score]
            r2 = ranges2[score]
            new_ranges[score] = range(max((r1.start, r2.start)), min((r1.stop, r2.stop)))
        return new_ranges

    def recurse(name, ranges):
        if name == "A":
            return math.prod(len(r) for r in ranges.values())
        if name == "R":
            return 0

        return sum(
            recurse(edge_name, combine_ranges(ranges, edge_ranges))
            for edge_ranges, edge_name in edges[name]
        )

    ranges = {score: range(1, 4001) for score in "xmas"}
    return recurse("in", ranges)
