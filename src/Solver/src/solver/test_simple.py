import regex as re
import sympy as sp
from sympy.parsing.latex import parse_latex

from pylatexenc.latex2text import LatexNodes2Text

constant_names_og = [name for name, obj in sp.__dict__.items() if isinstance(obj, (sp.Basic, sp.core.singleton.Singleton)) and not name.startswith('_') and sp.sympify(name).is_number]
print([type(const) for const in constant_names_og])

empty = []
print(re.findall('5', '5'))