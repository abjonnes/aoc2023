from collections import defaultdict
import itertools


def dfs(graph, node=0, target=1, seen=None, weight=0):
    """Basic search algorithm to yield weights along every path to the target."""
    if node == target:
        yield weight
        return

    if seen is None:
        seen = set()

    seen = seen | {node}
    for neighbor, dw in graph[node]:
        if neighbor in seen:
            continue
        yield from dfs(graph, neighbor, target, seen, weight + dw + 1)  # +1 to account for node


def parse_map(lines):
    """Build a graph where each node is an "intersection" and the edge weights are the distances
    between intersections.
    """
    dir_map = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}

    # target is in a fixed location
    target = (len(lines) - 1, len(lines[0]) - 2)

    seen = set()
    node_counter = itertools.count()
    nodes = dict()
    queue = list()

    # start node
    nodes[next(node_counter)] = (0, 1)
    seen.add((0, 1))
    # row, col, node originating this path, current weight
    queue.append((1, 1, 0, 0))

    while queue:
        r, c, start_node, weight = queue.pop()
        seen.add((r, c))

        if (r, c) == target:
            yield start_node, next(node_counter), weight
            continue

        node_dir = dir_map.get(lines[r][c])
        if weight > 0 and node_dir:
            # we're at an intersection
            dr, dc = node_dir
            node_r, node_c = r + dr, c + dc
            if (node_r, node_c) not in nodes:
                # if this is the first time coming to this intersection, label it
                nodes[node_r, node_c] = next(node_counter)

        # if at an intersection, yield the edge if we're not somehow back to where we started
        if (r, c) in nodes:
            if start_node == nodes[r, c]:
                continue
            yield start_node, nodes[r, c], weight
            start_node = nodes[r, c]
            weight = -1  # will be incremented to 0 on the next iteration

        # add neighbors to queue
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            symbol = lines[r + dr][c + dc]
            if (
                symbol == "#"  # wall
                or (r + dr, c + dc) in seen - set(nodes)  # we've been here before (unless node)
                or not (symbol == "." or dir_map[symbol] == (dr, dc))  # wrong direction
            ):
                continue
            queue.append((r + dr, c + dc, start_node, weight + 1))


def run(lines, add_edge):
    graph = defaultdict(list)

    # build the graph and keep track of which nodes we've seen as "from" and as "to" to find the
    # target node
    from_nodes = set()
    to_nodes = set()
    for u, v, weight in parse_map(lines):
        add_edge(graph, u, v, weight)
        from_nodes.add(u)
        to_nodes.add(v)

    target = next(iter(to_nodes - from_nodes))

    return max(dfs(graph, target=target))


def part1(lines):
    def add_edge(graph, u, v, weight):
        # directed graph
        graph[u].append((v, weight))

    return run(lines, add_edge)


def part2(lines):
    def add_edge(graph, u, v, weight):
        # undirected graph
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    return run(lines, add_edge)
