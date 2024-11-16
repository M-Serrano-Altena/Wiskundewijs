"""
sympy_custom_funcs.py
----------------------

This module extends general SymPy and SymPy's vector capabilities with customized functions, symbolic operations, 
and specialized LaTeX printing. It introduces new operations for vector handling, customized inequality 
printing, rational number formatting, and symbolic function handling to enhance symbolic math representation 
and formatting, particularly for educational and presentation purposes.

Classes:
    Dot: A symbolic class for representing the dot product symbolically with evaluation deferred until necessary.
    CustomLatexPrinter: Extends SymPy's LatexPrinter with custom methods for printing relations, vectors, 
                        logarithms, limits, and more in LaTeX format. Also formats rational numbers in mixed 
                        fractional form, making expressions more accessible for students and presentations.

Functions:
    convert_symbols_for_vector(args): 
        Replaces symbols 'x', 'y', and 'z' in expressions with vector symbols from a CoordSys3D object, 
        based on vector dimension. Supports expressions in 1D, 2D, and 3D.
    
    vect(*args, dim=None): 
        Constructs a vector based on input components or dimension, utilizing `convert_symbols_for_vector` 
        for symbol substitution. Supports 1D to 3D vectors.
    
    Abs(expr): 
        Returns the magnitude (Euclidean norm) of a vector or the absolute value of a scalar expression.
    
    grad(expr): 
        Computes the gradient of a scalar field using vector symbols, calling `convert_symbols_for_vector` 
        to replace standard symbols with vector counterparts.
    
    equation_type_to_latex(equation_symbol): 
        Maps common relational symbols to their LaTeX equivalents for improved readability in inequalities.
    
    flip_inequality_sign(inequality_sign): 
        Returns the opposite inequality symbol, useful for managing inequalities in custom expressions.
    
    dot(vec1, vec2): 
        Computes the dot product of two vectors, returning a scalar result. Supports symbolic input.
    
    LOCALS: 
        Dictionary of functions and variables to be used with SymPy's `sympify` for dynamic evaluations.

Module Enhancements:
    - Extends SymPy's printing functionality to handle custom cases for vectors, inequalities, and 
      trigonometric solutions.
    - Provides symbolic and numerical vector operations for general 3D coordinate systems.
"""

import sympy as sp
import sympy.vector as sp_vector
from collections.abc import Iterable
import regex as re
from sympy.printing.latex import LatexPrinter
from sympy.physics.units import degree
import typing
from numbers import Number
from src.Solver.src.solver.helper import *


r = sp_vector.CoordSys3D('r')
vect_dim = None

SYMPY_BOOLEANS = (sp.logic.boolalg.BooleanTrue, sp.logic.boolalg.BooleanFalse)

def convert_symbols_for_vector(args):
    """
    Converts standard symbols ('x', 'y', 'z') in an expression or list of expressions to corresponding
    vector symbols (e.g., CoordSys3D basis symbols `r.x`, `r.y`, `r.z`) based on the current vector dimension.
    
    Parameters:
        args (Iterable or Expr): A single expression or list of expressions containing symbols 
                                 to be converted to vector symbols.
    
    Returns:
        Expr or List[Expr]: The modified expression(s) with vector symbols in place of standard symbols.
    
    Notes:
        The global variable `vect_dim` is used to infer the dimension if not specified, allowing for
        support of up to 3D vector representation.
    """
    global vect_dim
    if isinstance(args, Iterable):
        args = [sp.sympify(arg) for arg in args]
        free_symbols = []
        for arg in args:
            free_symbols.extend(arg.free_symbols)

        if vect_dim is None:
            vect_dim = len(args)

        if not free_symbols:
            return args
    
        x = list({symbol for symbol in free_symbols if symbol.name == "x"})
        y = list({symbol for symbol in free_symbols if symbol.name == "y"})
        z = list({symbol for symbol in free_symbols if symbol.name == "z"})

        symbols = x + y + z
        vect_symbols = []

        if x:
            vect_symbols.append(r.x)
        if y:
            vect_symbols.append(r.y)
        if z:
            vect_symbols.append(r.z)

        symbols_map = dict(zip(symbols, vect_symbols))

        args = [arg.subs(symbols_map) for arg in args]
        return args
    
    expr = args # args is then an expresion
    vect_symbols_map = {"x": r.x, "y": r.y, "z": r.z}
    symbols = expr.free_symbols
    for symbol in symbols:
        if symbol.name in vect_symbols_map:
            expr = expr.subs(symbol, vect_symbols_map[symbol.name])

    return expr

DifferentialOperators = (
    sp_vector.Gradient,
    sp_vector.Divergence,
    sp_vector.Curl,
    sp_vector.Laplacian
)

