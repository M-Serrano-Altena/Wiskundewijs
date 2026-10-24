"""Vectors and matrices for the solver, built on sympy.vector and sympy matrices.

`vect(1, 2)` creates a CustomVector and `matrix([1, 2], [3, 4])` a CustomMatrix. Their operators
keep results unevaluated where possible, so the solver can show both the input and the result.
"""

# SymPy wraps its operator methods (__add__, __lt__, ...) in decorators, so pyright sees them as
# variables and can't compare the overrides below with them.
# pyright: reportIncompatibleMethodOverride=false, reportIncompatibleVariableOverride=false

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import sympy as sp
import sympy.vector as sp_vector

# The coordinate system for all vectors. Its basis vectors (r.i, r.j, r.k) and coordinates
# (r.x, r.y, r.z) are created dynamically, so pyright can't know them.
r: Any = sp_vector.CoordSys3D("r")

# Dimension of the most recently created vector, used to print vectors with the right
# number of components. Every solve runs in a fresh process, so this doesn't leak between users.
vect_dim: int | None = None

DifferentialOperators = (sp_vector.Gradient, sp_vector.Divergence, sp_vector.Curl, sp_vector.Laplacian)

_MATRIX_TYPES = (sp.MatrixBase, sp.MatrixExpr)


def _is_number(value: object) -> bool:
    return bool(sp.sympify(value).is_number)


def _contains_only_numbers(value: Any) -> bool:
    return value.contains_only_numbers()


def convert_symbols_for_vector(args: Any) -> Any:
    """Replace the symbols x, y and z by the coordinates r.x, r.y and r.z of the vector space.

    args is either a single expression or the components of a vector.
    """
    global vect_dim
    if not isinstance(args, Iterable):
        expr = args
        vect_symbols_map = {"x": r.x, "y": r.y, "z": r.z}
        for symbol in expr.free_symbols:
            if symbol.name in vect_symbols_map:
                expr = expr.subs(symbol, vect_symbols_map[symbol.name])
        return expr

    components = [sp.sympify(arg) for arg in args]
    free_symbols = [symbol for component in components for symbol in component.free_symbols]

    if vect_dim is None:
        vect_dim = len(components)

    if not free_symbols:
        return components

    symbols: list[Any] = []
    vect_symbols: list[Any] = []
    for name, vect_symbol in (("x", r.x), ("y", r.y), ("z", r.z)):
        matching = list({symbol for symbol in free_symbols if symbol.name == name})
        symbols.extend(matching)
        if matching:
            vect_symbols.append(vect_symbol)

    symbols_map = dict(zip(symbols, vect_symbols))
    return [component.subs(symbols_map) for component in components]


