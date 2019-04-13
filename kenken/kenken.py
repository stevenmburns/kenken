
from tally.tally import *
import itertools
import functools
import collections
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
                    pass
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

#
# Check that there is only one solution
#
    assumption = []
    for x in range(g.n):
        for y in range(g.n):
            for i in range(g.n):
                var = matrix[(x,y)][i]
                model = s.h[var]
                if model:
                    assumption.append( -var)
                else:
                    assumption.append(  var)


    s.add_clause( assumption)

    s.solve()
    assert s.state == 'UNSAT'

def parse_and_run( r, e):
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

    tbl = collections.defaultdict( list)
    for (x,q) in enumerate(rr):
        for (y,t) in enumerate(q):
            tbl[t].append( (x,y))

    for k in tbl2.keys():
        assert k in tbl

    for (k,lst) in tbl.items():
        assert k in  tbl2
        op, value = tbl2[k]
        g.add_cluster( op, value, lst)

#
# Check that the clusters are connected
#
    def check_connected( k, lst):
        dads = {}
        for p,q in lst:
            dads[p],dads[q] = p,q

        def Find( c):
            while c != dads[c]:
                c = dads[c]
            return c

        def Union( p, q):
            dads[Find(p)] = Find(q)

        for p,q in lst:
            Union( p, q)

        assert len(set([ Find(p) for (k,p) in dads.items()])) == 1


    def X():
        for x in range(g.n-1):
            for y in range(g.n):
                yield (x,y),(x+1,y)

    def Y():
        for x in range(g.n):
            for y in range(g.n-1):
                yield (x,y),(x,y+1)

    raster = {}
    for (x,q) in enumerate(rr):
        for (y,t) in enumerate(q):
            raster[(x,y)] = t

    connections = collections.defaultdict( list)
    for (p,q) in itertools.chain( X(), Y()):
        if raster[p] == raster[q]:
            connections[raster[p]].append( ( p, q))

    for (k,lst) in connections.items():
        check_connected( k, lst)


#
# Setup and run the solver
#
    run(g)


