"""Console client stuff.

make test T=test_console.py
"""
import os

from . import TestBase


class TestConsole(TestBase):
    """Tests console client."""

    def test_noargs(self):
        """Call without args."""
        from source.cli import main

        assert main([], self.options) == 1
