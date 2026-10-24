"""Compare the solver's output with the output recorded in golden_outputs.json.

When a change to the output is intended, re-record with:
    PYTHONHASHSEED=0 python -m src.Solver.tests.golden --record
and check the diff of golden_outputs.json before committing it.
"""

import json
import math
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pytest

from src.Solver.tests.golden import GOLDEN_PATH, golden_key, run_with_timeout
from src.Solver.tests.golden_inputs import GOLDEN_INPUTS


@pytest.fixture(scope="module")
def actual_outputs() -> dict[str, Any]:
    # the solver processes are spawned with this environment, which makes set ordering reproducible
    os.environ["PYTHONHASHSEED"] = "0"
    with ThreadPoolExecutor(max_workers=max(1, (os.cpu_count() or 2) - 1)) as pool:
        results = pool.map(lambda case: run_with_timeout(*case), GOLDEN_INPUTS)
        return {golden_key(*case): result for case, result in zip(GOLDEN_INPUTS, results)}


@pytest.fixture(scope="module")
def expected_outputs() -> dict[str, Any]:
    return json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))


def assert_matches(actual: Any, expected: Any, path: str = "") -> None:
    if isinstance(expected, float) and isinstance(actual, (int, float)):
        assert math.isclose(actual, expected, rel_tol=1e-4, abs_tol=1e-4), f"{path}: {actual} != {expected}"
    elif isinstance(expected, dict) and isinstance(actual, dict):
        assert actual.keys() == expected.keys(), f"{path}: keys {sorted(actual)} != {sorted(expected)}"
        for key in expected:
            assert_matches(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list) and isinstance(actual, list):
        assert len(actual) == len(expected), f"{path}: {actual} != {expected}"
        for index, (actual_item, expected_item) in enumerate(zip(actual, expected)):
            assert_matches(actual_item, expected_item, f"{path}[{index}]")
    else:
        assert actual == expected, f"{path}: {actual!r} != {expected!r}"


@pytest.mark.parametrize("equation_text, angle_mode", GOLDEN_INPUTS)
def test_output_matches_golden(
    equation_text: str, angle_mode: str, actual_outputs: dict[str, Any], expected_outputs: dict[str, Any]
) -> None:
    key = golden_key(equation_text, angle_mode)
    assert_matches(actual_outputs[key], expected_outputs[key], key)
