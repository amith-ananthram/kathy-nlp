import time
from collections import Counter


class Timer:
    def __init__(self, logger=print):
        self._current_key = None
        self._current_start = None
        self.mins = {}
        self.maxes = {}
        self.averages = {}
        self.counts = Counter()
        self.logger = logger

    def clock_start(self, key):
        assert self._current_key is None or self._current_key == key
        assert self._current_start is None
        self._current_key = key
        self._current_start = time.perf_counter()

    def clock_end(self):
        assert self._current_key is not None
        assert self._current_start is not None

        elapsed = (time.perf_counter() - self._current_start) * 1000
        if self._current_key not in self.mins \
                or self._current_key not in self.maxes \
                or self._current_key not in self.averages:
            self.mins[self._current_key] = elapsed
            self.maxes[self._current_key] = elapsed
            self.averages[self._current_key] = elapsed
        else:
            self.mins[self._current_key] = min(self.mins[self._current_key], elapsed)
            self.maxes[self._current_key] = max(self.maxes[self._current_key], elapsed)
            self.averages[self._current_key] = \
                ((self.averages[self._current_key] * self.counts[self._current_key]) + elapsed) / (self.counts[self._current_key] + 1)
        self.counts[self._current_key] += 1

        self._current_key = None
        self._current_start = None

    def __call__(self, key):
        self._current_key = key
        return self

    def __enter__(self):
        self.clock_start(self._current_key)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clock_end()

    def log(self):
        output_lines = []
        for key in sorted(self.mins.keys() | self.maxes.keys() | self.averages.keys() | self.counts.keys()):
            output_lines.append("%s: min=%0.3fms, max=%0.3fms, avg=%0.3fms, count=%s" % (
                key, self.mins[key], self.maxes[key], self.averages[key], self.counts[key]
            ))

        self.logger('PROFILER STATS')
        for output_line in output_lines:
            self.logger(output_line)