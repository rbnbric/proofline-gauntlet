import unittest

from experiment.tests.support import allocator


class DeterminismGate(unittest.TestCase):
    def test_repeated_calls_and_tie_policy(self):
        allocate = allocator()
        expected = [2, 2, 1]
        observed = [allocate(5, [1, 1, 1]) for _ in range(20)]
        self.assertTrue(all(result == expected for result in observed), observed[:3])


if __name__ == "__main__":
    unittest.main()
