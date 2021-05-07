import time
import threading
from collections import Counter


class Timer:
    def __init__(self, logger=print):
        self._current_keys = {}
        self._current_starts = {}

        self.mins = {}
        self.maxes = {}
        self.averages = {}
        self.counts = Counter()
        self.logger = logger
        self.lock = threading.Lock()

    def clock_start(self, key):
        with self.lock:
            thread_id = threading.get_ident()
            assert thread_id not in self._current_keys or self._current_keys[thread_id] == key
            assert thread_id not in self._current_starts
            self._current_keys[thread_id] = key
            self._current_starts[thread_id] = time.perf_counter()

    def clock_end(self):
        with self.lock:
            thread_id = threading.get_ident()
            assert thread_id in self._current_keys
            assert thread_id in self._current_starts

            _current_key = self._current_keys[thread_id]
            _current_start = self._current_starts[thread_id]

            elapsed = (time.perf_counter() - _current_start) * 1000
            if _current_key not in self.mins \
                    or _current_key not in self.maxes \
                    or _current_key not in self.averages:
                self.mins[_current_key] = elapsed
                self.maxes[_current_key] = elapsed
                self.averages[_current_key] = elapsed
            else:
                self.mins[_current_key] = min(self.mins[_current_key], elapsed)
                self.maxes[_current_key] = max(self.maxes[_current_key], elapsed)
                self.averages[_current_key] = \
                    ((self.averages[_current_key] * self.counts[_current_key]) + elapsed) / (
                                self.counts[_current_key] + 1)
            self.counts[_current_key] += 1

            del self._current_keys[thread_id]
            del self._current_starts[thread_id]

    def __call__(self, key):
        with self.lock:
            thread_id = threading.get_ident()
            self._current_keys[thread_id] = key
        return self

    def __enter__(self):
        thread_id = threading.get_ident()
        self.clock_start(self._current_keys[thread_id])

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clock_end()

    def log(self, logger=None):
        output_lines = []
        with self.lock:
            for key in sorted(self.mins.keys() | self.maxes.keys() | self.averages.keys() | self.counts.keys()):
                output_lines.append("%s: min=%0.3fms, max=%0.3fms, avg=%0.3fms, count=%s" % (
                    key, self.mins[key], self.maxes[key], self.averages[key], self.counts[key]
                ))

        if not logger:
            logger = self.logger

        logger('PROFILER STATS')
        for output_line in output_lines:
            logger(output_line)
