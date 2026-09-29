import unittest

from experiment.tests.support import allocator


class ContractGate(unittest.TestCase):
    def test_output_shape_and_types(self):
        result = allocator()(7, [1, 2, 4])
        self.assertEqual(len(result), 3)
        self.assertTrue(all(type(value) is int for value in result))
        self.assertTrue(all(value >= 0 for value in result))

    def test_invalid_inputs_are_rejected_consistently(self):
        allocate = allocator()
        invalid = [
            (-1, [1]),
            (1, []),
            (1, [1, -1]),
            (1, [0, 0]),
            (True, [1]),
            (1, [True]),
        ]
        for total, weights in invalid:
            with self.subTest(total=total, weights=weights):
                with self.assertRaises(ValueError):
                    allocate(total, weights)


if __name__ == "__main__":
    unittest.main()
