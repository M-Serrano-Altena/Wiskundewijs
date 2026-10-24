"""Runs the solver for the oplosser view: solving, then building the Plotly traces."""

from __future__ import annotations

import traceback
from dataclasses import dataclass, field
from typing import Any

from src.Solver.src.solver.output import OutputLine
from src.Solver.src.solver.plotting import PlotTrace, generate_plot_data
from src.Solver.src.solver.solve_calculations import Solve
from src.Solver.src.solver.topics import Topic, find_topic

ANGLE_MODES: dict[str, bool | None] = {"automatic": None, "degrees": True, "radians": False}


@dataclass
class SolveResult:
    equation_text: str
    equation_interpret: str
    outputs: list[OutputLine]
    plot: bool
    # whether the solutions were found numerically (then there is no step-by-step explanation)
    numerical: bool
    plot_error: bool = False
    plot_data: list[PlotTrace] = field(default_factory=list)
    x_range: list[float] = field(default_factory=list)
    y_range: list[float] = field(default_factory=list)
    # the page on the site that explains how to solve this kind of equation
    topic: Topic | None = None


def solve_for_view(equation_text: str, angle_mode: str) -> SolveResult:
    solver = Solve(input_string=equation_text, use_degrees=ANGLE_MODES.get(angle_mode))
    equation_interpret, outputs, plot = solver.solve_equation()
    result = SolveResult(equation_text, equation_interpret, outputs, plot, solver.numerical)
    has_error = any("error" in (line[0] if isinstance(line, tuple) else line).casefold() for line in outputs)
    try:
        result.topic = find_topic(solver, has_error)
    except Exception:
        # a missing link isn't worth failing the whole answer for
        traceback.print_exc()

    if plot:
        try:
            plot_data, x_range, y_range = generate_plot_data(solver)
            result.plot_data = plot_data
            result.x_range = [float(value) for value in x_range]
            result.y_range = [float(value) for value in y_range]
        except Exception:
            traceback.print_exc()
            result.plot = False
            result.plot_error = True

    return result


def describe_for_explanation(result: SolveResult) -> Any:
    """What the explanation feature sends to ChatGPT: the input and the solver's output."""
    if result.numerical:
        return "numeriek"
    outputs = [tuple(line) if isinstance(line, tuple) else line for line in result.outputs]
    return {"equation_text": result.equation_text, "equation_interpret": result.equation_interpret, "outputs": outputs}
