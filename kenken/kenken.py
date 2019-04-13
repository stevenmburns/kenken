
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
        self.raster = {}

        for idx,(op,value,tups) in enumerate(self.clusters):
            for (x,y) in tups:
                assert 0 <= x < self.n
                assert 0 <= y < self.n
                assert (x,y) not in self.raster
                self.raster[(x,y)] = idx
        
        for x in range(self.n):
            for y in range(self.n):
                assert (x,y) in self.raster

        self.clusters_connected()

    @property
    def r( self):
        return list( range(1,self.n+1))
    
    def clusters_connected( self):
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
            for x in range(self.n-1):
                for y in range(self.n):
                    yield (x,y),(x+1,y)

        def Y():
            for x in range(self.n):
                for y in range(self.n-1):
                    yield (x,y),(x,y+1)

        connections = collections.defaultdict( list)
        for (p,q) in itertools.chain( X(), Y()):
            if self.raster[p] == self.raster[q]:
                connections[self.raster[p]].append( ( p, q))

        for (k,lst) in connections.items():
            check_connected( k, lst)

    def run( self):
        self.semantic()

        s = Tally()

        matrix = {}
        for x in range(self.n):
            for y in range(self.n):
                matrix[(x,y)] = [ s.add_var() for i in range(self.n)]
                s.emit_exactly_one( matrix[(x,y)])


        for i in range(self.n):
            for x in range(self.n):
                s.emit_exactly_one( [ matrix[(x,y)][i] for y in range(self.n)])
            for y in range(self.n):
                s.emit_exactly_one( [ matrix[(x,y)][i] for x in range(self.n)])


        for (op,value,tups) in self.clusters:
            ok = []
            for q in itertools.product( self.r, repeat=len(tups)):
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

            ands = [s.add_var() for q in ok]
            s.add_clause( ands)
            for q,a in zip(ok,ands):
                s.emit_and( [ matrix[tup][i-1] for tup,i in zip(tups,q)], a)

        s.solve()

        assert s.state == 'SAT'

        print()
        for x in range(self.n):
            for y in range(self.n):
                print( [ i+1 for i in range(self.n) if s.h[matrix[(x,y)][i]]][0], end='')
            print()

        self.check_single_solution( s, matrix)

    def check_single_solution( self, s, matrix):
        assumption = []
        for x in range(self.n):
            for y in range(self.n):
                for i in range(self.n):
                    var = matrix[(x,y)][i]
                    model = s.h[var]
                    if model:
                        assumption.append( -var)
                    else:
                        assumption.append(  var)


        s.add_clause( assumption)

        s.solve()
        assert s.state == 'UNSAT'

    @staticmethod
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

        g.run()


