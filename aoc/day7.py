from collections import Counter


def run(lines, card_ranks, hand_scorer):
    def hand_strength_key(line):
        hand, _ = line
        # rank first by the hand's score, then by the ranks of the individual cards (in order of
        # appearance)
        return (hand_scorer(hand),) + tuple(card_ranks.index(card) for card in hand)

    data = [line.split() for line in lines]
    return sum(
        idx * int(value)
        for idx, (_, value) in enumerate(sorted(data, key=hand_strength_key), start=1)
    )


def part1(lines):
    def hand_scorer(hand):
        """Hand scoring works as follows: count the number of each card present, then order the
        counts from high to low in a sequence. Each type of hand corresponds to a different such
        sequence, and the sequence ordering is the same as the ordering of hands by strength.

        In order of decreasing hand strength (note that the tuples are also in decreasing order):
        (5,)             Five of a kind
        (4, 1)           Four of a kind
        (3, 2)           Full house
        (3, 1, 1)        Three of a kind
        (2, 2, 1)        Two pair
        (2, 1, 1, 1)     One pair
        (1, 1, 1, 1, 1)  High card
        """
        return tuple(count for _, count in Counter(hand).most_common())

    card_ranks = [str(x) for x in range(2, 10)] + ["T", "J", "Q", "K", "A"]

    return run(lines, card_ranks, hand_scorer)


def part2(lines):
    def hand_scorer(hand):
        """Hand scoring works similarly to that in part 1, but we first exclude jokers from the
        count. Then, we can always generate the strongest hand by making those jokers become
        whichever card we already have the most of, so adding the number of jokers to the first
        element of the count sequence gives us the strongest hand possible.
        """
        counts = [count for card, count in Counter(hand).most_common() if card != "J"]

        # OOPS! ALL JOKERS! (five of a kind)
        if not counts:
            counts = [5]

        # add in any jokers
        counts[0] += 5 - sum(counts)

        return tuple(counts)

    card_ranks = ["J"] + [str(x) for x in range(2, 10)] + ["T", "Q", "K", "A"]

    return run(lines, card_ranks, hand_scorer)
