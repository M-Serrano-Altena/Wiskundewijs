import scipy.optimize
from scipy.interpolate import UnivariateSpline
import sympy as sp
from sympy.simplify.fu import TR2, TR1, TR111
import numpy as np
import regex as re
import matplotlib.pyplot as plt
from sympy.printing.latex import LatexPrinter
import ast
from src.Solver.src.solver.math_parser import math_interpreter, get_uneval_sp_objs, latex_to_plain_text
from types import FunctionType
from collections.abc import Iterable
import typing
import operator

def equation_type_to_latex(equation_symbol):
    equation_type_latex_map = {"!=": "\\neq", ">=": "\\geq", "<=": "\\leq", "==": "="}
    return equation_type_latex_map.get(equation_symbol, equation_symbol)

def flip_inequality_sign(inequality_sign):
    """
    Flip the sign of an inequality.

    Args:
        inequality_sign (str): The inequality sign to flip.

    Returns:
        str: The flipped inequality sign.
    """
    inequality_flip_replacements = {">": "<", "<": ">", ">=": "\\leq", "<=": "\\geq", "!=": "=", "=": "\\neq"}
    return inequality_flip_replacements.get(inequality_sign, inequality_sign)

class CustomLatexPrinter(LatexPrinter):
    """
    A custom LaTeX printer that provides customized formatting for SymPy expressions.
    """

     
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

        symbol_left = expr_left.args[1]
        symbol_right = expr_right.args[0]
        lower_bound = expr_left.args[0]
        upper_bound = expr_right.args[1]

        if not symbol_left.is_Symbol or not symbol_right.is_Symbol:
            symbol_left = expr_left.args[0]
            symbol_right = expr_right.args[1]
            lower_bound = expr_left.args[1]
            upper_bound = expr_right.args[0]

        if symbol_left != symbol_right or not symbol_left.is_Symbol:
            return super()._print_And(expr, **kwargs)
        
        if lower_bound.evalf() > upper_bound.evalf():
            lower_bound, upper_bound = upper_bound, lower_bound

        left_inequality = equation_type_to_latex(expr_left.rel_op)
        right_inequality = equation_type_to_latex(expr_right.rel_op)

        return f"{self._print(lower_bound)} {left_inequality} {self._print(symbol_left)} {right_inequality} {self._print(upper_bound)}"
    

    def _print_Mul(self, expr: sp.Mul, **kwargs) -> str:

        """
        Customize the printing of multiplication expressions, especially for logarithmic functions.

        Args:
            expr (sp.Mul): The multiplication expression to print.

        Returns:
            str: The LaTeX representation of the multiplication expression.
        """

        numer, denom = expr.as_numer_denom()

        # Custom handling for logarithms
        if isinstance(numer, sp.log) and isinstance(denom, sp.log):
            arg = numer.args[0]
            base = denom.args[0]

            if isinstance(base, sp.Number):
                arg = self._print(numer)
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
        

        return sp.latex(expr).replace("log", "ln")

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
    

def custom_latex(expr: sp.Basic, **kwargs) -> str:
    """
    Convert a SymPy expression to a custom LaTeX representation.

    Args:
        expr (sp.Basic): The SymPy expression to convert.

    Returns:
        str: The LaTeX representation of the expression.
    """

    return CustomLatexPrinter(**kwargs).doprint(expr)


x, y = sp.symbols("x,y", real=True)

string = r"(x == 2)"
string = math_interpreter(string)
print(string)

# # print([''.join([])])
# l = [1,1,2,3,4]
# dummy_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
# print("key1" in dummy_dict.keys())
# # func = sp.sympify("1/((x)**(2/3))")
# # print(func)




solution = sp.solve(sp.Lt(x**2, 4 - x**2), x)
print(solution)
print(custom_latex(solution))
