"""The links from the oplosser's answers to the pages that explain them."""

from pathlib import Path

import pytest

from src.Solver.src.solver import topics
from src.Solver.src.solver.solve_calculations import Solve

BUILT_SITE = Path(__file__).parents[3] / "docs" / "static" / "mkdocs_build"


def page_html(page: str) -> str:
    """The built HTML of a page, including the sections that pages like goniometrie load later."""
    html = (BUILT_SITE / page / "index.html").read_text(encoding="utf-8")
    sections = BUILT_SITE / "main_sections" / page
    if sections.is_dir():
        html += "".join(path.read_text(encoding="utf-8") for path in sections.glob("*/index.html"))
    return html


@pytest.mark.parametrize("topic", topics.ALL_TOPICS, ids=lambda topic: topic.title)
def test_link_points_to_an_existing_section(topic: topics.Topic) -> None:
    # if this fails, a page or heading was renamed: update the url in topics.py
    page, _, anchor = topic.url.strip("/").partition("/#")
    html = page_html(page)
    if anchor:
        assert f'id="{anchor}"' in html


@pytest.mark.parametrize("equation, angle_mode, expected", [
    ("2x + 1 = 9", None, topics.LINEAIRE_VERGELIJKING),
    ("2x^2 + 1 = 9", None, topics.KWADRATISCH_X2_C),
    ("x^2 + 4x = 0", None, topics.KWADRATISCH_X2_BX),
    ("x^2 - 5x + 6 = 0", None, topics.KWADRATISCH_X2_BX_C),
    ("y = x^2 - 4", None, topics.SNIJPUNTEN_X_AS),
    ("2y - 4x = 8", None, topics.FORMULES_OMSCHRIJVEN),
    ("2x + 1 < 7", None, topics.LINEAIRE_ONGELIJKHEID),
    ("x^2 >= 4", None, topics.KWADRATISCHE_ONGELIJKHEID),
    ("sin(x) = 0.5", None, topics.GONIOMETRISCHE_VERGELIJKING),
    ("sin(x) = 0.5", True, topics.GONIOMETRISCHE_VERGELIJKING),
    ("2^x = 8", None, topics.LOGARITMES),
    ("log(8, 2)", None, topics.LOGARITMES),
    ("diff(x^2 + 3x)", None, topics.AFGELEIDE),
    ("diff(x^2 - 4x) = 0", None, topics.EXTREME_WAARDES),
    ("integrate(x^2)", None, topics.PRIMITIEVE),
    ("integrate(x^2, (0, 1))", None, topics.INTEGRAAL),
    ("x + y = 10; x - y = 2", None, topics.STELSELS),
])
def test_topic(equation: str, angle_mode: bool | None, expected: topics.Topic) -> None:
    solver = Solve(equation, angle_mode)
    solver.solve_equation()
    assert topics.find_topic(solver) == expected


@pytest.mark.parametrize("equation", [
    "cos(x) = x",                   # solved numerically
    "x^5 - 3x + 1 = 0",             # no method taught at school
    "matrix([1,2], [3,4]) * matrix([1,0], [0,1])",
    "vect(1,2) + vect(3,4)",
    "x^2 + y^2 = 25; y = x + 1",    # not a linear system
    "2 + 3 * 4",                    # a calculation
    "x = 1 = 2",                    # an error
])
def test_no_topic(equation: str) -> None:
    solver = Solve(equation, None)
    _, outputs, _ = solver.solve_equation()
    has_error = any("error" in (line[0] if isinstance(line, tuple) else line).casefold() for line in outputs)
    assert topics.find_topic(solver, has_error) is None
