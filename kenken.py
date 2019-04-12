
from tally.tally import *
import itertools
import functools

class Grid:
    def __init__(self, n):
        self.n = n
        self.clusters = []

    def add_cluster( self, op, value, tups):
        self.clusters.append( (op, value, tups))

    def semantic( self):
        for (op,value,tups) in self.clusters:
            for (x,y) in tups:
                assert 0 <= x < self.n
                assert 0 <= y < self.n

    @property
    def r( self):
        return list( range(1,self.n+1))
    

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
