
from tally.tally import *
import itertools
import functools
import re

class Grid:
    def __init__(self, n):
        self.n = n
        self.clusters = []

    def add_cluster( self, op, value, tups):
        self.clusters.append( (op, value, tups))

    def semantic( self):
        raster = {}

        for idx,(op,value,tups) in enumerate(self.clusters):
            for (x,y) in tups:
                assert 0 <= x < self.n
                assert 0 <= y < self.n
                assert (x,y) not in raster
                raster[(x,y)] = idx
        
        for x in range(self.n):
            for y in range(self.n):
                assert (x,y) in raster

    @property
    def r( self):
        return list( range(1,self.n+1))
    

def run( g):
    g.semantic()
    
    s = Tally()

    matrix = {}
    for x in range(g.n):
        for y in range(g.n):
            matrix[(x,y)] = [ s.add_var() for i in range(g.n)]
            s.emit_exactly_one( matrix[(x,y)])


    for i in range(g.n):
        for x in range(g.n):
            s.emit_exactly_one( [ matrix[(x,y)][i] for y in range(g.n)])
        for y in range(g.n):
            s.emit_exactly_one( [ matrix[(x,y)][i] for x in range(g.n)])


    for (op,value,tups) in g.clusters:
        ok = []
        for q in itertools.product( g.r, repeat=len(tups)):
            if op == '+':
                if sum(q) == value:
                    ok.append( q)
            elif op == '*':
                if functools.reduce( lambda x,y: x*y, q) == value:
                    ok.append( q)
            elif op == '/':
                if q[0] * value == q[1] or q[1] * value == q[0]:
                    ok.append( q)
            elif op == '-':
                if q[0] + value == q[1] or q[1] + value == q[0]:
                    ok.append( q)
            else:
                assert False, op

# One of these must be true
        tmp = [s.add_var() for q in ok]
        s.add_clause( tmp)
        for q,t in zip(ok,tmp):
            qq = [ matrix[tup][i-1] for tup,i in zip(tups,q)]
            s.emit_and( qq, t)

    s.solve()

    assert s.state == 'SAT'

    print()
    for x in range(g.n):
        for y in range(g.n):
            print( [ i+1 for i in range(g.n) if s.h[matrix[(x,y)][i]]][0], end='')
        print()


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

    run(g)

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


    run(g)


def test_c():

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


    rr = r.split('\n')[1:-1]

    g = Grid( len(rr))

    assert all( [len(q) == g.n for q in rr])

    ee = e.split('\n')[1:-1]

    tbl2 = {}
    p = re.compile( r"^(\S)\s+(\d+)\s+(\S)\s*$")
    for q in ee:
        m = p.match( q)
        assert m is not None, q

        k = m.groups()[0]
        value = int(m.groups()[1])
        op = m.groups()[2]
                    
        assert k not in tbl2
        tbl2[k] = (op,value)

    tbl = {}

    for (x,q) in enumerate(rr):
        for (y,t) in enumerate(q):
            if t not in tbl:
                tbl[t] = []
            tbl[t].append( (x,y))

    for k in tbl2.keys():
        assert k in tbl

    for (k,lst) in tbl.items():
        assert k in  tbl2
        op, value = tbl2[k]
        g.add_cluster( op, value, lst)


    run(g)