class CustomVector(sp_vector.Vector):
    """A vector that remembers its components, so it can be printed and computed with directly."""

    # Not called _components: sympy's Vector uses that name for its own dict of components
    # ({r.i: 1, r.j: 2}), which sympy needs when vectors are added.
    _vector_components: tuple[Any, ...]
    _components: Any

    def __new__(cls, *args: Any) -> CustomVector:
        if len(args) == 2:
            vector = args[0] * r.i + args[1] * r.j
        elif len(args) == 3:
            vector = args[0] * r.i + args[1] * r.j + args[2] * r.k
        elif len(args) == 1:
            vector = sp.simplify(args[0])
        else:
            raise ValueError("Only 2D and 3D vectors are supported for the CustomVector class")

        obj = super().__new__(cls, vector)
        obj._vector_components = args
        obj._components = getattr(vector, "components", {})
        return obj

    def __add__(self, other: Any) -> Any:
        if _is_number(other):
            return CustomVector(*(comp + other for comp in self._vector_components))
        if isinstance(other, CustomVector):
            return CustomVector(*(a + b for a, b in zip(self._vector_components, other._vector_components)))
        if isinstance(other, _MATRIX_TYPES):
            return self.to_custom_matrix() + other
        if isinstance(other, (*DifferentialOperators, sp.Expr)):
            return CustomVectorAdd(self, other)
        raise NotImplementedError()

    def __sub__(self, other: Any) -> Any:
        if _is_number(other):
            return CustomVector(*(comp - other for comp in self._vector_components))
        if isinstance(other, CustomVector):
            return CustomVector(*(a - b for a, b in zip(self._vector_components, other._vector_components)))
        if isinstance(other, _MATRIX_TYPES):
            return self.to_custom_matrix() - other
        if isinstance(other, (*DifferentialOperators, sp.Expr)):
            return CustomVectorAdd(self, -other)
        raise NotImplementedError()

    def __mul__(self, other: Any) -> Any:
        if _is_number(other):
            return CustomVector(*(comp * other for comp in self._vector_components))
        # multiplying two vectors gives the dot product
        if isinstance(other, sp_vector.Vector):
            return self.dot(other)
        if isinstance(other, _MATRIX_TYPES):
            return self.to_custom_matrix() * other
        if isinstance(other, (*DifferentialOperators, sp.Expr)):
            return CustomVectorMul(self, other)
        raise NotImplementedError()

    def __truediv__(self, other: Any) -> Any:
        if _is_number(other):
            return CustomVector(*(comp * 1 / other for comp in self._vector_components))
        raise NotImplementedError()

    def __xor__(self, other: Any) -> Any:
        # vect(...) ^ vect(...) is the cross product
        if not isinstance(other, CustomVector):
            raise NotImplementedError()
        if len(self._vector_components) != 3 or len(other._vector_components) != 3:
            raise ValueError("Cross product requires 3-dimensional vectors.")

        cross_prod = sp_vector.cross(self.to_sympy_vector(), other.to_sympy_vector())
        return CustomVector(cross_prod.dot(r.i), cross_prod.dot(r.j), cross_prod.dot(r.k))

    def __pow__(self, other: Any) -> Any:
        if _is_number(other):
            return CustomVector(*(comp**other for comp in self._vector_components))
        # a vector to the power of a vector is seen as the cross product
        if isinstance(other, CustomVector):
            return self.cross(other)
        raise NotImplementedError()

    def __neg__(self) -> Any:
        return CustomVectorMul(-1, self)

    def __radd__(self, other: Any) -> Any:
        return self.__add__(other)

    def __rmul__(self, other: Any) -> Any:
        if isinstance(other, _MATRIX_TYPES):
            return CustomMatMul(other, self.to_custom_matrix())
        return self.__mul__(other)

    def __rsub__(self, other: Any) -> Any:
        if _is_number(other):
            return CustomVector(*(other - comp for comp in self._vector_components))
        if isinstance(other, (*DifferentialOperators, sp.Expr)):
            return CustomVectorAdd(other, -self)
        raise NotImplementedError("Right-side subtraction only supports scalar types.")

    # vectors are compared by their length
    def _compare_magnitude(self, other: Any) -> tuple[Any, Any]:
        if isinstance(other, sp_vector.Vector):
            return self.magnitude(), other.magnitude()
        if _is_number(other):
            return self.magnitude(), other
        raise NotImplementedError()

    def __lt__(self, other: Any) -> Any:
        own, others = self._compare_magnitude(other)
        return own < others

    def __le__(self, other: Any) -> Any:
        own, others = self._compare_magnitude(other)
        return own <= others

    def __gt__(self, other: Any) -> Any:
        own, others = self._compare_magnitude(other)
        return own > others

    def __ge__(self, other: Any) -> Any:
        own, others = self._compare_magnitude(other)
        return own >= others

    def __repr__(self) -> str:
        return f"CustomVector({', '.join(map(str, self._vector_components))})"

    def __str__(self) -> str:
        return self.__repr__()

    def doit(self) -> CustomVector:
        return CustomVector(*(sp.simplify(comp).doit() for comp in self._vector_components))

    def to_sympy_vector(self) -> Any:
        vector = 0 * r.i
        for comp, basis in zip(self._vector_components, [r.i, r.j, r.k]):
            vector += comp * basis
        return vector

    def to_custom_matrix(self) -> CustomMatrix:
        return matrix([[comp] for comp in self._vector_components])

    def simplify(self) -> CustomVector:
        return self.doit()

    def contains_only_numbers(self) -> bool:
        return all(_is_number(comp) for comp in self._vector_components)

    def dot(self, other: Any) -> Any:
        if isinstance(other, CustomVector):
            return sum(a * b for a, b in zip(self._vector_components, other._vector_components))
        if isinstance(other, sp_vector.Vector):
            return dot(self.to_sympy_vector(), other)
        raise TypeError("Dot product requires a CustomVector or a standard SymPy Vector.")

    def cross(self, other: Any) -> CustomVector:
        if isinstance(other, CustomVector):
            a1, a2, a3 = self._vector_components
            b1, b2, b3 = other._vector_components
            return CustomVector(a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1)
        if isinstance(other, sp_vector.Vector):
            result_vector = sp_vector.cross(self.to_sympy_vector(), other)
            return CustomVector(*(result_vector.dot(basis) for basis in [r.i, r.j, r.k]))
        raise TypeError("Cross product requires a CustomVector or a standard SymPy Vector.")

    def normalize(self) -> CustomVector:
        magnitude = self.magnitude()
        return CustomVector(*(comp / magnitude for comp in self._vector_components))

    def unit(self) -> CustomVector:
        return self.normalize()

    @property
    def T(self) -> Any:
        return sp.Transpose(self.to_custom_matrix())

    def evalf(self) -> CustomVector:
        return CustomVector(*(sp.N(comp) for comp in self._vector_components))


