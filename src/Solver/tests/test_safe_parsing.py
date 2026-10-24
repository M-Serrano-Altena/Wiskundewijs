from typing import Any

import pytest
import sympy as sp

from src.Solver.src.solver.safe_parsing import UnsafeInputError, safe_sympify, validate_user_input


@pytest.mark.parametrize("text", [
    "__import__('os').system('echo hi')",
    "x.__class__",
    "getattr(x, 'y')",
    "open('file.txt')",
    'limit(1/x, 0, "+") + "abc"',
    "x" * 256,
])
def test_validate_rejects_code(text: str) -> None:
    with pytest.raises(UnsafeInputError):
        validate_user_input(text)


@pytest.mark.parametrize("text", [
    "2x^2 + 1 = 9",
    "limit(1/x, 0, '+')",
    'limit(1/x, 0, "-")',
    r"\frac{1}{2}x = 3",
    "4x - 2y = 6; x - y = 1",
    "sin(30°)",
])
def test_validate_accepts_maths(text: str) -> None:
    validate_user_input(text)


@pytest.mark.parametrize("text", [
    "x**2 + 3*x + 1",
    "sin(x)/cos(x)",
    "Abs(x - 2)",
    "Integral(x**2, (x, 0, 1))",
    "Limit(1/x, x, 0, dir='+')",
    "x^2",
    "Matrix([[1, 2], [3, 4]])",
    "max(x, 2) + min(x, 3)",
])
def test_safe_sympify_matches_sympify(text: str) -> None:
    assert safe_sympify(text) == sp.sympify(text)


def test_safe_sympify_uses_local_dict() -> None:
    t = sp.Symbol("t")
    double = sp.Lambda(t, sp.Mul(2, t))
    assert safe_sympify("double(3)", local_dict={"double": double}) == 6


def test_builtins_are_unavailable() -> None:
    # Python builtins become plain symbols instead of being called.
    assert safe_sympify("open") == sp.Symbol("open")
    with pytest.raises(Exception):
        safe_sympify("getattr(x, dir(x)[0])")
    # an unknown name followed by brackets becomes an undefined maths function
    undefined_function: Any = sp.Function("eval")
    assert safe_sympify("eval(x)") == undefined_function(sp.Symbol("x"))


def test_string_evaluating_sympy_functions_are_unavailable() -> None:
    assert safe_sympify("sympify") == sp.Symbol("sympify")
    assert safe_sympify("lambdify") == sp.Symbol("lambdify")


def test_safe_sympify_rejects_strings_and_dunders() -> None:
    with pytest.raises(UnsafeInputError):
        safe_sympify("x.__class__")
    with pytest.raises(UnsafeInputError):
        safe_sympify("Symbol('a')")


def test_unparsable_text_raises_sympify_error() -> None:
    with pytest.raises(sp.SympifyError):
        safe_sympify("x +")
