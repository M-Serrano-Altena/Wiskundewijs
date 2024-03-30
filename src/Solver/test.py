import sympy as sp
import numpy as np
import re

def main():
    eq_string = "2x^2 + 1 = 9"
    eq_string = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_string)
    eq_split = eq_string.split("=")
    print(eq_split)

    if len(eq_split) == 1:
        eq = sp.Eq(sp.sympify(eq_split[0]), 0)

    elif len(eq_split) == 2:
        eq = sp.Eq(sp.sympify(eq_split[0]), sp.sympify(eq_split[1]))

    else:
        print("Invalid equation")
        return
        
    solutions = sp.solve(eq)
    symbol = eq.free_symbols.pop()
    for solution in solutions:
        print(f"{symbol} = {solution}")

def no_frac(num):
    if isinstance(num, sp.Rational) and (abs(num.p) > 100 or abs(num.q) > 100):
        return num.evalf()
    return num
    

if __name__ == "__main__":

    x = sp.symbols('x')
    eq = sp.Eq(sp.cos(x)**2+sp.sin(x)**2 + x, 1)

    solution_set = sp.solveset(sp.simplify(eq))
    if isinstance(solution_set, sp.ConditionSet):
        print(f"Variable: {solution_set.sym}, Condition: {solution_set.condition}")
    else:
        sp.pprint(solution_set)
        
    # main()