"""Implementation shaped by the full deterministic conformance contract."""


def _plain_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def allocate_units(total: int, weights: list[int]) -> list[int]:
    """Allocate every unit proportionally with stable largest-remainder ties."""
    if not _plain_int(total) or total < 0:
        raise ValueError("total must be a non-negative integer")
    if not isinstance(weights, list) or not weights:
        raise ValueError("weights must be a non-empty list")
    if any(not _plain_int(weight) or weight < 0 for weight in weights):
        raise ValueError("weights must contain non-negative integers")

    weight_sum = sum(weights)
    if weight_sum == 0:
        if total == 0:
            return [0] * len(weights)
        raise ValueError("positive total requires at least one positive weight")

    allocations = [(total * weight) // weight_sum for weight in weights]
    remainders = [(total * weight) % weight_sum for weight in weights]
    units_left = total - sum(allocations)

    # Larger fractional remainders receive leftover units. Original position is
    # the explicit, stable tie-break rule.
    priority = sorted(range(len(weights)), key=lambda index: (-remainders[index], index))
    for index in priority[:units_left]:
        allocations[index] += 1
    return allocations
