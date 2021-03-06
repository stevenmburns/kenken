
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
        """
        Check if raster contains only h/v adjacent connections
        Illegal
        ac 
        ba

        Legal
        ab
        aa

        Solution: build a graph (edges say vertices are locally adjacent)
        and use a cheap Union-Find (no path compression) to check connectivity
"""
        def check_connected( k, vertices, edges):
            dads = {}
            for p in vertices:
                dads[p] = p

            def Find( c):
                while c != dads[c]:
                    c = dads[c]
                return c

            def Union( p, q):
                dads[Find(p)] = Find(q)

            for p,q in edges:
                Union( p, q)

            stuff = set([ Find(p) for (k,p) in dads.items()])
            assert len(stuff) == 1, "More than one partition"

        vertices = collections.defaultdict( list)
        for p in itertools.product( range(self.n), repeat=2):
            vertices[self.raster[p]].append( p)

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

        for (k,v) in vertices.items():
            check_connected( k, v, connections[k])

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


        communitive_ops = {
            '+': lambda x,y: x+y,
            '*': lambda x,y: x*y
        }

        non_communitive_ops = {
            '-': lambda x,y: x+y,
            '/': lambda x,y: x*y
        }

        for (op,value,tups) in self.clusters:
            def pred( q):
                if op in communitive_ops:
                    f = communitive_ops[op]
                    return functools.reduce( f, q) == value
                elif op in non_communitive_ops:
                    f = non_communitive_ops[op]
                    return f(q[0], value) == q[1] or f(q[1], value) == q[0]
                else:
                    assert False, op

            ok = [q for q in itertools.product( self.r, repeat=len(tups))
                    if pred(q)]
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


