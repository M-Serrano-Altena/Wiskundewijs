"""Turning user text into SymPy objects without letting it run Python code.

`sympy.sympify` evaluates strings with Python's `eval`, with all builtins available, so text
like `getattr(...)` or `__import__('os')` runs as code. Everything the solver parses goes
through `safe_sympify` instead, which adds two layers of protection:

1. `check_safe_text` rejects text containing `__` (the way into Python internals) and any
   string literal other than `'+'` and `'-'` (used by `limit(f(x), a, '+')`). Without
   strings, text can't be handed to anything that evaluates it again.
2. The text is evaluated in a namespace with SymPy's math functions but without Python's
   builtins (`open`, `getattr`, `eval`, ...) or the SymPy functions that evaluate, print or
   plot. Unknown names, like `open`, simply become symbols.
"""

from __future__ import annotations

from typing import Any, Mapping

import regex as re
import sympy as sp
from sympy.parsing.sympy_parser import (
    TokenError,
    convert_xor,
    parse_expr,
    standard_transformations,
)

MAX_INPUT_LENGTH = 255

_ALLOWED_STRING_LITERAL = re.compile(r"""(['"])[+-]\1""")

# SymPy functions that evaluate strings, run external programs, print or plot.
_BLOCKED_SYMPY_NAMES = frozenset({
    "sympify", "lambdify", "preview", "var", "init_session", "init_printing",
    "interactive_traversal", "test", "doctest", "plot", "plot_implicit", "plot_parametric",
    "plot3d", "plot3d_parametric_line", "plot3d_parametric_surface", "plot_backends", "textplot",
    "pprint", "pretty_print", "pprint_use_unicode", "pprint_try_use_unicode", "print_tree",
    "print_gtk", "print_latex", "print_mathml", "print_python", "print_rcode", "print_ccode",
    "print_fcode", "print_jscode", "print_glsl", "python", "sstr", "sstrrepr", "srepr", "latex",
    "multiline_latex", "mathml", "pretty", "upretty", "dotprint", "ccode", "fcode", "jscode",
    "julia_code", "octave_code", "rust_code", "maple_code", "mathematica_code", "rcode",
    "cxxcode", "glsl_code", "pycode", "smtlib_code",
})

# Python builtins that sympify normally makes available and that maths input can use.
_SAFE_BUILTINS: dict[str, Any] = {"abs": abs, "round": round, "pow": pow, "divmod": divmod, "max": sp.Max, "min": sp.Min}


def _build_namespace() -> dict[str, Any]:
    namespace: dict[str, Any] = {
        name: getattr(sp, name) for name in sp.__all__ if name not in _BLOCKED_SYMPY_NAMES
    }
    namespace.update(_SAFE_BUILTINS)
    # Without this key, eval() would add the full builtins module itself.
    namespace["__builtins__"] = {}
    return namespace


_NAMESPACE = _build_namespace()

# The type hints of sympy.sympify (since sympy 1.14) leave out its `evaluate` argument.
_sympify: Any = sp.sympify
_TRANSFORMATIONS = standard_transformations + (convert_xor,)


class UnsafeInputError(ValueError):
    """Raised for input that looks like Python code instead of maths."""


def check_safe_text(text: str) -> None:
    """Raise UnsafeInputError if text could reach Python internals or contains strings."""
    if "__" in text:
        raise UnsafeInputError("Input may not contain '__'")

    without_allowed_strings = _ALLOWED_STRING_LITERAL.sub("", text)
    if "'" in without_allowed_strings or '"' in without_allowed_strings:
        raise UnsafeInputError("Input may only contain the strings '+' and '-'")


def validate_user_input(text: str) -> None:
    """Check text typed by a user before it's given to the solver."""
    if len(text) > MAX_INPUT_LENGTH:
        raise UnsafeInputError(f"Input may be at most {MAX_INPUT_LENGTH} characters long")
    check_safe_text(text)


def safe_sympify(expr: Any, local_dict: Mapping[str, Any] | None = None, evaluate: bool = True) -> Any:
    """Drop-in replacement for `sympy.sympify(expr, locals=local_dict, evaluate=evaluate)`.

    Returns Any rather than sp.Basic because, like sympify, the custom functions in
    local_dict can produce non-Basic objects (sympy vectors, Python numbers).
    """
    if not isinstance(expr, str):
        return _sympify(expr, evaluate=evaluate)

    check_safe_text(expr)
    try:
        return parse_expr(
            expr.replace("\n", ""),
            local_dict=dict(local_dict) if local_dict is not None else {},
            global_dict=_NAMESPACE.copy(),
            transformations=_TRANSFORMATIONS,
            evaluate=evaluate,
        )
    except (TokenError, SyntaxError) as error:
        raise sp.SympifyError(f"could not parse {expr!r}", error) from error
