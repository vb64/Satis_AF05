"""Console client stuff.

make test T=test_console.py
"""
from . import TestBase, MockSocket


class TestConsole(TestBase):
    """Tests console client."""

    def test_nodata(self):
        """Call CLI main."""
        import cli

        saved_websocket = cli.websocket.WebSocket
        saved_read = cli.read

        cli.websocket.WebSocket = MockSocket
        cli.read = lambda socket, start, end, rbw, vid, att: []

        assert cli.main([], self.options) == 0

        self.options.with_data = True
        assert cli.main([], self.options) == 0

        cli.read = saved_read
        cli.websocket.WebSocket = saved_websocket