class CustomVectorAdd(sp.Add):
    """An unevaluated sum of vectors (and differential operators like grad)."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if not kwargs.get("evaluate", False):
            return super().__new__(cls, *args, evaluate=False)
        return super().__new__(cls, *args, evaluate=False).doit()

    def __add__(self, other: Any) -> Any:
        return CustomVectorAdd(self, other)

    def __radd__(self, other: Any) -> Any:
        return CustomVectorAdd(other, self)

    def __sub__(self, other: Any) -> Any:
        return CustomVectorAdd(self, -other)

    def __rsub__(self, other: Any) -> Any:
        return CustomVectorAdd(other, -self)

    def doit(self, **hints: Any) -> Any:
        evaluated_terms: list[Any] = [arg.doit(**hints) for arg in self.args]
        return sum(evaluated_terms)


class CustomVectorMul(sp.Mul):
    """An unevaluated product involving vectors."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        return super().__new__(cls, *args, **kwargs)

    def __mul__(self, other: Any) -> Any:
        return CustomVectorMul(self, other)

    def __rmul__(self, other: Any) -> Any:
        return CustomVectorMul(other, self)

    def __truediv__(self, other: Any) -> Any:
        return CustomVectorMul(self, sp.Pow(other, -1))

    def __rtruediv__(self, other: Any) -> Any:
        return CustomVectorMul(other, sp.Pow(self, -1))

    def doit(self, **hints: Any) -> Any:
        result: Any = sp.S.One
        for arg in self.args:
            result *= arg.doit(**hints)
        return result


class VectorShapeError(sp.ShapeError):
    """Raised when a matrix can't be turned into a vector."""

    def __init__(self, message: str = "Vector components must match the specified dimension") -> None:
        super().__init__(message)


def vect(*args: Any, dim: int | None = None) -> CustomVector:
    """Create a vector from its components, a column matrix or a list of components."""
    global vect_dim
    components: Any = args
    if len(args) == 1 and isinstance(args[0], _MATRIX_TYPES):
        column: Any = args[0]
        if column.cols != 1 or column.rows not in [1, 2, 3]:
            raise sp.ShapeError("Matrix must be a column matrix with 1, 2, or 3 rows.")
        rows = column.doit().tolist()
        components = [row[0] for row in rows]

    if isinstance(components[0], Iterable):
        components = components[0]
    elif dim is not None:
        vect_dim = dim
        components = tuple(components[:dim]) + (0,) * max(0, dim - len(components))
    else:
        vect_dim = len(components)

    return CustomVector(*convert_symbols_for_vector(components))


def to_custom_vector(sympy_vector: Any) -> CustomVector:
    return CustomVector(*(sympy_vector.dot(basis) for basis in [r.i, r.j, r.k]))


class Magnitude(sp.Function):
    """The length of a vector, kept unevaluated until doit()."""

    def __new__(cls, vector: Any) -> Any:
        if not isinstance(vector, sp_vector.Vector):
            raise TypeError("Magnitude can only be applied to vector objects.")
        return super().__new__(cls, vector)

    def doit(self, **hints: Any) -> Any:
        vector: Any = self.args[0]
        return sp.sqrt(vector.dot(vector))


def Abs(expr: Any) -> Any:
    """|x|: the length for vectors, the absolute value for everything else."""
    if isinstance(expr, sp_vector.Vector):
        return Magnitude(expr)
    return sp.Abs(expr)


def unit(vector: Any) -> Any:
    return vector.normalize()


def grad(expr: Any) -> CustomVector:
    return to_custom_vector(sp_vector.gradient(convert_symbols_for_vector(expr)))


def laplacian(expr: Any) -> Any:
    return sp_vector.laplacian(convert_symbols_for_vector(expr))


def angle(v1: Any, v2: Any) -> Any:
    """The angle between two vectors, in radians."""
    return sp.acos(v1.dot(v2) / (v1.magnitude() * v2.magnitude()))


