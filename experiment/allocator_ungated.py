"""Plausible first-pass implementation: concise, readable, and lossy."""


def allocate_units(total: int, weights: list[int]) -> list[int]:
    """Allocate integer units in proportion to weights."""
    weight_sum = sum(weights)
    return [round(total * weight / weight_sum) for weight in weights]
