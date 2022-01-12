"""Tests for satis.py.

make test T=test_satis.py
"""
from . import TestBase  # MockSocket


class TestSatis(TestBase):
    """Tests satis module."""

    @staticmethod
    def test_get_string():
        """Call get_string function."""
        from satis import get_string

        assert get_string([True]) == '[true]'
