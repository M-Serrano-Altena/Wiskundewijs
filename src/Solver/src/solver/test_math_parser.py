import os
import pytest

os.chdir(os.path.dirname(os.path.abspath(__file__)))
from src.Solver.src.solver.math_parser import *



def test_math_interpreter_proper_no_functions():
    string = "2*x + 44 - 6/3"
    string = math_interpreter(string)
    assert string == "2*x + 44 - 6/3"

def test_math_interpreter_proper_with_functions():
    string = "sin(x) + 44 - 6/3"
    string = math_interpreter(string)
    assert string == "sin(x) + 44 - 6/3"

def test_math_interpreter_num_besides_symbol():
    string = "4x - 3y + 2"
    string = math_interpreter(string)
    assert string == "4*x - 3*y + 2"

def test_math_interpreter_num_besides_symbol_with_functions():
    string = "4sin(x) - 3y + 2"
    string = math_interpreter(string)
    assert string == "4*sin(x) - 3*y + 2"

def test_math_interpreter_num_besides_symbol_with_parentheses():
    string = "3(x + 2)"
    string = math_interpreter(string)
    assert string == "3*(x + 2)"

def test_math_interpreter_no_space():
    string = "3(x+2)"
    string = math_interpreter(string)
    assert string == "3*(x+2)"

def test_math_interpreter_function_no_parentheses():
    string = "sin x"
    string = math_interpreter(string)
    assert string == "sin(x)"

def test_math_interpreter_function_no_parentheses_no_space():
    string = "sinx"
    string = math_interpreter(string)
    assert string == "sin(x)"


def test_math_interpreter_function_no_parentheses_with_num():
    string = "sin 2x"
    string = math_interpreter(string)
    assert string == "sin(2*x)"

def test_math_interpreter_function_no_parentheses_with_num_and_symbol():
    string = "sin 2x + 3y"
    string = math_interpreter(string)
    assert string == "sin(2*x) + 3*y"

def test_math_interpreter_constant():
    string = "pi"
    string = math_interpreter(string)
    assert string == "pi"

def test_math_interpreter_constant_with_num():
    string = "2pi"
    string = math_interpreter(string)
    assert string == "2*pi"

def test_math_interpreter_constants_with_num_and_symbol():
    string = "2pi + 3e + 4x"
    string = math_interpreter(string)
    assert string == "2*pi + 3*E + 4*x"

def test_math_interpreter_constants_as_func_args():
    string = "sin pi"
    string = math_interpreter(string)
    assert string == "sin(pi)"

def test_math_interpreter_constants_as_func_args_with_num():
    string = "sin 2pi"
    string = math_interpreter(string)
    assert string == "sin(2*pi)"

def test_math_interpreter_multiple_constants_as_func_args_with_num():
    string = "expipi"
    string = math_interpreter(string)
    assert string == "exp(I*pi)"

def test_math_interpreter_definite_integral_no_symbol():
    string = "integrate(sin(x), (0, 1))"
    string = math_interpreter(string)
    assert string == "integrate(sin(x), (x, 0, 1))"

def test_math_interpreter_definite_integral_with_symbol():
    string = "integrate(sin(x), (x, 0, 1))"
    string = math_interpreter(string)
    assert string == "integrate(sin(x), (x, 0, 1))"

def test_math_interpreter_indefinite_integral_no_symbol():
    string = "integrate(sin(x))"
    string = math_interpreter(string)
    assert string == "integrate(sin(x))"

def test_math_interpreter_indefinite_integral_with_symbol():
    string = "integrate(sin(x), x)"
    string = math_interpreter(string)
    assert string == "integrate(sin(x), x)"

def test_math_interpreter_log_no_base():
    string = "log(x)"
    string = math_interpreter(string)
    assert string == "log(x, 10)"

def test_math_interpreter_log_with_base():
    string = "log(x, 2)"
    string = math_interpreter(string)
    assert string == "log(x, 2)"

def test_math_interpreter_ln():
    string = "ln(x)"
    string = math_interpreter(string)
    assert string == "ln(x)"

def test_math_interpreter_log_with_num():
    string = "log(2)"
    string = math_interpreter(string)
    assert string == "log(2, 10)"

def test_math_interpreter_log_with_num_and_symbol():
    string = "log(2x)"
    string = math_interpreter(string)
    assert string == "log(2*x, 10)"

def test_math_interpreter_nested_functions():
    string = "sin(cos(x))"
    string = math_interpreter(string)
    assert string == "sin(cos(x))"

def test_math_interpreter_nested_functions_with_num():
    string = "sin(2cos(x))"
    string = math_interpreter(string)
    assert string == "sin(2*cos(x))"

def test_math_interpreter_nested_functions_with_num_and_symbol():
    string = "sin(2cos(x) + 3y)"
    string = math_interpreter(string)
    assert string == "sin(2*cos(x) + 3*y)"

def test_math_interpreter_nested_functions_no_parentheses():
    string = "sin cosx"
    string = math_interpreter(string)
    assert string == "sin(cos(x))"

