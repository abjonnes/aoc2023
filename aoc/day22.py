import collections
import dataclasses
import functools
import itertools
import operator


@dataclasses.dataclass
class Block:
    xy: set[tuple[int, int]]
    bottom_z: int
    height: int
    label: int

    def __init__(self, string, label):
        self.label = label

        start, end = string.split("~")
        x1, y1, z1 = [int(t) for t in start.split(",")]
        x2, y2, z2 = [int(t) for t in end.split(",")]

        self.xy = set(
            itertools.product(
                range(min(x1, x2), max(x1, x2) + 1), range(min(y1, y2), max(y1, y2) + 1)
            )
        )

        self.bottom_z = min(z1, z2)
        self.height = abs(z1 - z2) + 1


def run(lines):
    """Parse the blocks from the input and calculate a graph of blocks and which other blocks they
    support.
    """
    n_blocks = len(lines)
    blocks = [Block(line, idx) for idx, line in enumerate(lines)]
    all_xy = set().union(*[block.xy for block in blocks])

    forward_edges = [list() for _ in range(n_blocks)]
    reverse_edges = [list() for _ in range(n_blocks)]

    # calculate which blocks are "adjacent" in each column, ignoring any space between blocks for
    # now
    for xy in all_xy:
        col_blocks = sorted(
            [block for block in blocks if xy in block.xy], key=operator.attrgetter("bottom_z")
        )

        for block1, block2 in zip(col_blocks, col_blocks[1:]):
            forward_edges[block1.label].append(block2.label)
            reverse_edges[block2.label].append(block1.label)

    # perform topological sort
    topo_sort = list()
    edges = [list(l) for l in reverse_edges]
    s = set(idx for idx, edges in enumerate(reverse_edges) if not edges)
    while s:
        block = s.pop()
        topo_sort.append(block)
        for neighbor in forward_edges[block]:
            edges[neighbor].remove(block)
            if not edges[neighbor]:
                s.add(neighbor)

    # calculate final z-coordinate for each block
    settled_z = [1] * n_blocks
    for block in topo_sort:
        top = settled_z[block] + blocks[block].height
        for neighbor in forward_edges[block]:
            if settled_z[neighbor] < top:
                settled_z[neighbor] = top

    # use z-coordinates to determine which blocks are supported by which
    settled_graph = {
        block: {
            neighbor
            for neighbor in forward_edges[block]
            if settled_z[block] + blocks[block].height == settled_z[neighbor]
        }
        for block in reversed(topo_sort)
    }

    return {block.label for block in blocks}, settled_graph


def part1(lines):
    _, supporters = run(lines)

    # which blocks are directly supported by more than one other block?
    multiply_supported = {
        block
        for block, count in collections.Counter(
            itertools.chain.from_iterable(supporters.values())
        ).items()
        if count > 1
    }

    # count how many blocks are supporting other blocks which themselves are supported by more than
    # one block
    return sum(supporting_blocks <= multiply_supported for supporting_blocks in supporters.values())


def part2(lines):
    blocks, supporters = run(lines)
    supported_by = {block: set() for block in blocks}
    for block, supported_blocks in supporters.items():
        for supported_block in supported_blocks:
            supported_by[supported_block].add(block)

    @functools.cache
    def enumerate_paths(block):
        """Recursive function which returns a list of block paths to the ground for a given
        block.
        """
        # base case: if on the ground (no supporting blocks), return an "empty" path
        if not supported_by[block]:
            return [set()]

        result = list()
        for supporter in supported_by[block]:
            result.extend({supporter} | path for path in enumerate_paths(supporter))

        return result

    # if a supporting block appears in every path for a given block, the given block will be
    # disrupted if the supporting block were to disappear, so we simply count all those occurrences
    return sum(len(set(blocks).intersection(*enumerate_paths(block))) for block in blocks)