class CustomVector(sp_vector.Vector):
    def __new__(cls, *args):
        # Create the vector components in the CoordSys3D basis
        if len(args) == 2:
            vector = args[0] * r.i + args[1] * r.j
        elif len(args) == 3:
            vector = args[0] * r.i + args[1] * r.j + args[2] * r.k
        elif len(args) == 1:
            vector = sp.simplify(args[0])
        else:
            raise ValueError("Only 2D and 3D vectors are supported for the CustomVector class")
        
        # Return the new object as a Vector instance
        obj = super(CustomVector, cls).__new__(cls, vector)
        obj._components = args  # Store components for further use if needed
        return obj
    

    def __add__(self, other):
        # Handle scalar addition by adding the scalar to each component
        if sp.sympify(other).is_number:
            new_components = tuple(comp + other for comp in self._components)
            return CustomVector(*new_components)
        
        # Handle vector addition
        elif isinstance(other, CustomVector):
            new_components = tuple(a + b for a, b in zip(self._components, other._components))
            return CustomVector(*new_components)
        
        elif isinstance(other, (sp.MatrixBase, sp.MatrixExpr)):
            return self.to_custom_matrix() + other
        
        elif isinstance(other, DifferentialOperators):
            return CustomVectorAdd(self, other)
        
        elif isinstance(other, sp.Expr):
            return CustomVectorAdd(self, other)

        raise NotImplementedError()
    
    def __sub__(self, other):
        # Handle scalar subtraction by subtracting the scalar to each component
        if sp.sympify(other).is_number:
            new_components = tuple(comp - other for comp in self._components)
            return CustomVector(*new_components)
        
        # Handle vector subtraction
        elif isinstance(other, CustomVector):
            new_components = tuple(a - b for a, b in zip(self._components, other._components))
            return CustomVector(*new_components)
        
        elif isinstance(other, (sp.MatrixBase, sp.MatrixExpr)):
            return self.to_custom_matrix() - other
        
        elif isinstance(other, DifferentialOperators):
            return CustomVectorAdd(self, -other)
        
        elif isinstance(other, sp.Expr):
            return CustomVectorAdd(self, -other)

        raise NotImplementedError()
        
    def __mul__(self, other):
        # Handle scalar multiplication
        if sp.sympify(other).is_number:
            new_components = tuple(comp * other for comp in self._components)
            return CustomVector(*new_components)
        
        # Handle vector multiplication as dot product
        elif isinstance(other, (sp_vector.Vector)):
            return self.dot(other)
        
        elif isinstance(other, (sp.MatrixBase, sp.MatrixExpr)):
            return self.to_custom_matrix() * other
        
        elif isinstance(other, DifferentialOperators):
            return CustomVectorMul(self, other)
        
        elif isinstance(other, sp.Expr):
            return CustomVectorMul(self, other)
        
        raise NotImplementedError()
    
    def __truediv__(self, other):
        # Handle scalar division
        if sp.sympify(other).is_number:
            new_components = tuple(comp * 1/other for comp in self._components)
            return CustomVector(*new_components)
        
        raise NotImplementedError()
    
    def __xor__(self, other):
        # Handle cross product if other is a CustomVector
        if isinstance(other, CustomVector):
            if len(self._components) == 3 and len(other._components) == 3:
                # Convert components to SymPy vector form
                self_vector = self._components[0] * r.i + self._components[1] * r.j + self._components[2] * r.k
                other_vector = other._components[0] * r.i + other._components[1] * r.j + other._components[2] * r.k
                # Calculate cross product
                cross_prod = sp_vector.cross(self_vector, other_vector)
                # Extract components for the result vector
                new_components = (cross_prod.dot(r.i), cross_prod.dot(r.j), cross_prod.dot(r.k))
                return CustomVector(*new_components)
            else:
                raise ValueError("Cross product requires 3-dimensional vectors.")

        raise NotImplementedError()
    
    def __pow__(self, other):
        if sp.sympify(other).is_number:
            new_components = tuple(comp ** other for comp in self._components)
            return CustomVector(*new_components)
        
        # two vectors to the power of eachother is just seen as curl
        elif isinstance(other, CustomVector):
            return self.cross(other)

        raise NotImplementedError()
    
    def __neg__(self):
        # Negate each component to return the negative of the vector
        return CustomVectorMul(-1, self)

    def __radd__(self, other):
        # Support scalar addition from the right side
        return self.__add__(other)
    
    def __rmul__(self, other):        
        if isinstance(other, (sp.MatrixBase, sp.MatrixExpr)):
            return CustomMatMul(other, self.to_custom_matrix())
        
        return self.__mul__(other)
    
    def __rsub__(self, other):
        # Handle scalar - vector by subtracting each component from the scalar
        if sp.sympify(other).is_number:
            new_components = tuple(other - comp for comp in self.components)
            return CustomVector(*new_components)
        
        elif isinstance(other, DifferentialOperators):
            return CustomVectorAdd(other, -self)
        
        elif isinstance(other, sp.Expr):
            return CustomVectorAdd(other, -self)
    
        raise NotImplementedError("Right-side subtraction only supports scalar types.")
    
    def __lt__(self, other):
        # Compare magnitudes of vectors
        if isinstance(other, (CustomVector, sp_vector.Vector)):
            return self.magnitude() < other.magnitude()
        elif sp.sympify(other).is_number:
            return self.magnitude() < other
        raise NotImplementedError()
    
    def __le__(self, other):
        # Compare magnitudes of vectors
        if isinstance(other, (CustomVector, sp_vector.Vector)):
            return self.magnitude() <= other.magnitude()
        elif sp.sympify(other).is_number:
            return self.magnitude() <= other
        raise NotImplementedError()
    
    def __gt__(self, other):
        # Compare magnitudes of vectors
        if isinstance(other, (CustomVector, sp_vector.Vector)):
            return self.magnitude() > other.magnitude()
        elif sp.sympify(other).is_number:
            return self.magnitude() > other
        raise NotImplementedError()
    
    def __ge__(self, other):
        # Compare magnitudes of vectors
        if isinstance(other, (CustomVector, sp_vector.Vector)):
            return self.magnitude() >= other.magnitude()
        elif sp.sympify(other).is_number:
            return self.magnitude() >= other
        raise NotImplementedError()
    
    def __repr__(self):
        # Format the representation without expanding into basis vectors
        return f"CustomVector({', '.join(map(str, self._components))})"

    def __str__(self):
        # Similar to __repr__, display the components directly in vector form
        return self.__repr__()

    def doit(self):
        # Simplify each component and create a new CustomVector with the simplified components
        simplified_components = tuple(sp.simplify(comp).doit() for comp in self._components)
        return CustomVector(*simplified_components)

    def to_sympy_vector(self):
        vector = 0*r.i
        for comp, basis in zip(self._components, [r.i, r.j, r.k]):
            vector += comp * basis

        return vector
    
    def to_custom_matrix(self):
        # Convert the vector to a matrix with the components as rows
        return matrix([[comp] for comp in self._components])
    
    def simplify(self):
        return self.doit()
    
    def contain_only_numbers(self):
        return all(sp.sympify(comp).is_number for comp in self._components)

    def dot(self, other):
        if isinstance(other, CustomVector):
            # Perform component-wise multiplication for dot product
            return sum(a * b for a, b in zip(self._components, other._components))
        
        elif isinstance(other, sp_vector.Vector):
            # Convert CustomVector to a standard Vector to use SymPy's built-in dot product
            self_vector = self.to_sympy_vector()
            return dot(self_vector, other)
        
        raise TypeError("Dot product requires a CustomVector or a standard SymPy Vector.")
    
    def cross(self, other):
        if isinstance(other, CustomVector):
            # Perform component-wise calculation for cross product by manually defining the cross product
            a1, a2, a3 = self._components
            b1, b2, b3 = other._components
            # Compute each component of the cross product
            c1 = a2 * b3 - a3 * b2
            c2 = a3 * b1 - a1 * b3
            c3 = a1 * b2 - a2 * b1
            return CustomVector(c1, c2, c3)
        
        elif isinstance(other, sp_vector.Vector):
            # Convert CustomVector to a standard Vector and perform cross product with SymPy's built-in function
            self_vector = self.to_sympy_vector()
            result_vector = sp_vector.cross(self_vector, other)
            # Extract components from result_vector to return as a CustomVector
            components = [result_vector.dot(basis) for basis in [r.i, r.j, r.k]]
            return CustomVector(*components)

        raise TypeError("Cross product requires a CustomVector or a standard SymPy Vector.")

    def normalize(self):
        # Calculate the magnitude of the vector
        magnitude = self.magnitude()
        # Normalize the vector by dividing each component by the magnitude
        new_components = tuple(comp / magnitude for comp in self._components)
        return CustomVector(*new_components)
    
    def unit(self):
        return self.normalize()
    
    @property
    def T(self):
        return sp.Transpose(self.to_custom_matrix())
    
    def evalf(self):
        return CustomVector(*[sp.N(comp) for comp in self._components])
    

