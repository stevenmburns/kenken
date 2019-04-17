# kenken
[![CircleCI](https://circleci.com/gh/stevenmburns/kenken.svg?style=svg)](https://circleci.com/gh/stevenmburns/kenken)

KenKen solver using SAT

Requires the "tally" Python package from "ALIGN-analoglayout/ALIGN-public/Pysat

Or use docker (to build and run the unit tests):
```bash
docker build -t kenken_image .
docker run -t kenken_image bash -c "source general/bin/activate && cd kenken && python setup.py test"
```

## Game Specification
Here is an example game specifications. (You can add a new game as a new test in the `tests` subdirectory.)
You specify the clusters using a raster of single characters.
I usually start in the upper left hand corner and then go down and then to the right.
Then you specify the mathematical constraint for that cluster using the space separated triple:

`<cluster character> <number> <operator>`. 

For a singleton cluster, use either `+` or `*` as the operator. (See `d` below.)
```python
from kenken.kenken import *

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
```
