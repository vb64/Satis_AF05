"""Filtered Satis source."""


class Average:
    """Stream average filter."""

    def __init__(self, length):
        """Average for last length values."""
        if length < 1:
            raise ValueError("Filter length must be more than zero.")

        self.length = length
        self.data = []

    def put(self, val):
        """Add new value."""
        self.data.append(val)
        if len(self.data) > self.length:
            self.data.pop(0)

    def get(self):
        """Return filtered value."""
        return int(sum(self.data) / len(self.data))
