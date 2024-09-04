from dataclasses import dataclass
import itertools
import re


@dataclass
class Stone:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    def __init__(self, line):
        self.x, self.y, self.z, self.dx, self.dy, self.dz = [
            int(m) for m in re.findall(r"-?\d+", line)
        ]


def part1(lines):
    stones = [Stone(line) for line in lines]

    def collide(s1, s2):
        m1 = s1.dy / s1.dx
        m2 = s2.dy / s2.dx

        if m1 == m2:
            if m1 * s1.x + s1.y == m2 * s2.x + s2.y:
                raise Exception("Uh oh")
            return False

        x = (m1 * s1.x - s1.y - m2 * s2.x + s2.y) / (m1 - m2)
        y = m1 * (x - s1.x) + s1.y

        t1 = (x - s1.x) / s1.dx
        t2 = (x - s2.x) / s2.dx

        return (
            (200000000000000 <= x <= 400000000000000)
            and (200000000000000 <= y <= 400000000000000)
            and t1 >= 0
            and t2 >= 0
        )

    return sum(collide(s1, s2) for s1, s2 in itertools.combinations(stones, 2))


# Part 2
# Solved with SageMath using the first three stones:
#
# sage: x,y,z,a,b,c,t,u,v=var('x y z a b c t u v')
# sage: eq1 = x+a*t==230027994633462+103*t
# ....: eq2 = y+b*t==224850233272831-57*t
# ....: eq3 = z+c*t==164872865225455+285*t
# ....: eq4 = x+a*u==213762157019377+184*u
# ....: eq5 = y+b*u==204038908928791-110*u
# ....: eq6 = z+c*u==198113097692531+174*u
# ....: eq7 = x+a*v==236440979253526+15*v
# ....: eq8 = y+b*v==104012423941037+694*v
# ....: eq9 = z+c*v==223798957622735-277*v
# sage: solve([eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9], x, y, z, a, b, c, t, u,
# ....:  v)
# [[x == 231279746486542, y == 131907658181641, z == 195227847662645, a == 99, b == 240, c == 188, t == 312937963270, u == 206089287849, v == 61443247226]]
#
# The sum of x, y and z is 558415252330828
