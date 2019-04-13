
from kenken.kenken import *


def test_a():

    g = Grid(4)
    g.add_cluster( '/',  2, [(0,0),(1,0)])
    g.add_cluster( '+',  6, [(2,0),(3,0),(2,1)])
    g.add_cluster( '*', 12, [(0,1),(0,2)])
    g.add_cluster( '-',  2, [(1,1),(1,2)])
    g.add_cluster( '/',  2, [(3,1),(3,2)])
    g.add_cluster( '+',  1, [(2,2)])
    g.add_cluster( '-',  1, [(0,3),(1,3)])
    g.add_cluster( '-',  1, [(2,3),(3,3)])

    g.run()

def test_a1():
    r = """
accg
addg
bbfh
beeh
"""

    e = """
a 2 / 
b 6 +
c 12 *
d 2 -
e 2 /
f 1 +
g 1 -
h 1 -
"""

    Grid.parse_and_run( r, e)

def test_b():

    g = Grid(6)
    g.add_cluster( '*', 36, [(0,0),(1,0),(2,0)])
    g.add_cluster( '-',  4, [(3,0),(4,0)])
    g.add_cluster( '+',  4, [(5,0)])

    g.add_cluster( '+', 11, [(0,1),(0,2)])
    g.add_cluster( '/',  2, [(1,1),(1,2)])
    g.add_cluster( '/',  2, [(2,1),(3,1)])
    g.add_cluster( '*', 15, [(4,1),(5,1)])
    g.add_cluster( '-',  2, [(2,2),(3,2)])
    g.add_cluster( '-',  1, [(4,2),(4,3)])
    g.add_cluster( '/',  2, [(5,2),(5,3)])

    g.add_cluster( '-',  4, [(0,3),(1,3)])
    g.add_cluster( '+', 12, [(2,3),(2,4),(2,5)])
    g.add_cluster( '/',  2, [(3,3),(3,4)])

    g.add_cluster( '/',  2, [(0,4),(0,5)])
    g.add_cluster( '/',  3, [(1,4),(1,5)])
    g.add_cluster( '*', 60, [(4,4),(5,4),(5,5)])

    g.add_cluster( '*',  6, [(3,5),(4,5)])


    g.run()




def test_b1():

    r = """
addkoo
aeekpp
afhlll
bfhmmq
bgiinq
cgjjnn
"""

    e = """
a 36 *
b  4 -
c  4 +
d 11 +
e  2 /
f  2 /
g 15 *
h  2 -
i  1 -
j  2 /
k  4 -
l 12 +
m  2 /
n 60 *
o  2 /
p  3 /
q  6 *
"""
    Grid.parse_and_run( r, e)

def test_c1():

    r = """
adddkl
aafdkl
bbfhhm
cbgiim
cbgijn
ceejjn
"""

    e = """
a 15 +
b 90 *
c  8 *
d 16 *
e  1 -
f 11 +
g  3 /
h  4 -
i 11 +
j 12 +
k  2 -
l  3 /
m  1 -
n  3 /
"""
    Grid.parse_and_run( r, e)

def test_d1():

    r = """
aaeg
bdeg
bcfh
ccfh
"""

    e = """
a 5 +
b 5 +
c 9 +
d 1 +
e 7 +
f 3 +
g 5 +
h 5 +
"""
    Grid.parse_and_run( r, e)



