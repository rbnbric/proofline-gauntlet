import time
import unittest

from experiment.tests.support import allocator


class EfficiencyGate(unittest.TestCase):
    def test_representative_workload(self):
        allocate = allocator()
        weights = list(range(1, 129))
        started = time.perf_counter()
        for _ in range(5_000):
            allocate(100_003, weights)
        elapsed = time.perf_counter() - started
        self.assertLess(elapsed, 2.0, f"representative workload took {elapsed:.3f}s")


if __name__ == "__main__":
    unittest.main()
