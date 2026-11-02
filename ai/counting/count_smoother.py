from collections import deque


class CountSmoother:
    """
    Smooths crowd counts using a moving average.
    """

    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.counts = deque(maxlen=window_size)

    def update(self, count: int) -> int:

        self.counts.append(count)

        average = sum(self.counts) / len(self.counts)

        return round(average)