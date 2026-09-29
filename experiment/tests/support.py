"""Load the implementation selected by the gauntlet runner."""

import importlib
import os


def allocator():
    # Direct test discovery verifies the corrected implementation. The
    # gauntlet runner always overrides this value for controlled comparisons.
    module_name = os.environ.get(
        "ALLOCATOR_IMPL", "experiment.allocator_conformant"
    )
    return importlib.import_module(module_name).allocate_units