def test_math_interpreter_nested_functions_no_parentheses_no_space():
    string = "sincosx"
    string = math_interpreter(string)
    assert string == "sin(cos(x))"

def test_math_interpreter_function_names_containing_another_function():
    string = "sinh(x)"
    string = math_interpreter(string)
    assert string == "sinh(x)"

def test_math_interpreter_function_names_containing_another_function_no_parentheses():
    string = "sinhx + sincx"
    string = math_interpreter(string)
    assert string == "sinh(x) + sinc(x)"

def test_math_interpreter_function_names_containing_another_function_no_parentheses_no_space():
    string = "sinhx+sincx"
    string = math_interpreter(string)
    assert string == "sinh(x)+sinc(x)"

def test_math_interpreter_latex_frac():
    string = r"\frac{1}{2}"
    string = math_interpreter(string)
    assert string == "1/2"

def test_math_interpreter_latex_frac_with_symbol():
    string = r"\frac{1}{2}x"
    string = math_interpreter(string)
    assert string == "1/2*x"

def test_math_interpeter_latex_basic_functions():
    string = r"\sin(x) + \cos(x)"
    string = math_interpreter(string)
    assert string == "sin(x) + cos(x)"

def test_math_interpreter_latex_sqrt():
    string = r"\sqrt{x}"
    string = math_interpreter(string)
    assert string == "sqrt(x)"

def test_math_interpreter_latex_sqrt_with_num():
    string = r"\sqrt{2}x"
    string = math_interpreter(string)
    assert string == "sqrt(2)*x"

def test_math_interpreter_cbrt():
    string = "root(x, 3)"
    string = math_interpreter(string)
    assert string == "root(x, 3)"

def test_math_interpreter_latex_cbrt():
    string = r"\sqrt[3]{x}"
    string = math_interpreter(string)
    assert string == "root(x, 3)"

def test_math_interpreter_latex_fourth_root():
    string = r"\sqrt[4]{x}"
    string = math_interpreter(string)
    assert string == "root(x, 4)"

def test_math_interpreter_latex_frac_with_symbol():
    string = r"\frac{1}{2}x"
    string = math_interpreter(string)
    assert string == "1/2*x"

def test_math_interpreter_latex_frac_with_symbol_and_func():
    string = r"\frac{1}{2}sin(x)"
    string = math_interpreter(string)
    assert string == "1/2*sin(x)"

def test_math_interpreter_latex_frac_expression():
    string = r"\frac{1 + 2}{3}"
    string = math_interpreter(string)
    assert string == "(1 + 2)/(3)"

def test_math_interpreter_latex_derivative():
    string = r"\frac{d}{dx}sin(x)"
    string = math_interpreter(string)
    assert string == "diff(sin(x), x)"

def test_math_interpreter_latex_derivative_with_num():
    string = r"\frac{d}{dx}2sin(x)"
    string = math_interpreter(string)
    assert string == "diff(2*sin(x), x)"

def test_math_interpreter_latex_derivative_with_num_and_symbol():
    string = r"\frac{d}{dx}2sin(x) + 3y"
    string = math_interpreter(string)
    assert string == "diff(2*sin(x), x) + 3*y"

def test_math_interpreter_latex_derivative_with_num_and_symbol_parentheses():
    string = r"\frac{d}{dx}(2sin(x) + 3y)"
    string = math_interpreter(string)
    assert string == "diff(2*sin(x) + 3*y, x)"

def test_math_interpreter_derivative_d_dx():
    string = "d/dx sin(x)"
    string = math_interpreter(string)
    assert string == "diff(sin(x), x)"

def test_math_interpreter_double_derivative_d_dx():
    string = "d^2/dx^2 sin(x)"
    string = math_interpreter(string)
    assert string == "diff(sin(x), x, 2)"

def test_math_interpreter_derivative_different_variable():
    string = "d/dy sin(x)"
    string = math_interpreter(string)
    assert string == "diff(sin(x), y)"

def test_math_interpreter_latex_integral():
    string = r"\int sin(x) dx"
    string = math_interpreter(string)
    assert string == "integrate(sin(x), x)"

def test_math_interpreter_latex_integral_with_limits():
    string = r"\int_{0}^{1} sin(x) dx"
    string = math_interpreter(string)
    assert string == "integrate(sin(x), (x, 0, 1))"

def test_math_interpreter_latex_integral_with_limits_and_symbol():
    string = r"\int_{0}^{pi} sin(x) dy"
    string = math_interpreter(string)
    assert string == "integrate(sin(x), (y, 0, pi))"

def test_math_interpreter_latex_integral_and_derivative():
    string = r"\int_{0}^{pi} \frac{d}{dx}sin(x) dx"
    string = math_interpreter(string)
    assert string == "integrate(diff(sin(x), x), (x, 0, pi))"

def test_math_interpreter_back_to_back_functions():
    string = "sinxcosx"
    string = math_interpreter(string)
    assert string == "sin(x)*cos(x)"

