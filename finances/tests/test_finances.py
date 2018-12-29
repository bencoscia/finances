"""
Unit and regression test for the finances package.
"""

# Import package, test suite, and other packages as needed
import finances
import pytest
import sys

def test_finances_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "finances" in sys.modules
