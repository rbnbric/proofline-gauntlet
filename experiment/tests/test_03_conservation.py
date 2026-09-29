import itertools
import unittest

from experiment.tests.support import allocator


class ConservationGate(unittest.TestCase):
    def test_no_units_are_lost_or_created(self):
        allocate = allocator()
        violations = []
        cases = 0
        for length in range(1, 5):
            for weights in itertools.product(range(5), repeat=length):
                if not any(weights):
                    continue
                for total in range(26):
                    cases += 1
                    result = allocate(total, list(weights))
                    if sum(result) != total:
                        violations.append((total, weights, result, sum(result)))
                        if len(violations) == 5:
                            break
                if len(violations) == 5:
                    break
            if len(violations) == 5:
                break
        self.assertFalse(
            violations,
            f"conservation failed; first violations={violations}; cases examined={cases}",
        )


if __name__ == "__main__":
    unittest.main()
