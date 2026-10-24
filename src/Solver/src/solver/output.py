"""The lines of output the solver produces, which the oplosser view turns into HTML.

An output line is either a LaTeX string, or a (text, options) tuple for plain text.
"""

from __future__ import annotations

from typing import TypedDict


class OutputOptions(TypedDict, total=False):
    latex: bool
    # True for one line break before the line, or the number of line breaks
    new_line: bool | int


OutputLine = str | tuple[str, OutputOptions]

# (interpreted equation, output lines, whether to plot)
SolveOutput = tuple[str, list[OutputLine], bool]


def text(message: str, new_line: bool | int | None = None) -> tuple[str, OutputOptions]:
    """A line of plain text (not LaTeX)."""
    options: OutputOptions = {"latex": False}
    if new_line is not None:
        options["new_line"] = new_line
    return message, options


def append_to_last(output: list[OutputLine], latex: str) -> None:
    """Add LaTeX to the last output line, which must be a LaTeX line."""
    last = output[-1]
    if isinstance(last, tuple):
        raise TypeError("Can only add LaTeX to a LaTeX output line")
    output[-1] = last + latex
