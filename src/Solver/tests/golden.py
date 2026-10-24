"""Record and compare the solver's output for the inputs in golden_inputs.py.

Record (only when the current output is known to be correct):
    PYTHONHASHSEED=0 python -m src.Solver.tests.golden --record

The comparison runs as a pytest test in test_golden.py.
"""

from __future__ import annotations

import io
import json
import multiprocessing
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np

GOLDEN_PATH = Path(__file__).with_name("golden_outputs.json")
TIMEOUT_SECONDS = 60
PLOT_SAMPLES = 40


def _sample(values: Any) -> list[float | None]:
    array = np.asarray(values, dtype=float).ravel()
    if array.size == 0:
        return []
    indices = np.linspace(0, array.size - 1, num=min(PLOT_SAMPLES, array.size)).astype(int)
    return [None if not np.isfinite(v) else round(float(v), 5) for v in array[indices]]


def _summarize_trace(trace: dict[str, Any]) -> dict[str, Any]:
    summary = {key: value for key, value in trace.items() if key not in ("x", "y")}
    summary["x_len"] = len(trace["x"])
    summary["x"] = _sample([v if v is not None else np.nan for v in trace["x"]])
    summary["y"] = _sample([v if v is not None else np.nan for v in trace["y"]])
    return summary


def run_solver(equation_text: str, angle_mode: str) -> dict[str, Any]:
    """Run an equation through the same steps as the oplosser view and summarize the result."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiskundewijs.settings")
    os.environ.setdefault("OPENAI_API_KEY", "test-key-not-used")
    from oplosser.solver_pipeline import solve_for_view

    result = solve_for_view(equation_text, angle_mode)
    return {
        "interpret": result.equation_interpret,
        "outputs": [list(o) if isinstance(o, tuple) else o for o in result.outputs],
        "plot": result.plot,
        "numerical": result.numerical,
        "plot_data": [_summarize_trace(trace) for trace in result.plot_data],
        "x_range": [round(float(v), 5) for v in result.x_range],
        "y_range": [round(float(v), 5) for v in result.y_range],
    }


def _worker(equation_text: str, angle_mode: str, queue: Any) -> None:
    try:
        queue.put(run_solver(equation_text, angle_mode))
    except Exception as error:  # the comparison only cares that it fails the same way
        queue.put({"exception": type(error).__name__})


def run_with_timeout(equation_text: str, angle_mode: str) -> dict[str, Any]:
    context = multiprocessing.get_context("spawn")
    queue = context.Queue()
    process = context.Process(target=_worker, args=(equation_text, angle_mode, queue))
    process.start()
    try:
        return queue.get(timeout=TIMEOUT_SECONDS)
    except Exception:
        return {"exception": "Timeout"}
    finally:
        process.join(timeout=5)
        if process.is_alive():
            process.kill()


def golden_key(equation_text: str, angle_mode: str) -> str:
    return f"{angle_mode} | {equation_text}"


def record() -> None:
    from src.Solver.tests.golden_inputs import GOLDEN_INPUTS

    results: dict[str, Any] = {}
    for equation_text, angle_mode in GOLDEN_INPUTS:
        key = golden_key(equation_text, angle_mode)
        results[key] = run_with_timeout(equation_text, angle_mode)
        print(key, "->", "exception" in results[key] and results[key]["exception"] or "ok", flush=True)

    GOLDEN_PATH.write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    if os.environ.get("PYTHONHASHSEED") != "0":
        sys.exit("Set PYTHONHASHSEED=0 so set ordering (and thus output order) is reproducible.")
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")  # the inputs contain π, ², ...
    if "--record" in sys.argv:
        record()