class CustomVectorAdd(sp.Add):
    def __new__(cls, *args, **kwargs):
        # Check for 'evaluate' in kwargs, similar to how Add and Mul handle it
        evaluate = kwargs.get('evaluate', False)
        if not evaluate:
            # Return an unevaluated Mul object if evaluate=False
            return super().__new__(cls, *args, evaluate=False)
        else:
            # Use the parent class's __new__ method to handle simplification if evaluate=True
            return super(CustomVectorAdd, cls).__new__(cls, *args, evaluate=False).doit()
    
    def __add__(self, other):
        return CustomVectorAdd(self, other)
    
    def __radd__(self, other):
        return CustomVectorAdd(other, self)
    
    def __sub__(self, other):
        return CustomVectorAdd(self, -other)
    
    def __rsub__(self, other):
        return CustomVectorAdd(other, -self)
    
    def doit(self, **hints):
        return sum(arg.doit(**hints) for arg in self.args)
    
class CustomVectorMul(sp.Mul):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)
    
    def __mul__(self, other):
        # Support chaining multiplications with other VectorMul objects
        return CustomVectorMul(self, other)
    
    def __rmul__(self, other):
        return CustomVectorMul(other, self)
    
    def __truediv__(self, other):
        # Allows division to be represented as a reciprocal multiplication
        return CustomVectorMul(self, sp.Pow(other, -1))
    
    def __rtruediv__(self, other):
        # Reverse division for right-hand operations
        return CustomVectorMul(other, sp.Pow(self, -1))
    
    def doit(self, **hints):
        # Evaluate each argument in the multiplication
        result = sp.S.One
        for arg in self.args:
            result *= arg.doit(**hints)
        return result