def test_math_interpreter_back_to_back_functions_flipped():
    string = "cosxsinx"
    string = math_interpreter(string)
    assert string == "cos(x)*sin(x)"

def test_math_interpreter_back_to_back_functions_with_space():
    string = "sin x cos x"
    string = math_interpreter(string)
    assert string == "sin(x)*cos(x)"

def test_math_interpreter_back_to_back_functions_with_constant():
    string = "2sinpicosx"
    string = math_interpreter(string)
    assert string == "2*sin(pi)*cos(x)"

def test_math_interpreter_back_to_back_functions_with_constant_and_space():
    string = "2 sin pi cos x"
    string = math_interpreter(string)
    assert string == "2*sin(pi)*cos(x)"

def test_math_interpreter_nested_log_in_complex_expression():
    string = "log(2log(3x)) + 5log(7 + log(3 * 10^(log(100))))"
    string = math_interpreter(string)
    assert string == "log(2*log(3*x, 10), 10) + 5*log(7 + log(3 * 10^(log(100, 10)), 10), 10)"

def test_math_interpreter_5_chained_logs():
    string = "logloglogloglogx"
    string = math_interpreter(string)
    assert string == "log(log(log(log(log(x, 10), 10), 10), 10), 10)"

def test_math_interpreter_derivative_dot_notation():
    string = "sin(x).diff()"
    string = math_interpreter(string)
    assert string == "sin(x).diff()"

def test_math_interpreter_derivative_dot_notation_with_variable():
    string = "sin(x).diff(x)"
    string = math_interpreter(string)
    assert string == "sin(x).diff(x)"

def test_math_interpreter_double_derivative_dot_notation():
    string = "2sin(x).diff(2)"
    string = math_interpreter(string)
    assert string == "2*sin(x).diff(x, 2)"

def test_math_interpreter_definite_integral_dot_notation():
    string = "sin(x).integrate((0, 1))"
    string = math_interpreter(string)
    assert string == "sin(x).integrate((x, 0, 1))"

def test_math_interpreter_definite_integral_dot_notation_single_parentheses():
    string = "sin(x).integrate(0, 1)"
    string = math_interpreter(string)
    assert string == "sin(x).integrate((x, 0, 1))"
    
def test_math_interpreter_definite_integral_dot_notation_single_parentheses_with_var():
    string = "sin(x).integrate(x, 0, 1)"
    string = math_interpreter(string)
    assert string == "sin(x).integrate((x, 0, 1))"

def test_math_interpreter_definite_integral_dot_notation_with_variable():
    string = "sin(x).integrate((x, 0, 1))"
    string = math_interpreter(string)
    assert string == "sin(x).integrate((x, 0, 1))"

def test_math_interpreter_indefinite_integral_dot_notation():
    string = "sin(x).integrate(x)"
    string = math_interpreter(string)
    assert string == "sin(x).integrate(x)"

def test_math_interpreter_indefinite_integral_dot_notation_no_var():
    string = "sin(x).integrate()"
    string = math_interpreter(string)
    assert string == "sin(x).integrate()"

def test_math_interpreter_mixed_fractions():
    string = "1 1/2"
    string = math_interpreter(string)
    assert string == "(1+1/2)"

def test_math_interpreter_mixed_fractions_with_symbol():
    string = "1 1/2x"
    string = math_interpreter(string)
    assert string == "(1+1/2)*x"

def test_math_interpreter_potential_mixed_fractions_with_symbol():
    string = "4 x/2 + 2 1/2"
    string = math_interpreter(string)
    assert string == "4*x/2 + (2+1/2)"

def test_math_interpreter_potential_mixed_fractions_with_decimal_numer():
    string = "4 0.2/2"
    string = math_interpreter(string)
    assert string == "4*0.2/2"

def test_math_interpreter_potential_mixed_fractions_with_decimal_denom():
    string = "3 4/0.5"
    string = math_interpreter(string)
    assert string == "3*4/0.5"

def test_math_interpreter_latex_mixed_fraction():
    string = r"1 \frac{1}{2}"
    string = math_interpreter(string)
    assert string == "(1+1/2)"

def test_math_interpreter_latex_mixed_fraction_no_space():
    string = r"1\frac{1}{2}"
    string = math_interpreter(string)
    assert string == "(1+1/2)"

def test_math_interpreter_latex_mixed_fraction_with_symbol():
    string = r"1 \frac{1}{2}x"
    string = math_interpreter(string)
    assert string == "(1+1/2)*x"

def test_math_interpreter_latex_mixed_fraction_with_symbol_no_space():
    string = r"1\frac{1}{2}x"
    string = math_interpreter(string)
    assert string == "(1+1/2)*x"

def test_math_interpreter_latex_mixed_fraction_expression():
    string = r"1 \frac{1 + 2}{3}"
    string = math_interpreter(string)
    assert string == "1*(1 + 2)/(3)"

def test_math_interpreter_latex_mixed_fraction_expression_no_space():
    string = r"1\frac{1 + 2}{3}"
    string = math_interpreter(string)
    assert string == "1*(1 + 2)/(3)"