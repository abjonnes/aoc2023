from collections import defaultdict
import re


def parse_graph(lines):
    graph = defaultdict(dict)

    for line in lines:
        source, *nodes = re.split(r"[ :]+", line)
        for node in nodes:
            graph[source][node] = 1
            graph[node][source] = 1

    return graph


def find_most_tightly_connected(graph, node_set):
    """Return a node which has the greatest sum of edge wait to nodes in `node_set`."""
    counts = defaultdict(int)

    for node in node_set:
        for neighbor, weight in graph[node].items():
            if neighbor in node_set:
                continue
            counts[neighbor] += weight

    return max(counts, key=counts.get)


def merge_nodes(graph, node1, node2):
    """Merge two nodes together and update all the edges."""
    new_node = f"{node1},{node2}"

    new_neighbors = defaultdict(int)

    for neighbor, weight in graph[node1].items():
        if neighbor == node2:
            continue
        new_neighbors[neighbor] += weight
    for neighbor, weight in graph[node2].items():
        if neighbor == node1:
            continue
        new_neighbors[neighbor] += weight

    new_graph = {new_node: dict(new_neighbors)}
    for node, neighbors in graph.items():
        if node in (node1, node2):
            continue
        new_weight = neighbors.pop(node1, 0) + neighbors.pop(node2, 0)
        if new_weight:
            neighbors[new_node] = new_weight
        new_graph[node] = neighbors

    return new_graph


def iterate(graph, start):
    n = len(graph)
    node_set = {start}
    node_path = [start]

    # add all nodes to a set in order of tightly-connectedness
    for _ in range(n - 1):
        new_node = find_most_tightly_connected(graph, node_set)
        node_set.add(new_node)
        node_path.append(new_node)

    # return the sum of the edge weights for the last node that was added to the set, as well as
    # the final two nodes which will be merged
    weight = sum(graph[node_path[-1]].values())
    return weight, node_path[-2], node_path[-1]


def part1(lines):
    graph = parse_graph(lines)
    start = lines[0][:3]

    min_weight = float("inf")
    n = n_cut = len(graph)

    while len(graph) > 1:
        weight, s, t = iterate(graph, start)

        # if the weight for this iteration is minimum, that's the min cut
        if weight < min_weight:
            min_weight = weight
            # for a min cut, the nodes that were merged to form the final node constitute one side
            # of the cut
            n_cut = t.count(",") + 1

        graph = merge_nodes(graph, s, t)

    return n_cut * (n - n_cut)
