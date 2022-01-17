"""Console client stuff.

make test T=test_console.py
"""
from . import TestBase, MockSocket


class TestConsole(TestBase):
    """Tests console client."""

    def test_wrong(self):
        """Call read command."""
        import cli

        assert cli.main([], self.options) == 1
        assert cli.main(["wrong_command"], self.options) == 1

    def test_sweep(self):
        """Call sweep command."""
        import cli

        saved_websocket = cli.websocket.WebSocket
        saved_sweep = cli.sweep

        cli.websocket.WebSocket = MockSocket
        cli.sweep = lambda socket, start, rbw, vid, att: []

        assert cli.main([cli.Command.Sweep], self.options) == 0

        cli.sweep = saved_sweep
        cli.websocket.WebSocket = saved_websocket

    def test_read(self):
        """Call read command."""
        import cli

        saved_websocket = cli.websocket.WebSocket
        saved_read = cli.read

        cli.websocket.WebSocket = MockSocket
        cli.read = lambda socket, start, end, rbw, vid, att: []

        assert cli.main([cli.Command.Read], self.options) == 0

        self.options.with_data = True
        assert cli.main([cli.Command.Read], self.options) == 0

        cli.read = saved_read
        cli.websocket.WebSocket = saved_websocket
