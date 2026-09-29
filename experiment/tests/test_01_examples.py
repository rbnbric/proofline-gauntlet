import unittest

from experiment.tests.support import allocator


class ExampleGate(unittest.TestCase):
    def test_familiar_examples(self):
        allocate = allocator()
        self.assertEqual(allocate(10, [1, 1]), [5, 5])
        self.assertEqual(allocate(12, [1, 2, 3]), [2, 4, 6])
        self.assertEqual(allocate(9, [1, 2]), [3, 6])


if __name__ == "__main__":
    unittest.main()