class VectorShapeError(sp.ShapeError):
    """
    Exception raised when the number of components in a vector does not match the expected dimension.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Vector components must match the specified dimension"):
        super().__init__(message)


def vect(*args, dim=None):
    """
    Constructs a vector based on input components or specified dimension, with optional symbol 
    substitution using `convert_symbols_for_vector`.

    Parameters:
        args (tuple): Individual components for the vector in 1D, 2D, or 3D, or a single iterable of components.
        dim (int, optional): The dimension of the vector (1, 2, or 3). If not provided, the length of `args`
                             will be used to determine dimension.

    Returns:
        Vector: A vector in the specified dimension using CoordSys3D basis vectors.
    
    Notes:
        The function defaults to a 3D vector if no dimension is provided and the number of arguments is 3.
    """
    global vect_dim
    if len(args) == 1 and isinstance(args[0], (sp.MatrixBase, sp.MatrixExpr)):
        args = args[0]
        if args.cols != 1 or args.rows not in [1, 2, 3]:
            raise sp.ShapeError("Matrix must be a column matrix with 1, 2, or 3 rows.")
        args = args.doit().tolist()
        args = [args[i][0] for i in range(len(args))]

    if isinstance(args[0], Iterable):
        args = args[0]

    elif dim is not None:
        vect_dim = dim
        if len(args) > dim:
            args = args[:dim]
        if len(args) < dim:
            while len(args) < dim:
                args += (0,)
    else:
        vect_dim = len(args)
    
    args = convert_symbols_for_vector(args)

    return CustomVector(*args)


def to_custom_vector(sympy_vector: sp_vector.Vector) -> CustomVector:
    # Define the basis vectors in the coordinate system (assuming Cartesian coordinates with r.i, r.j, and r.k)
    basis_vectors = [r.i, r.j, r.k]

    # Extract each component by dotting with the basis vectors
    components = [sympy_vector.dot(basis) for basis in basis_vectors]
    
    # Create and return a CustomVector with the extracted components
    return CustomVector(*components)


class Magnitude(sp.Function):
    """
    Custom Magnitude function that symbolically represents the magnitude
    of a vector. The `doit()` method evaluates the Euclidean norm.
    """

    def __new__(cls, vector):
        if not isinstance(vector, sp_vector.Vector):
            raise TypeError("Magnitude can only be applied to vector objects.")
        return super(Magnitude, cls).__new__(cls, vector)

    def doit(self, **hints):
        """
        Evaluate the magnitude (Euclidean norm) of the vector.
        """
        vector = self.args[0]
        return sp.sqrt(vector.dot(vector))


def Abs(expr):
    """
    Computes the Euclidean norm (magnitude) of a vector or the absolute value of a scalar expression.

    Parameters:
        expr (Expr or Vector): The input expression or vector for which the magnitude or absolute value 
                               is calculated.
    
    Returns:
        Expr: The magnitude of the vector or absolute value of the scalar expression.
    """
    if isinstance(expr, sp_vector.Vector):
        return Magnitude(expr)
    
    return sp.Abs(expr)

def unit(vector):
    """
    Computes the unit vector of a given vector.

    Parameters:
        vector (Vector): The input vector for which the unit vector is calculated.
    
    Returns:
        Vector: The unit vector of the input vector.
    """
    return vector.normalize()

def grad(expr):
    """
    Computes the gradient of a scalar field, converting symbols in the expression to vector symbols
    where necessary.

    Parameters:
        expr (Expr): A scalar expression representing a field over which the gradient is calculated.
    
    Returns:
        Vector: The gradient vector of the input expression.
    """
    expr = convert_symbols_for_vector(expr)
    sympy_vector = sp_vector.gradient(expr)
    return to_custom_vector(sympy_vector)

def laplacian(expr):
    """
    Computes the Laplacian of a scalar field, converting symbols in the expression to vector symbols
    where necessary.

    Parameters:
        expr (Expr): A scalar expression representing a field over which the Laplacian is calculated.
    
    Returns:
        Expr: The Laplacian of the input expression.
    """
    expr = convert_symbols_for_vector(expr)
    return sp_vector.laplacian(expr)


def angle(v1, v2):
    """
    Compute the angle between two vectors.

    Args:
        v1 (Vector): The first vector.
        v2 (Vector): The second vector.

    Returns:
        Expr: The angle between the two vectors.
    """
    return sp.acos(v1.dot(v2) / (v1.magnitude() * v2.magnitude()))

def angle_deg(v1, v2):
    """
    Compute the angle in degrees between two vectors.

    Args:
        v1 (Vector): The first vector.
        v2 (Vector): The second vector.

    Returns:
        Expr: The angle in degrees between the two vectors.
    """
    return acos_deg(v1.dot(v2) / (v1.magnitude() * v2.magnitude()))

class Angle(sp.Function):
    """
    Custom Angle function that symbolically represents the angle between two vectors.
    """

    def __new__(cls, v1, v2):
        if not isinstance(v1, sp_vector.Vector) or not isinstance(v2, sp_vector.Vector):
            raise TypeError("Angle can only be applied to vector objects.")
        return super(Angle, cls).__new__(cls, v1, v2)

    def doit(self, **hints):
        """
        Evaluate the angle between two vectors.
        """
        v1 = self.args[0]
        v2 = self.args[1]
        return angle(v1, v2)


def dot(v1, v2):
    if isinstance(v1, CustomVector):
        v1 = v1.to_sympy_vector()

    if isinstance(v2, CustomVector):
        v2 = v2.to_sympy_vector()

    return sp_vector.dot(v1, v2)

def Dot(v1, v2):
    if isinstance(v1, CustomVector):
        v1 = v1.to_sympy_vector()

    if isinstance(v2, CustomVector):
        v2 = v2.to_sympy_vector()

    return sp_vector.Dot(v1, v2)

def cross(v1, v2):
    if isinstance(v1, CustomVector):
        v1 = v1.to_sympy_vector()

    if isinstance(v2, CustomVector):
        v2 = v2.to_sympy_vector()

    sympy_vector = sp_vector.cross(v1, v2)
    return to_custom_vector(sympy_vector)

def Cross(v1, v2):
    if isinstance(v1, CustomVector):
        v1 = v1.to_sympy_vector()

    if isinstance(v2, CustomVector):
        v2 = v2.to_sympy_vector()

    return sp_vector.Cross(v1, v2)

def curl(v1):
    if isinstance(v1, CustomVector):
        v1 = v1.to_sympy_vector()

    sympy_vector = sp_vector.curl(v1)
    return to_custom_vector(sympy_vector)

def Curl(v1):
    if isinstance(v1, CustomVector):
        v1 = v1.to_sympy_vector()

    return sp_vector.Curl(v1)


class CustomMatrix(sp.Matrix):
    def __new__(cls, *args):
        # Create a new CustomMatrix instance by calling the constructor of sp.Matrix
        if len(args) == 1 and isinstance(args[0], list):  # If input is a list of lists
            matrix_data = args[0]
            obj = super(CustomMatrix, cls).__new__(cls, matrix_data)
        elif len(args) == 2 and all(isinstance(arg, int) for arg in args):  # If given dimensions
            obj = super(CustomMatrix, cls).__new__(cls, args[0], args[1], lambda i, j: 0)
        else:
            raise ValueError("CustomMatrix requires either a list of lists or two integers for dimensions")
        
        obj._matrix_data = obj.tolist()  # Store components for further use if needed
        return obj

    def __add__(self, other):
        # Handle scalar addition by adding the scalar to each element
        if sp.sympify(other).is_number:
            return self.applyfunc(lambda x: x + other)
        
        # Handle matrix addition if other is CustomMatrix
        elif isinstance(other, CustomMatrix):
            return CustomMatAdd(self.to_sympy_matrix(), other.to_sympy_matrix())
        
        elif isinstance(other, (sp.MatrixBase, sp.MatrixExpr)):
            return CustomMatAdd(self.to_sympy_matrix(), other)

        raise NotImplementedError("Only scalar or Matrix addition is supported.")

    def __sub__(self, other):
        # Handle scalar subtraction
        if sp.sympify(other).is_number:
            return self.applyfunc(lambda x: x - other)
        
        # Handle matrix subtraction
        elif isinstance(other, CustomMatrix):
            return CustomMatAdd(self.to_sympy_matrix(), CustomMatMul(-1, other.to_sympy_matrix()))
        
        elif isinstance(other, (sp.MatrixBase, sp.MatrixExpr)):
            return CustomMatAdd(self.to_sympy_matrix(), CustomMatMul(-1, other))

        raise NotImplementedError("Only scalar or Matrix subtraction is supported.")
        
    def __mul__(self, other):
        # Handle scalar multiplication
        if sp.sympify(other).is_number:
            return CustomMatMul(other, self.to_sympy_matrix())
        
        # Handle CustomMatrix multiplication
        elif isinstance(other, CustomMatrix):
            return CustomMatMul(self.to_sympy_matrix(), other.to_sympy_matrix())
        
        # Handle regular matrix multiplication
        elif isinstance(other, (sp.MatrixBase, sp.MatrixExpr)):
            return CustomMatMul(self.to_sympy_matrix(), other)
        
        # Handle vector multiplication
        elif isinstance(other, CustomVector):
            return self * other.to_custom_matrix()
        
        raise NotImplementedError("Only scalar or Matrix multiplication is supported.")

    def __truediv__(self, other):
        # Handle scalar division
        if sp.sympify(other).is_number:
            return CustomMatrix((self / other).tolist())

        raise NotImplementedError("Division only supports scalar types.")
    
    def __matmul__(self, other):
        return self.__mul__(other)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __rsub__(self, other):
        # Handle scalar subtraction
        if sp.sympify(other).is_number:
            return self.applyfunc(lambda x: other - x)
        
        return self.__sub__(other)

    def __neg__(self):
        # Negate each component to return the negative of the matrix
        return CustomMatMul(-1, self.to_sympy_matrix())

    def __repr__(self):
        # Generate a string representation for debugging
        return f'CustomMatrix({self.tolist()})'
    
    def __str__(self):
        # Generate a pretty string representation for display
        return f'CustomMatrix({self.tolist()})'
    
    def transpose(self):
        # Transpose the matrix
        return sp.Transpose(self.to_sympy_matrix())
    
    def det(self):
        # Calculate and return the determinant of the matrix
        if self.rows == self.cols:
            return sp.Determinant(self.to_sympy_matrix())
        raise ValueError("Determinant is defined only for square matrices.")
    
    def inverse(self):
        # Calculate the inverse of the matrix
        if self.rows == self.cols:
            return to_custom_matrix(self.to_sympy_matrix().inv())
        raise ValueError("Inverse is defined only for square matrices.")
    
    def is_symmetric(self):
        # Check if the matrix is symmetric
        return self == self.T
    
    def simplify(self):
        # Simplify each component in the matrix
        return sp.simplify(self)
    
    def to_sympy_matrix(self):
        # Convert to a standard SymPy Matrix
        return sp.Matrix(self._matrix_data)


def max_depth(lst):
    if isinstance(lst, list):
        return 1 + max((max_depth(item) for item in lst), default=0)
    return 0


def matrix(*args):
    args = list(args)
    if len(args) == 1 and isinstance(args[0], Iterable) and len(args[0]) == 1:
        args = list(args[0])

    while max_depth(args) > 2 and len(args) == 1:
        args = args[0]

    return CustomMatrix(args)

def to_custom_matrix(sympy_matrix: sp.Matrix) -> CustomMatrix:
    # Extract each row of the matrix as a list and construct a 2D list
    matrix_data = sympy_matrix.tolist()
    
    # Create and return a CustomMatrix with the extracted matrix data
    return CustomMatrix(matrix_data)


class CustomMatAdd(sp.MatAdd):
    def __new__(cls, *args, **kwargs):
        # This ensures that all additions result in a CustomMatAdd instance
        return super(CustomMatAdd, cls).__new__(cls, *args, **kwargs)
    
    def __add__(self, other):
        return CustomMatAdd(self, other)
    
    def __radd__(self, other):
        return CustomMatAdd(other, self)

    def __sub__(self, other):
        # Subtraction is treated as adding the negative, resulting in a CustomMatAdd
        return CustomMatAdd(self, -other)
    
    def __rsub__(self, other):
        # Reverse subtraction also results in a CustomMatAdd
        return CustomMatAdd(other, -self)

class CustomMatMul(sp.MatMul):
    def __new__(cls, *args, **kwargs):
        # This ensures that all multiplications result in a CustomMatMul instance
        return super(CustomMatMul, cls).__new__(cls, *args, **kwargs)
    
    def __mul__(self, other):
        return CustomMatMul(self, other)
    
    def __rmul__(self, other):
        return CustomMatMul(other, self)

    def __add__(self, other):
        # Addition should result in a CustomMatAdd if it involves a multiplication
        return CustomMatAdd(self, other)
    
    def __radd__(self, other):
        return CustomMatAdd(other, self)


def inverse_expr(expr):
    symbol = expr.free_symbols.pop()
    placeholder_symbol = sp.symbols("PLACEHOLDER_SYMBOL")
    free_y_equation = reversed([sol for sol in sp.solve(expr.subs(symbol, placeholder_symbol) - symbol, placeholder_symbol) if "I" not in str(sol)])
    abs_solutions = []
    new_solutions = []
    for sol in free_y_equation:
        if sp.Abs(sol) not in abs_solutions:
            new_solutions.append(sol)
            abs_solutions.append(sp.Abs(sol))

    return new_solutions[0]

def inverse(expr):
    if isinstance(expr, (sp.MatrixBase, sp.MatrixExpr)):
        return expr.inv()
    
    elif sp.sympify(expr).has(sp.Symbol):
        inverse_expression = inverse_expr(expr)        
        return inverse_expression
    
    return sp.nsimplify(1 / expr)

def det(matrix):
    if isinstance(matrix, (sp.MatrixBase, sp.MatrixExpr)):
        return sp.Determinant(matrix)

    return matrix

LOCALS = {
    "vect": vect, 
    "Abs": Abs, 
    "r": r,
    "dot": dot,
    "Dot": Dot,
    "cross": cross,
    "Cross": Cross,
    "div": sp_vector.divergence, 
    "Divergence": sp_vector.Divergence,
    "curl": curl, 
    "Curl": Curl,
    "grad": grad, 
    "Gradient": sp_vector.Gradient,
    "laplacian": laplacian,
    "Laplacian": sp_vector.Laplacian,
    "magnitude": Abs,
    "Magnitude": Magnitude,
    "unit": unit,
    "norm": unit,
    "normalize": unit,
    "angle": angle,
    "Angle": Angle,
    "matrix": matrix,
    "inverse": inverse,
    "det": det,
}

class ArcGonioInvalidDomainError(ValueError):
    """
    Exception raised when an invalid input value is provided to an arc-goniometric function 
    (e.g., arcsin, arccos) that would result in a complex output.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Operation requires a valid input that yields a real result for arc-goniometric functions"):
        super().__init__(message)

