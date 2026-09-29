import unittest

from experiment.tests.support import allocator


class BoundaryGate(unittest.TestCase):
    def test_zero_total_and_zero_weights(self):
        allocate = allocator()
        self.assertEqual(allocate(0, [0, 0]), [0, 0])
        self.assertEqual(allocate(0, [1, 2]), [0, 0])
        self.assertEqual(allocate(3, [0, 1]), [0, 3])

    def test_indivisible_small_total(self):
        self.assertEqual(allocator()(1, [1, 1, 1]), [1, 0, 0])


if __name__ == "__main__":
    unittest.main()
