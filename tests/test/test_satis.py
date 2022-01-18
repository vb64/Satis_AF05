"""Tests for satis.py.

make test T=test_satis.py
"""
import pytest
from . import TestBase, MockSocket


class TestSatis(TestBase):
    """Tests satis module."""

    @staticmethod
    def test_get_string():
        """Call get_string function."""
        from satis import get_string

        assert get_string([True]) == '[true]'

    @staticmethod
    def test_sweep():
        """Call sweep function."""
        from satis import sweep, Rbw, Attenuation, Key

        socket = MockSocket()
        socket.connect('testsweep')
        socket.answers.append({
          Key.Data: [1, 2],
        })

        assert sweep(socket, 100, Rbw.Hz6400, 100, Attenuation.Db0)

    @staticmethod
    def test_read():
        """Call read function."""
        from satis import read, Rbw, Attenuation, Key, Error

        socket = MockSocket()
        socket.connect('test')
        socket.answers.append({
          Key.First: 3,
          Key.Data: [4, 5],
        })
        socket.answers.append({
          Key.Total: 5,
          Key.First: 0,
          Key.Data: [1, 2, 3],
        })

        assert read(socket, 100, 150, Rbw.Hz6400, 100, Attenuation.Db0, True) is None

        socket.answers.append({
          Key.First: 0,
          Key.Data: [4, 5],
        })
        socket.answers.append({
          Key.Total: 5,
          Key.First: 0,
          Key.Data: [1, 2, 3],
        })

        with pytest.raises(Error) as exp:
            read(socket, 100, 150, Rbw.Hz6400, 100, Attenuation.Db0, False)
        assert "Error: index " in str(exp)

        socket.close()