class ArcReciprocalInvalidDomainError(ArcGonioInvalidDomainError):
    pass

def asin_deg(arg):
    arg = sp.sympify(arg).subs(degree, 1)
    if sp.sympify(arg).has(sp.Symbol):
        return sp.asin(arg)
    
    if not -1 <= arg <= 1:
        raise ArcGonioInvalidDomainError()
    return sp.N(sp.deg(sp.asin(arg)), 4) * degree

def acos_deg(arg):
    arg = sp.sympify(arg).subs(degree, 1)
    if sp.sympify(arg).has(sp.Symbol):
        return sp.acos(arg)

    if not -1 <= arg <= 1:
        raise ArcGonioInvalidDomainError()
    return sp.N(sp.deg(sp.acos(arg)), 4) * degree

def atan_deg(arg):
    arg = sp.sympify(arg).subs(degree, 1)
    if sp.sympify(arg).has(sp.Symbol):
        return sp.atan(arg)

    return sp.N(sp.deg(sp.atan(arg)), 4) * degree

def asec_deg(arg):
    arg = sp.sympify(arg).subs(degree, 1)
    if sp.sympify(arg).has(sp.Symbol):
        return sp.asec(arg)

    if -1 <= arg <= 1:
        raise ArcReciprocalInvalidDomainError()
    return sp.N(sp.deg(sp.asec(arg)), 4) * degree

