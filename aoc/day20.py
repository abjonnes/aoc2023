import collections
import itertools
import math


class Node:
    def __init__(self, string):
        name, _, children_str = string.split(" ", maxsplit=2)
        children = children_str.split(", ")
        if name.startswith(("%", "&")):
            name = name[1:]

        self.name = name
        self.children = children
        self.parents = list()

    def set_parent(self, parent):
        self.parents.append(parent.name)


class Broadcast(Node):
    def input(self, high, _):
        for child in self.children:
            yield (child, self.name, high)


class FlipFlop(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on = False

    def input(self, high, _):
        if high:
            return

        self.on = not self.on
        for child in self.children:
            yield (child, self.name, self.on)


class Conjunction(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_inputs = dict()

    def set_parent(self, parent, *args, **kwargs):
        super().set_parent(parent, *args, **kwargs)
        self.last_inputs[parent.name] = False

    def input(self, high, parent):
        self.last_inputs[parent] = high
        output = not all(self.last_inputs.values())
        for child in self.children:
            yield (child, self.name, output)


def build_graph(lines):
    nodes = list()

    for line in lines:
        class_ = Broadcast
        if line.startswith("%"):
            class_ = FlipFlop
        elif line.startswith("&"):
            class_ = Conjunction

        nodes.append(class_(line))

    node_map = {node.name: node for node in nodes}

    for node in nodes:
        for child in node.children:
            if child in node_map:
                node_map[child].set_parent(node)

    return node_map


def part1(lines):
    node_map = build_graph(lines)

    pulse_counts = {False: 0, True: 0}
    pulses = collections.deque()
    for _ in range(1000):
        pulses.append(("broadcaster", None, False))

        while pulses:
            node, parent, high = pulses.popleft()
            pulse_counts[high] += 1

            if node in node_map:
                pulses.extend(node_map[node].input(high, parent))

    return math.prod(pulse_counts.values())


def part2(lines):
    """This part relies on manual inspection of the graph to notice that there are four similar
    strongly connected components which the `broadcaster` node has edges to. Each of these acts as a
    counter which increments on a low pulse input and emits a single low pulse when the counter hits
    a specific value, and a single high pulse on every other input. These four counters each pass
    through an inverter, and then to a single conjunction node which emits a low pulse to the target
    node, `rx`, when each counter has each its specific value at the same time.

    The key to this part is to identify each of the four counters' specific value, and return the
    LCM of these values.

    Each counter consists of a number of FlipFlop nodes which act as bits that encode the current
    count as a binary number. Some of these bits have edges to a central conjunction node; when all
    of those bits are "on," the counter emits its low pulse and resets its bits back to "off." If we
    identify which bits have edges to the conjunction node, we can determine the specific value for
    the counter.
    """
    node_map = build_graph(lines)

    def find_value(node):
        value = 0

        # the first bit always has an edge to the conjunction node
        conjunction_node = next(
            child for child in node_map[node].children if isinstance(node_map[child], Conjunction)
        )

        for idx in itertools.count():
            if conjunction_node in node_map[node].children:
                value += 1 << idx

            others = [child for child in node_map[node].children if child != conjunction_node]

            if not others:
                return value

            (node,) = others

    return math.lcm(*[find_value(counter) for counter in node_map["broadcaster"].children])
