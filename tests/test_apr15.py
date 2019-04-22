
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


def test_saturday_large():

    r = """
adhiin
adhjln
aeejlo
bbejmo
cfffmp
cggkkp
"""

    e = """
a 12 +
b 3 -
c 2 /
d 1 -
e 10 *
f 15 +
g 3 -
h 6 *
i 2 /
j 24 *
k 2 /
l 15 *
m 2 -
n 3 -
o 3 /
p 2 -
"""

    Grid.parse_and_run( r, e)


def test_saturday_small():

    r = """
adff
aeef
bbef
ccgg
"""

    e = """
a 5 +
b 4 +
c 5 +
d 4 +
e 9 +
f 8 +
g 5 +
"""

    Grid.parse_and_run( r, e)


def test_sunday_large():

    r = """
aeeenno
affjooo
bgjjpss
bgklqtv
ccklqtw
dhhmmuw
diimrrw
"""

    e = """
a 5 -
b 2 -
c 6 +
d 3 /
e 90 *
f 1 -
g 2 -
h 2 -
i 1 -
j 10 +
k 3 -
l 5 -
m 13 +
n 2 /
o 9 +
p 7 +
q 2 /
r 1 -
s 3 -
t 2 /
u 7 +
v 3 +
w 18 +
"""

    Grid.parse_and_run( r, e)

def test_sunday_small():

    r = """
aagii
bdhjj
behkm
ceekm
cffll
"""

    e = """
a 3 -
b 2 /
c 2 -
d 5 +
e 7 +
f 2 -
g 5 +
h 6 *
i 1 -
j 5 +
k 2 -
l 2 /
m 4 -
"""

    Grid.parse_and_run( r, e)