def acsc_deg(arg):
    arg = sp.sympify(arg).subs(degree, 1)
    if -1 <= arg <= 1:
        raise ArcReciprocalInvalidDomainError()
    return sp.N(sp.deg(sp.acsc(arg)), 4) * degree

def acot_deg(arg):
    return sp.N(sp.deg(sp.acot(arg)), 4) * degree

DEG_ARC_GONIO_LOCALS = {
    "asin": asin_deg,
    "acos": acos_deg,
    "atan": atan_deg,
    "asec": asec_deg,
    "acsc": acsc_deg, 
    "acot": acot_deg,
    "angle": angle_deg
}


class CustomLatexPrinter(LatexPrinter):
    """
    A custom LaTeX printer that provides customized formatting for SymPy expressions.
    """

    def __init__(self, **kwargs):
        self.symbol = kwargs.get("symbol", "x")
        self.vect_dim = kwargs.get("vect_dim", 3)
        super().__init__()

    def _print_Union(self, expr, **kwargs):
        """
        Customize the printing of Union (for trigonometric periodic solutions).
        Example: x = a + 2k*pi or x = b + 2k*pi instead of set notation.
        """

        # Extract individual sets from the union
        parts = []
        for arg in expr.args:
            # Look for expressions in the form {2n*pi + constant | n ∈ Z}
            if isinstance(arg, sp.ImageSet):
                # We assume the form 2n*pi + constant for periodic solutions
                element_expr: sp.Expr = sp.expand(arg.lamda.expr)
                variable = list(arg.lamda.variables)[0]

                coeff, summation = element_expr.as_coeff_add()
                if coeff != 0:
                    summation = (coeff, *summation)

                summation = [f"k \\cdot {str(self._print(element)).replace("n", "")}" if "_n" in str(element) else self._print(element) for element in summation]
 
                # Format the periodic solution in the form a + 2k*pi
                formatted_expr = f"{' + '.join(summation)}".replace("n", "k")
                parts.append(formatted_expr)

        # Join the parts with the OR symbol
        return f' \\ \\vee \\ {self.symbol} = '.join(parts)
    
    def _print_ImageSet(self, expr, **kwargs):
        """
        Customize the printing of ImageSet (for trigonometric periodic solutions).
        Example: x = a + 2k*pi instead of set notation.
        """

        # We assume the form 2n*pi + constant for periodic solutions
        element_expr: sp.Expr = sp.expand(expr.lamda.expr)
        variable = list(expr.lamda.variables)[0]

        coeff, summation = element_expr.as_coeff_add()
        if coeff != 0:
            summation = (coeff, *summation)

        summation = [f"k \\cdot {str(self._print(element)).replace("n", "")}" if "_n" in str(element) else self._print(element) for element in summation]

        # Format the periodic solution in the form a + 2k*pi
        formatted_expr = f"{' + '.join(summation)}".replace("n", "k")
        return formatted_expr

     
    def _print_Relational(self, expr, **kwargs):
        """
        Customize the printing of relational expressions (e.g., inequalities).

        Args:
            expr (sp.Relational): The relational expression to print.

        Returns:
            str: The LaTeX representation of the relational expression.
        """

        lhs = expr.lhs
        rhs = expr.rhs

        # If the relation is flipped, reverse the relation and swap lhs and rhs
        if lhs.is_Symbol:
            return super()._print_Relational(expr, **kwargs)
        else:
            flipped_relation = flip_inequality_sign(expr.rel_op)
            flipped_relation = equation_type_to_latex(flipped_relation)
            return f"{self._print(rhs)} {flipped_relation} {self._print(lhs)}"
        
    def _print_Or(self, expr, **kwargs):
        """
        Customize the printing of Or expressions by controlling the order of arguments.

        Args:
            expr (sp.Or): The Or expression to print.

        Returns:
            str: The LaTeX representation of the Or expression.
        """

        if len(expr.args) != 2:
            return super()._print_Or(expr, **kwargs)

        ordered_args = [expr.args[1], expr.args[0]]

        # Convert the ordered arguments to LaTeX
        latex_args = [self._print(arg) for arg in ordered_args]

        # Join the LaTeX strings with the \vee symbol
        return ' \\ \\vee \\ '.join(latex_args)
    

    def _print_And(self, expr, **kwargs):
        """
        Customize the printing of And expressions by combining inequalities.

        Args:
            expr (sp.And): The And expression to print.

        Returns:
            str: The LaTeX representation of the And expression.
        """

        if len(expr.args) != 2:
            return super()._print_And(expr, **kwargs)
        
        expr_left = expr.args[0]
        expr_right = expr.args[1]


        get_symbol_value_pair = lambda expr: (expr.args[0], expr.args[1]) if expr.args[0].is_Symbol else (expr.args[1], expr.args[0])
        symbol_left, value_left = get_symbol_value_pair(expr_left)
        symbol_right, value_right = get_symbol_value_pair(expr_right)

        if value_left.evalf() < value_right.evalf():
            lower_bound, upper_bound = value_left, value_right
        else:
            lower_bound, upper_bound = value_right, value_left

        if symbol_left != symbol_right or not symbol_left.is_Symbol:
            return super()._print_And(expr, **kwargs)

        def get_proper_smaller_than(inequality_symbol):
            if inequality_symbol == ">=":
                inequality_symbol = "<="
            elif inequality_symbol == ">":
                inequality_symbol = "<"

            return inequality_symbol
        
        left_inequality = equation_type_to_latex(get_proper_smaller_than(expr_left.rel_op))
        right_inequality = equation_type_to_latex(get_proper_smaller_than(expr_right.rel_op))

        return f"{self._print(lower_bound)} {left_inequality} {self._print(symbol_left)} {right_inequality} {self._print(upper_bound)}"
    
    def _print_Rational(self, expr, **kwargs):
        """
        Customize the printing of Rational numbers as 'n \\frac{a}{b}' where n is an integer.

        Args:
            expr (sp.Rational): The rational expression to print.

        Returns:
            str: The LaTeX representation of the rational expression.
        """
        # Separate the expression into integer and fractional parts
        numer, denom = expr.as_numer_denom()
        integer_part = numer // denom
        fractional_part = numer % denom

        if fractional_part == 0:  # If there is no fractional part, print just the integer
            return rf"{integer_part}"       
        elif integer_part == 0:  # If there is no integer part, print just the fraction
            return rf"\frac{{{fractional_part}}}{{{denom}}}"
        elif integer_part == -1:  # If the integer part is negative, print the negative sign
            return rf"- \frac{{{fractional_part}}}{{{denom}}}"
        elif integer_part < -1:  # If the integer part is negative and greater than -1, print both parts
            return rf"{int(numer / denom)} \frac{{{abs(fractional_part)}}}{{{denom}}}"
        else:  # Print both integer and fractional parts
            return rf"{integer_part} \frac{{{fractional_part}}}{{{denom}}}"

    def _print_Mul(self, expr: sp.Mul, **kwargs) -> str:

        """
        Customize the printing of multiplication expressions, especially for logarithmic functions.

        Args:
            expr (sp.Mul): The multiplication expression to print.

        Returns:
            str: The LaTeX representation of the multiplication expression.
        """


        if expr.as_numer_denom()[1] == 1:
            if len(expr.args) == 2 and all(isinstance(arg, CustomVector) for arg in expr.args) and dot(expr.args[0], expr.args[1]).is_number:
                return f"{self._print(expr.args[0])} \\cdot {self._print(expr.args[1])}"
            
            # Default handling with custom modifications
            result = super()._print_Mul(expr).replace("1 \\cdot", " ")
            result = re.sub(r"\\left\(-(\d+)\\right\) ", r"- \1 \\cdot", result)
            return result

        # handle Rationals with a symbol
        if any(expr.has(obj) for obj in [sp.Symbol, sp.pi, sp.E]):
            coeff, sym_part = sp.nsimplify(sp.sympify(str(expr))).as_coeff_Mul()
            numer, denom = coeff.as_numer_denom()
            if denom == 1:
                numer, denom = expr.as_numer_denom()
        else:
            sym_part = 1
            numer, denom = expr.as_numer_denom()

        # Check if we're dealing with a Rational
        if isinstance(numer, sp.Integer) and isinstance(denom, sp.Integer):
            latex = self._print_Rational(sp.Rational(numer, denom), **kwargs)
            if sym_part != 1:
                latex += self._print(sym_part)
            return latex
        
        numer, denom = expr.as_numer_denom()
        
        # Custom handling for logarithms
        if isinstance(numer, sp.log) and isinstance(denom, sp.log):
            arg = numer.args[0]
            base = denom.args[0]

            if isinstance(base, sp.Number):
                arg = self._print(arg)
                base = self._print(base)

                return f' \\ ^{{{base}}} \\! \\log\\left({arg} \\right)'
        
        if expr.has(CustomVector):
            numer, denom = expr.as_numer_denom()
            return f"{self._print(1/denom)} \\cdot {self._print(numer)}"
            
        # Default handling with custom modifications
        result = sp.latex(expr).replace("1 \\cdot", " ")
        result = re.sub(r"\\left\(-(\d+)\\right\) ", r"- \1 \\cdot", result)
        return result
    

    def _print_Pow(self, expr: sp.Pow, **kwargs) -> str:
        """
        Customize the printing of power expressions.

        Args:
            expr (sp.Pow): The power expression to print.

        Returns:
            str: The LaTeX representation of the power expression.
        """

        base, exp = expr.as_base_exp()

        if expr.is_Rational and exp.q != 1 and expr != sp.root(base, 1/exp, evaluate=False):
            base = self._print(base)
            exp = self._print(sp.simplify(exp))
            return f"{base}^{{{exp}}}"

        elif expr.as_numer_denom()[1] != 1:
            expr = sp.nsimplify(expr)
            return sp.latex(expr)

        if any(base.has(class_) for class_ in [CustomVector, sp_vector.Gradient]) and any(exp.has(class_) for class_ in [CustomVector, sp_vector.Gradient]):
            # For vectors and gradients, use the cross product symbol
            base_str = self._print(base)
            exp_str = self._print(exp)
            return f"{base_str} \\times {exp_str}"

        result = sp.latex(expr)
        result = result.replace("log", "ln").replace("circ", "\\circ")
        return result

    def _print_log(self, expr: sp.log, **kwargs) -> str:
        """
        Customize the printing of logarithmic expressions.

        Args:
            expr (sp.log): The logarithmic expression to print.

        Returns:
            str: The LaTeX representation of the logarithmic expression.
        """

        arg = self._print(expr.args[0])

        # Natural logarithm
        if len(expr.args) == 1:
            return f'\\ln \\left({arg} \\right)'
        
        # Logarithm with a specific base
        elif len(expr.args) == 2:
            base = self._print(expr.args[1])
            return f' \\ ^{{{base}}} \\! \\log\\left({arg} \\right)'
            
        # Fallback for unexpected cases
        return super()._print_log(expr)
        

    def _print_Limit(self, expr: sp.Limit, **kwargs) -> str:
        """
        Customize the printing of limit expressions.

        Args:
            expr (sp.Limit): The limit expression to print.

        Returns:
            str: The LaTeX representation of the limit expression.
        """

        func, var, point, direction = expr.args
        limit_expr = str(expr)
        limit_value = sp.simplify(expr)

        if str(direction) == "+":
            limit_expr_opposite = limit_expr.replace("dir='+'", "dir='-'")
        else:
            limit_expr_opposite = limit_expr.replace("dir='-'", "dir='+'")
        
        limit_value_opposite = sp.simplify(limit_expr_opposite)


        if limit_value == limit_value_opposite:
            return f"\\lim_{{{self._print(var)} \\, \\to \\, {self._print(point)}}} {self._print(func)}"
        
        elif str(direction) == "+":
            return f"\\lim_{{{self._print(var)} \\, \\downarrow \\, {self._print(point)}}} {self._print(func)}"
        
        elif str(direction) == "-":
            return f"\\lim_{{{self._print(var)} \\, \\uparrow \\, {self._print(point)}}} {self._print(func)}"

        # Fallback just in case
        return super()._print_Limit(expr)
    
    
    def _print_Function(self, expr: sp.Function, **kwargs) -> str:
        """
        Customize the printing of specific mathematical functions.

        Args:
            expr (sp.Function): The function expression to print.

        Returns:
            str: The LaTeX representation of the function expression.
        """

        func_name = expr.func.__name__
        func_map = {
            'asin': '\\arcsin',
            'acos': '\\arccos',
            'atan': '\\arctan',
            'asec': '\\arcsec',
            'acsc': '\\arccsc',
            'acot': '\\arccot',
        }

        if func_name in func_map:
            return rf'{func_map[func_name]}{{\left({self._print(expr.args[0])}\right)}}'
        
        return super()._print_Function(expr, **kwargs)
    

    def _print_Vector(self, expr: sp_vector.Vector, **kwargs) -> str:
        """
        Customize the printing of Vector objects in a single column format.

        Args:
            expr (Vector): The vector expression to print.

        Returns:
            str: The LaTeX representation of the vector expression.
        """
        unit_vects = [r.i, r.j, r.k]
        unit_vects = unit_vects[:self.vect_dim]

        # Get the components of the vector
        components = [expr.dot(unit_vect) for unit_vect in unit_vects]

        # Format the components into a LaTeX column vector
        latex_vector = r'\begin{pmatrix}' + r'\\'.join([self._print(c) for c in components]) + r'\end{pmatrix}'

        
        return latex_vector
    
    def _print_Magnitude(self, expr, **kwargs):
        # Custom LaTeX format for Magnitude
        return rf"\left| {self._print(expr.args[0])} \right|"
    

    def _print_Angle(self, expr, **kwargs):
        # Custom LaTeX format for Angle
        return rf"\angle \left( {self._print(expr.args[0])}, {self._print(expr.args[1])} \right)"
    