class Angle(sp.Function):
    """The angle between two vectors, kept unevaluated until doit()."""

    def __new__(cls, v1: Any, v2: Any) -> Any:
        if not isinstance(v1, sp_vector.Vector) or not isinstance(v2, sp_vector.Vector):
            raise TypeError("Angle can only be applied to vector objects.")
        return super().__new__(cls, v1, v2)

    def doit(self, **hints: Any) -> Any:
        return angle(self.args[0], self.args[1])


def _to_sympy_vector(vector: Any) -> Any:
    return vector.to_sympy_vector() if isinstance(vector, CustomVector) else vector


def dot(v1: Any, v2: Any) -> Any:
    return sp_vector.dot(_to_sympy_vector(v1), _to_sympy_vector(v2))


def Dot(v1: Any, v2: Any) -> Any:
    return sp_vector.Dot(_to_sympy_vector(v1), _to_sympy_vector(v2))


def cross(v1: Any, v2: Any) -> CustomVector:
    return to_custom_vector(sp_vector.cross(_to_sympy_vector(v1), _to_sympy_vector(v2)))


def Cross(v1: Any, v2: Any) -> Any:
    return sp_vector.Cross(_to_sympy_vector(v1), _to_sympy_vector(v2))


def curl(v1: Any) -> CustomVector:
    return to_custom_vector(sp_vector.curl(_to_sympy_vector(v1)))


def Curl(v1: Any) -> Any:
    return sp_vector.Curl(_to_sympy_vector(v1))


class CustomMatrix(sp.Matrix):
    """A matrix whose operators give unevaluated results (CustomMatAdd, CustomMatMul)."""

    _matrix_data: list[list[Any]]

    def __new__(cls, *args: Any) -> Any:
        obj: Any
        if len(args) == 1 and isinstance(args[0], list):
            obj = super().__new__(cls, args[0])
        elif len(args) == 2 and all(isinstance(arg, int) for arg in args):
            obj = super().__new__(cls, args[0], args[1], lambda i, j: 0)
        else:
            raise ValueError("CustomMatrix requires either a list of lists or two integers for dimensions")

        obj._matrix_data = obj.tolist()
        return obj

    def __init__(self, *args: Any) -> None:
        self._matrix_data = self.tolist()

    def __add__(self, other: Any) -> Any:
        if _is_number(other):
            return self.applyfunc(lambda x: x + other)
        if isinstance(other, CustomMatrix):
            return CustomMatAdd(self.to_sympy_matrix(), other.to_sympy_matrix())
        if isinstance(other, _MATRIX_TYPES):
            return CustomMatAdd(self.to_sympy_matrix(), other)
        raise NotImplementedError("Only scalar or Matrix addition is supported.")

    def __sub__(self, other: Any) -> Any:
        if _is_number(other):
            return self.applyfunc(lambda x: x - other)
        if isinstance(other, CustomMatrix):
            return CustomMatAdd(self.to_sympy_matrix(), CustomMatMul(-1, other.to_sympy_matrix()))
        if isinstance(other, _MATRIX_TYPES):
            return CustomMatAdd(self.to_sympy_matrix(), CustomMatMul(-1, other))
        raise NotImplementedError("Only scalar or Matrix subtraction is supported.")

    def __mul__(self, other: Any) -> Any:
        if _is_number(other):
            return CustomMatMul(other, self.to_sympy_matrix())
        if isinstance(other, CustomMatrix):
            return CustomMatMul(self.to_sympy_matrix(), other.to_sympy_matrix())
        if isinstance(other, _MATRIX_TYPES):
            return CustomMatMul(self.to_sympy_matrix(), other)
        if isinstance(other, CustomVector):
            return self * other.to_custom_matrix()
        raise NotImplementedError("Only scalar or Matrix multiplication is supported.")

    def __truediv__(self, other: Any) -> Any:
        if _is_number(other):
            # dividing the plain sympy matrix, since self / other would call this method again
            return CustomMatrix((sp.Matrix(self.tolist()) / other).tolist())
        raise NotImplementedError("Division only supports scalar types.")

    def __matmul__(self, other: Any) -> Any:
        return self.__mul__(other)

    def __radd__(self, other: Any) -> Any:
        return self.__add__(other)

    def __rmul__(self, other: Any) -> Any:
        return self.__mul__(other)

    def __rsub__(self, other: Any) -> Any:
        if _is_number(other):
            return self.applyfunc(lambda x: other - x)
        return self.__sub__(other)

    def __neg__(self) -> Any:
        return CustomMatMul(-1, self.to_sympy_matrix())

    def __repr__(self) -> str:
        return f"CustomMatrix({self.tolist()})"

    def __str__(self) -> str:
        return f"CustomMatrix({self.tolist()})"

    def transpose(self) -> Any:
        return sp.Transpose(self.to_sympy_matrix())

    def det(self) -> Any:
        if self.rows == self.cols:
            return sp.Determinant(self.to_sympy_matrix())
        raise ValueError("Determinant is defined only for square matrices.")

    def inverse(self) -> CustomMatrix:
        if self.rows == self.cols:
            return to_custom_matrix(self.to_sympy_matrix().inv())
        raise ValueError("Inverse is defined only for square matrices.")

    def is_symmetric(self) -> bool:
        return bool(self == self.T)

    def simplify(self) -> Any:
        return self.applyfunc(sp.simplify)

    def to_sympy_matrix(self) -> Any:
        self._matrix_data = self.tolist()
        return sp.Matrix(self._matrix_data)

    def contains_only_numbers(self) -> bool:
        self._matrix_data = self.tolist()
        return all(_is_number(elem) for row in self._matrix_data for elem in row)


