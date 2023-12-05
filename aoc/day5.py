from functools import total_ordering


@total_ordering
class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def map(self, new_start, old_start, len_):
        """Method to "map" an interval according to the given map data. It returns a tuple where the
        first element is a list of remaining unmapped intervals (i.e. parts of this interval which
        were unaffected by the current map), and the second element is a mapped interval, or `None`.
        """
        old_end = old_start + len_ - 1
        delta = new_start - old_start

        # break the mapping operation down according to various cases

        # interval is either entirely upstream or entirely downstream of the current map
        if self.end < old_start or old_end < self.start:
            return [self], None

        # interval is entirely contained within the current map
        if old_start <= self.start and self.end <= old_end:
            return list(), Interval(self.start + delta, self.end + delta)

        # map is entirely contained within interval
        if self.start < old_start and old_end < self.end:
            return [
                Interval(self.start, old_start - 1),
                Interval(old_end + 1, self.end),
            ], Interval(old_start + delta, old_end + delta)

        # the first part of this interval is outside of the map, but the second part is mapped
        if self.start < old_start and self.end <= old_end:
            return [Interval(self.start, old_start - 1)], Interval(
                old_start + delta, self.end + delta
            )

        # the first part of this interval is mapped, but the second part is outside of the map
        if old_start <= self.start and old_end < self.end:
            return [Interval(old_end + 1, self.end)], Interval(
                self.start + delta, old_start - 1 + delta
            )

        raise RuntimeError("We shouldn't have gotten here!")

    def __eq__(self, other):
        return (self.start, self.end) == (other.start, other.end)

    def __lt__(self, other):
        return (self.start, self.end) < (other.start, other.end)

    def __repr__(self):
        return f"<Interval: {self.start}-{self.end}>"


def parse_data(data):
    seed_str, rest = data.split("\n", 1)
    seed_ints = [int(seed) for seed in seed_str.split()[1:]]

    maps = list()
    for map_ in rest.split("\n\n"):
        map_data = list()
        for line in map_.strip().split("\n")[1:]:
            dest, src, len_ = [int(x) for x in line.split()]
            map_data.append((dest, src, len_))
        maps.append(map_data)

    return seed_ints, maps


def run(intervals, maps):
    for map_ in maps:
        done_intervals = list()
        pending_intervals = intervals

        for map_data in map_:
            new_pending_intervals = list()

            for interval in pending_intervals:
                new_pending, done = interval.map(*map_data)
                new_pending_intervals.extend(new_pending)

                if done:
                    done_intervals.append(done)

            pending_intervals = new_pending_intervals

        # any remaining pending intervals lies outside of any map given in the data, and so are
        # unmapped
        intervals = done_intervals + pending_intervals

    return min(intervals).start


def part1(data):
    seed_ints, maps = parse_data(data)
    intervals = [Interval(start, start) for start in seed_ints]

    return run(intervals, maps)


def part2(data):
    seed_ints, maps = parse_data(data)
    intervals = [
        Interval(start, start + len_ - 1) for start, len_ in zip(seed_ints[::2], seed_ints[1::2])
    ]

    return run(intervals, maps)