def custom_latex(expr: sp.Expr, **kwargs) -> str:
    """
    Convert a SymPy expression to a custom LaTeX representation.

    Args:
        expr (sp.Expr): The SymPy expression to convert.

    Returns:
        str: The LaTeX representation of the expression.
    """

    def latex_vectors(match: re.Match):
        if r"\begin{pmatrix}" in match.group(2):
            return match.group(0)
        
        return match.group(1)

    latex_str = CustomLatexPrinter(**kwargs).doprint(expr)
    vector_pattern = re.escape(r"\left(") + "(" + re.escape(r"\begin{pmatrix}") + r"(.*?)" + re.escape(r"\end{pmatrix}")+ ")" + re.escape(r"\right)")
    latex_str = re.sub(vector_pattern, latex_vectors, latex_str)
    # latex_str = latex_str.replace(r"\left(\begin{pmatrix}", r"\begin{pmatrix}").replace(r"\end{pmatrix}\right)", r"\end{pmatrix}")
    return latex_str


def custom_simplify(expr: typing.Union[sp.Basic, Number]) -> typing.Union[sp.Basic, Number]:
    """
    Simplify a SymPy expression with custom logic.

    Args:
        expr: The expression to simplify.

    Returns:
        sp.Basic: The simplified expression, or the original expression if simplification fails.
    """
    if not isinstance(expr, sp.Basic):
        return expr

    if expr.is_number:
        return sp.nsimplify(expr)

    try:
        symp_expr = sp.simplify(expr)
        return sp.expand_log(symp_expr)
    except Exception:
        pass

    try:
        return symp_expr
    except UnboundLocalError:
        return expr
    
def get_real_root(expr: sp.Expr):
    def replace_root(matched_expr):
        base = matched_expr.group(1)
        power = matched_expr.group(2)
        power_sp = sp.sympify(power)
        if power_sp.q % 2 == 0 or power_sp.p % 2 == 0:
            return f"Abs({base})**({power})"
        return f"sign({base})*Abs({base})**({power})"
        

    str_expr = str(expr)

    str_expr = re.sub(r"(\w*\(.*\))\*\*\((-*\d+/\d+)\)", replace_root, str_expr)
    str_expr = re.sub(r"(\w+)\*\*\((-*\d+/\d+)\)", replace_root, str_expr)

    expr = sp.sympify(str_expr)
    return expr