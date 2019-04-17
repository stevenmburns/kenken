
from kenken.kenken import *


def test_monday_small():

    r = """
accg
adfg
bbff
beef
"""

    e = """
a 1 -
b 4 *
c 3 +
d 3 +
e 7 +
f 9 +
g 2 /
"""

    Grid.parse_and_run( r, e)

def test_monday_large():

    r = """
affkmm
bggknq
bchhnq
ccilor
ddilos
eejjps
"""

    e = """
a 2 +
b 5 -
c 100 *
d 2 /
e 3 /
f 5 -
g 7 +
h 1 -
i 3 /
j 30 *
k 20 *
l 3 /
m 2 -
n 5 +
o 11 +
p 2 +
q 3 /
r 3 +
s 5 +
"""

    Grid.parse_and_run( r, e)

def test_tuesday_small():

    r = """
aadd
baee
bcff
ccfg
"""

    e = """
a 8 *
b 7 +
c 6 *
d 2 -
e 2 /
f 8 *
g 3 +
"""

    Grid.parse_and_run( r, e)

def test_tuesday_large():

    r = """
aefiim
aefjmm
bbfjnp
bbggnp
cchkoo
dchlll
"""

    e = """
a 2 /
b 60 *
c 8 *
d 5 +
e 4 -
f 12 *
g 11 +
h 3 /
i 2 /
j 3 +
k 5 +
l 72 *
m 100 *
n 5 -
o 3 /
p 1 -
"""

    Grid.parse_and_run( r, e)
