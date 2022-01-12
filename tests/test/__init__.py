"""Root class for testing."""
from unittest import TestCase


class MockSocket:
    """Mocked websocket."""

    def __init__(self):
        """Instance."""
        self.addr = None
        self.last_text = None
        self.answers = []

    def connect(self, addr):
        """Connect to address."""
        self.addr = addr

    def send(self, text):
        """Write string to socket."""
        self.last_text = text

    def recv(self):
        """Return string from socket."""
        return self.answers.pop()

    def close(self):
        """Close instance."""
        self.addr = None


class TestBase(TestCase):
    """Base class for tests."""

    def setUp(self):
        """Init tests."""
        TestCase.setUp(self)

        from source.cli import PARSER
        self.options, _args = PARSER.parse_args(args=[])
