import sympy as sp
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

if __name__ == "__main__":
    x = sp.symbols('x')
    eq = sp.lambdify(x, 0)
    print(eq(5))
    # main()