def max_depth(value: Any) -> int:
    """How deeply lists are nested: 0 for a non-list, 1 for [1, 2], 2 for [[1], [2]]."""
    if isinstance(value, list):
        return 1 + max((max_depth(item) for item in value), default=0)
    return 0


def matrix(*args: Any) -> CustomMatrix:
    """matrix([1, 2], [3, 4]) or matrix([[1, 2], [3, 4]]) or matrix(vect(1, 2))."""
    rows: Any = list(args)
    if len(rows) == 1:
        if isinstance(rows[0], CustomVector):
            rows = list(rows[0]._vector_components)
        elif isinstance(rows[0], Iterable) and len(rows[0]) == 1:
            rows = list(rows[0])

    while max_depth(rows) > 2 and len(rows) == 1:
        rows = rows[0]

    return CustomMatrix(rows)


def to_custom_matrix(sympy_matrix: Any) -> CustomMatrix:
    return CustomMatrix(sympy_matrix.tolist())


class CustomMatAdd(sp.MatAdd):
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        return super().__new__(cls, *args, **kwargs)

    def __add__(self, other: Any) -> Any:
        return CustomMatAdd(self, other)

    def __radd__(self, other: Any) -> Any:
        return CustomMatAdd(other, self)

    def __sub__(self, other: Any) -> Any:
        return CustomMatAdd(self, -other)

    def __rsub__(self, other: Any) -> Any:
        return CustomMatAdd(other, -self)

    def contains_only_numbers(self) -> bool:
        return all(_contains_only_numbers(arg) for arg in self.args)


class CustomMatMul(sp.MatMul):
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        return super().__new__(cls, *args, **kwargs)

    def __mul__(self, other: Any) -> Any:
        return CustomMatMul(self, other)

    def __rmul__(self, other: Any) -> Any:
        return CustomMatMul(other, self)

    def __add__(self, other: Any) -> Any:
        return CustomMatAdd(self, other)

    def __radd__(self, other: Any) -> Any:
        return CustomMatAdd(other, self)

    def contains_only_numbers(self) -> bool:
        return all(_contains_only_numbers(arg) for arg in self.args)


def inverse_expr(expr: Any) -> Any:
    """The inverse function of an expression in one variable."""
    symbol = expr.free_symbols.pop()
    placeholder_symbol = sp.Symbol("PLACEHOLDER_SYMBOL")
    solutions = [sol for sol in sp.solve(expr.subs(symbol, placeholder_symbol) - symbol, placeholder_symbol) if "I" not in str(sol)]

    abs_solutions: list[Any] = []
    new_solutions: list[Any] = []
    for sol in reversed(solutions):
        if sp.Abs(sol) not in abs_solutions:
            new_solutions.append(sol)
            abs_solutions.append(sp.Abs(sol))

    return new_solutions[0]


def inverse(expr: Any) -> Any:
    if isinstance(expr, _MATRIX_TYPES):
        return expr.inv()
    if sp.sympify(expr).has(sp.Symbol):
        return inverse_expr(expr)
    return sp.nsimplify(1 / expr)


def det(matrix: Any) -> Any:
    if isinstance(matrix, _MATRIX_TYPES):
        return sp.Determinant(matrix)
    return matrix
