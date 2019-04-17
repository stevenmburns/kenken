
from kenken.kenken import *
import pytest


def test_bad_singletons():

    r = """
ac
ba
"""

    e = """
a 2 +
b 2 +
c 2 +
"""

    with pytest.raises( AssertionError, match='More than one partition'):
        Grid.parse_and_run( r, e)

def test_bad_separated():

    r = """
aba
aba
aba
"""

    e = """
a 12 +
b 6 +
"""

    with pytest.raises( AssertionError, match='More than one partition'):
        Grid.parse_and_run( r, e)

def test_bad2():
    
    r = """
a
"""

    e = """
a 2 &
"""
    
    with pytest.raises( AssertionError, match='&'):
        Grid.parse_and_run( r, e)
