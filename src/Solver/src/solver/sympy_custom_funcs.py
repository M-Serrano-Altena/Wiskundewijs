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
import typing
from numbers import Number


r = sp_vector.CoordSys3D('r')
vect_dim = None

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
    

        x = [symbol for symbol in free_symbols if symbol.name == "x"]
        y = [symbol for symbol in free_symbols if symbol.name == "y"]
        z = [symbol for symbol in free_symbols if symbol.name == "z"]

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

    if vect_dim == 1:
        return args[0] * r.i
    elif vect_dim == 2:
        return args[0] * r.i + args[1]*r.j
    
    return args[0]*r.i + args[1]*r.j + args[2]*r.k

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
    return sp_vector.gradient(expr)

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


def equation_type_to_latex(equation_symbol):
    """
    Maps common inequality symbols to their LaTeX equivalents.

    Parameters:
        equation_symbol (str): The symbol representing the type of equation or inequality.

    Returns:
        str: The LaTeX representation of the inequality or the original symbol if not in the map.
    
    Examples:
        - "!=" maps to "\\neq"
        - ">=" maps to "\\geq"
    """
    equation_type_latex_map = {"!=": "\\neq", ">=": "\\geq", "<=": "\\leq"}
    return equation_type_latex_map.get(equation_symbol, equation_symbol)

def flip_inequality_sign(inequality_sign):
    """
    Flip the sign of an inequality.

    Args:
        inequality_sign (str): The inequality sign to flip.

    Returns:
        str: The flipped inequality sign.
    """
    inequality_flip_replacements = {">": "<", "<": ">", ">=": "<=", "<=": ">=", "!=": "=", "=": "!="}
    return inequality_flip_replacements.get(inequality_sign, inequality_sign)

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

LOCALS = {
    "vect": vect, 
    "Abs": Abs, 
    "r": r,
    "dot": sp_vector.dot,
    "Dot": sp_vector.Dot,
    "cross": sp_vector.cross,
    "Cross": sp_vector.Cross,
    "div": sp_vector.divergence, 
    "Divergence": sp_vector.Divergence,
    "curl": sp_vector.curl, 
    "Curl": sp_vector.Curl,
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
                latex += sp.latex(sym_part)
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
            
        # Default handling with custom modifications
        result = super()._print_Mul(expr).replace("1 \\cdot", " ")
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
        

        return sp.latex(expr).replace("log", "ln").replace("circ", "\\circ")

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
    

def custom_latex(expr: sp.Expr, **kwargs) -> str:
    """
    Convert a SymPy expression to a custom LaTeX representation.

    Args:
        expr (sp.Expr): The SymPy expression to convert.

    Returns:
        str: The LaTeX representation of the expression.
    """
    latex_str = CustomLatexPrinter(**kwargs).doprint(expr)
    latex_str = latex_str.replace(r"\left(\begin{pmatrix}", r"\begin{pmatrix}").replace(r"\end{pmatrix}\right)", r"\end{pmatrix}")
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