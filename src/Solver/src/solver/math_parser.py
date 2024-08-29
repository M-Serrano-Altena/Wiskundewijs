import numpy as np
import sympy as sp
import regex as re
from typing import Dict, Union
from pylatexenc.latex2text import LatexNodes2Text

def fix_mismatched_parenthesis(eq_string):
    eq_split = split_equation(eq_string)

    for i in range(len(eq_split)):
        eq_split[i] = eq_split[i].strip()
        count_open_bracket = eq_split[i].count('(')
        count_close_bracket = eq_split[i].count(')')
        difference = count_open_bracket - count_close_bracket
        
        if difference > 0:
            eq_split[i] += difference * ")"
        elif difference < 0:
            eq_split[i] = abs(difference) * "(" + eq_split[i]
    
    eq_string = ' '.join(eq_split)
    return eq_string

def get_arg_in_brackets(eq_string, index_start_bracket, bracket_type="()"):
    map_brackets = {"(": ")", "[" : "]", "{": "}"}

    if len(bracket_type) == 2:
        open_bracket = bracket_type[0]
        close_bracket = bracket_type[1]

    elif len(bracket_type) == 1:
        open_bracket = bracket_type
        close_bracket = map_brackets[bracket_type]

    nested = 0
    index = index_start_bracket
    for char in eq_string[index:]:
        if char == open_bracket:
            nested += 1
        elif char == close_bracket:
            nested -= 1
            if nested == 0:
                index_close_bracket = index
                arg_in_parenthesis = eq_string[index_start_bracket+1:index_close_bracket]
                return arg_in_parenthesis, index

        index += 1

    return "PLACEHOLDER", index


def interpret_latex_root(eq_string):
    def interpret_latex_sqrt(eq_string):
        index_sqrt = [m.start() for m in re.finditer(r"\\sqrt\[", eq_string)]
        index_start_square_brackets = [index + 5 for index in index_sqrt]
        if not index_sqrt:
            return eq_string
        
        for index in index_start_square_brackets:
            root_exp, index =  get_arg_in_brackets(eq_string, index, bracket_type="[]")
            eq_string = re.sub(rf"\\sqrt\[({re.escape(root_exp)})\]" + r"([\w\p{Greek}])", r"root(\2, \1)", eq_string)
            index += 1

            sqrt_arg, _ = get_arg_in_brackets(eq_string, index, bracket_type="()")
            eq_string = re.sub(rf"\\sqrt\[({re.escape(root_exp)})\]\(({re.escape(sqrt_arg)})\)", r"root(\2, \1)", eq_string)

            sqrt_arg, _ = get_arg_in_brackets(eq_string, index, bracket_type=r"{}")
            eq_string = re.sub(rf"\\sqrt\[({re.escape(root_exp)})\]" + r"\{(" + re.escape(sqrt_arg) + r")\}", r"root(\2, \1)", eq_string)

        return eq_string

    def interpret_fourth_root(eq_string):
        index_fourth_root = [m.start() for m in re.finditer(r"∜\(", eq_string)]
        index_start_brackets = [index + 1 for index in index_fourth_root]
        if not index_fourth_root:
            return eq_string
        
        for index in index_start_brackets:
            root_arg, index =  get_arg_in_brackets(eq_string, index)
            eq_string = re.sub(rf"∜\(({re.escape(root_arg)})\)", r"root(\1, 4)", eq_string)

        return eq_string

    replacements = [
        (r"\\sqrt\{", r"sqrt"),
        (r"\\sqrt\(", r"sqrt("),  # \sqrt(x) --> √(x)
        (r"∜([\w\p{Greek}])", r"root(\1, 4)"),  # ∜x --> root(x, 4)
    ]

    for pattern, repl in replacements:
        eq_string = re.sub(pattern, repl, eq_string)

    eq_string = interpret_latex_sqrt(eq_string)
    eq_string = interpret_fourth_root(eq_string)

    return eq_string


def interpret_integral(eq_string):
    def interpret_integral_replacement(eq_string):
        index_integral = [m.start() for m in re.finditer(r"∫_", eq_string)]
        if not index_integral:
            return eq_string
        
        for index in index_integral:
            matched_args = []
            continue_ = False
            for char in ["_", "^"]:
                if index + 2 >= len(eq_string) or eq_string[index+1] != char:
                    continue_ = True
                    break
                
                index += 2
                matched_arg, index = get_arg_in_brackets(eq_string, index)
                matched_args.append(matched_arg)

            if continue_:
                continue

            matched_subscript, matched_superscript = matched_args

            eq_string = re.sub(rf"∫_\(({re.escape(matched_subscript)})\)\^\(({re.escape(matched_superscript)})\)\s*([^∫]*?)\s*" + r"(?<!d/)d(\p{L})(?=\b|d\p{L})", r"integrate(\3, (\4, \1, \2))", eq_string)

        return eq_string

    format_integral = [
        (r"∫\s*_\s*(\d+|[\w\p{Greek}])\s*\^\s*(\d+|[\w\p{Greek}])", r"∫_(\1)^(\2)"),
        (r"∫\s*_\s*(\d+|[\w\p{Greek}])\s*\^\s*\((.*?)\)", r"∫_(\1)^(\2)"),
        (r"∫\s*_\s*\((.*?)\)\s*\^\s*(\d+|[\w\p{Greek}])", r"∫_(\1)^(\2)"),
        (r"∫\s*_\s*\(([^∫]*?)\)\s*\^\s*\((.*?)\)", r"∫_(\1)^(\2)"),
    ]

    for pattern, repl in format_integral:
        eq_string = re.sub(pattern, repl, eq_string)

    for _ in range(100):
        eq_string_before = eq_string
        eq_string = re.sub(r"∫(?!(?:\s*_\s*\([^∫]*?\)\s*\^\s*\([^∫]*?\)))\s*([^∫]*?)\s*d(\p{L})\b", r"integrate(\1, \2)", eq_string)
        eq_string = interpret_integral_replacement(eq_string)
        if eq_string == eq_string_before:
            break

    return eq_string


def interpret_derivative(eq_string):
    index_derivative = [m.end() for m in re.finditer(r"d/d\p{L}", eq_string)]
    index_nth_derivative = [m.end() for m in re.finditer(r"d\^\((\d+)\)/d(\p{L})\^\(\1\)", eq_string)]

    if not (index_derivative or index_nth_derivative):
        return eq_string
    
    diff_args = []
    for index in index_derivative:
        diff_arg, _ =  get_arg_in_brackets(eq_string, index)
        diff_args.append(diff_arg)

    for diff_arg in diff_args:
        eq_string = re.sub(rf"d/d(" + r"\p{L}" + rf")\s*\(({re.escape(diff_arg)})\)", r"diff(\2, \1)", eq_string)
    
    if not index_nth_derivative:
        return eq_string
    
    diff_args = []
    for index in index_nth_derivative:
        diff_arg, _ =  get_arg_in_brackets(eq_string, index)
        diff_args.append(diff_arg)

    for diff_arg in diff_args:
        eq_string = re.sub(rf"d\^\((\d+)\)/d(" + r"\p{L}" + rf")\^\(\1\)\s*\(({re.escape(diff_arg)})\)", r"diff(\3, \2, \1)", eq_string)
        

    return eq_string

def interpret_log(eq_string):
    eq_string = re.sub(r"log_(\d+|[\w\p{Greek}])", r"log_(\1)", eq_string)

    index_log = [m.end() for m in re.finditer(r"log_", eq_string)]

    if not index_log:
        return eq_string
    
    log_bases = []
    indices_start_args = []
    log_args = []
    for index in index_log:
        log_base, index =  get_arg_in_brackets(eq_string, index)
        log_bases.append(log_base)
        indices_start_args.append(index + 2)

    for log_base in log_bases:
        eq_string = re.sub(rf"log_\(({re.escape(log_base)})\)\s*" + r"(\d+|[\w\p{Greek}])", r"log_(\1) (\2)", eq_string)
        eq_string = re.sub(rf"log_\(({re.escape(log_base)})\)\s*\(", r"log_(\1) (", eq_string)

    for index in indices_start_args:
        log_arg, index =  get_arg_in_brackets(eq_string, index)
        log_args.append(log_arg)

    for log_base, log_arg in zip(log_bases, log_args):
        eq_string = re.sub(rf"log_\(({re.escape(log_base)})\)\s*\(({re.escape(log_arg)})\)", r"log(\2, \1)", eq_string)

    return eq_string


def latex_to_plain_text(latex_str):
    diff_formatting = [
        (r"d/d(\p{L})\s*(?!\()([\w\p{Greek}()]+)", r"d/d\1(\2)"),
        (r"d/d(\p{L})\s*\(?", r"d/d\1("),
        (r"d\^[({]*(\d+)[)}]*/d(\p{L})\^[({]*\1[)}]*\s*(?!\()([\w\p{Greek}()]+)", r"d^(\1)/d\2^(\1)(\3)"),
        (r"d\^[({]*(\d+)[)}]*/d(\p{L})\^[({]*\1[)}]*\s*\(?", r"d^(\1)/d\2^(\1)("),
        (r"\\[cd]?frac\{\s*d\s*\}\{d\s*(\p{L})\s*\}\s*(?!\()([\w\p{Greek}()]+)", r"d/d\1(\2)"),
        (r"\\[cd]?frac\{\s*d\s*\}\{d\s*(\p{L})\s*\}\s*\(?", r"d/d\1("),
        (r"\\[cd]?frac\{\s*d\^[({]*(\d+)[)}]*\s*\}\{d\s*(\p{L})\^[({]*\1[)}]*\s*\}\s*(?!\()([\w\p{Greek}()]+)", r"d^(\1)/d\2^(\1)(\3)"),
        (r"\\[cd]?frac\{\s*d\^[({]*(\d+)[)}]*\s*\}\{d\s*(\p{L})\^[({]*\1[)}]*\s*\}\s*\(?", r"d^(\1)/d\2^(\1)("),
    ]    
    general_formatting = [
        (r"\{", "{("),
        (r"\}", ")}"),
        (r"%", r"\%"),  # Escape percent signs
        (r"\\[cd]?frac", r"\\frac"),
    ]

    replacements_before = diff_formatting + general_formatting

    for pattern, repl in replacements_before:
        latex_str = re.sub(pattern, repl, latex_str)

    latex_str = interpret_latex_root(latex_str)
    latex_str = LatexNodes2Text().latex_to_text(latex_str)

    replacements_symbols = [
        ("≠", "!="), 
        ("≥", ">="), 
        ("≤", "<="), 
        ("≈", "="), 
        ("≡", "="), 
        ("·", "* "),  
        ("×", "* "),
        (r"−", r"-"), 
        ("÷", "/ "),
        (":", "/ "),
    ]

    for pattern, repl in replacements_symbols:
        latex_str = re.sub(pattern, repl, latex_str)

    latex_str =fix_mismatched_parenthesis(latex_str)

    latex_str = interpret_derivative(latex_str)
    latex_str = interpret_integral(latex_str)
    latex_str = interpret_log(latex_str)

    return latex_str


def split_equation(eq_string):
    equation_symbols = ["!=", ">=", "<=", "==", "=", ">", "<"]

    relevant_eq_symbols = []
    for i in range(1, len(eq_string) - 1):
        char_prev = eq_string[i-1]
        char = eq_string[i]
        char_next =  eq_string[i+1]
        if char_prev + char in equation_symbols and char_prev + char not in relevant_eq_symbols:
            relevant_eq_symbols.append(eq_string[i-1] + eq_string[i])
        elif char + char_next in equation_symbols and char + char_next not in relevant_eq_symbols:
            relevant_eq_symbols.append(eq_string[i] + eq_string[i+1])
        elif char in equation_symbols and char not in relevant_eq_symbols:
            relevant_eq_symbols.append(eq_string[i])

    
    relevant_eq_symbols.sort(key=len, reverse=True)

    symbols_string = '|'.join(relevant_eq_symbols)
    if symbols_string:
        return re.split(rf"({symbols_string})", eq_string)
    else:
        return [eq_string]
    

def add_args_to_func(eq_string: str, func_name: str='log', replace_with: str='10', amt_commas: int=1, nested_level: int=1, position_type: str='after', extra_arguments: int=0) -> str:
    """
    Adds arguments to a specified function within a mathematical expression.

    Args:
        eq_string (str): The equation string where the function arguments need to be added.
        func_name (str): The function name to target for argument addition. Default is 'log'.
        replace_with (str): The argument to insert. Default is '10'.
        amt_commas (int): Number of commas to navigate before inserting the argument. Default is 1.
        nested_level (int): The level of nesting to consider for adding the argument. Default is 1.
        position_type (str): Position to insert the argument, either 'before' or 'after' the current function arguments. Default is 'after'.

    Returns:
        str: The modified equation string with the added arguments.
    """


    def check_object_is_type(object_type="number") -> bool:
        """
        Checks if the substring following the current position in the equation is a numeric object.

        Returns:
            bool: True if the substring is a number, False otherwise.
        """
        def is_type(sp_object, object_type):
            if object_type == "number":
                return sp_object.is_number
            elif object_type == "symbol":
                return sp_object.is_Symbol
            
            return False

        index_comma = get_index_in_substring()
        relevant_index = index_comma + 1
        relevant_string = string[relevant_index:]
        relevant_nested = nested
        for char in relevant_string:
            if char == '(':
                relevant_nested += 1
            elif char == ')':
                relevant_nested -= 1
                if relevant_nested < nested:
                    break
            elif char == ',' and relevant_nested == nested:
                break
        
            relevant_index += 1

        relevant_string = ''.join(string[index_comma+1:relevant_index])

        try:
            return is_type(sp.sympify(relevant_string), object_type)
        except Exception:
            return False
        
    def count_commas() -> int:
        """
        Counts the number of commas in the substring following the current position in the equation.

        Returns:
            int: The count of commas in the relevant part of the string.
        """

        index_bracket = get_index_in_substring()
        relevant_index = index_bracket + 1
        relevant_string = string[relevant_index:]
        relevant_nested = nested
        comma_counter = 0
        for char in relevant_string:
            if char == '(':
                relevant_nested += 1
            elif char == ')':
                relevant_nested -= 1
                if relevant_nested < nested:
                    break
            elif char == ',' and relevant_nested == nested:
                comma_counter += 1
        
        return comma_counter


    func_amt_commas = {'diff': 2, 'subs': 2, "limit": 3, 'integrate': 3, "Sum": 3, "Product": 3} # max amount of commas each function has for proper syntax
    index_func = [m.start() for m in re.finditer(func_name, eq_string)] # get index list of start of each function name
    
    if len(index_func) == 0:
        return eq_string
    
    index_dot_func = [m.start() for m in re.finditer(r'\.' + func_name, eq_string)]
    is_dot_func = []
    func_amt_commas_start = func_amt_commas.copy()

    for func_index in index_func:
        is_dot_func.append(func_index - 1 in index_dot_func)
    
    eq_string_list = list(eq_string)
    string_split = [eq_string_list[index_func[i]:index_func[i+1]] if i != len(index_func) - 1 else eq_string_list[index_func[i]:] for i in range(len(index_func)) ]
    index_list_secure = []
    nested = 0
    char_index = 0
    add_args = 0 # add the arguments if add_args > 0

    amt_commas_start = amt_commas
    num_comma = amt_commas
    substring_index = -1

    get_index_in_substring = lambda: char_index - sum([len(string_) for string_ in string_split[:substring_index]])
    no_replace = lambda: (nested == 0 and nested_before == 0 and has_been_nested)

    for string in string_split:
        substring_index += 1

        add_args += 1
        if add_args < 1:
            add_args = 1

        index_list = []
        amt_commas = amt_commas_start
        func_amt_commas = func_amt_commas_start.copy()
        nested_before = nested
        nested = 0
        replace_with_pretty = f', {replace_with}'
        char_index_before = None
        check_is_number = False
        comma_amt = 0
        has_been_nested = False
        add_close_bracket = False

        if func_name in func_amt_commas.keys():
            if is_dot_func[substring_index]:
                amt_commas -= 1
                func_amt_commas[func_name] -= 1
            num_comma = func_amt_commas[func_name]

        for char in string:
            if no_replace():
                char_index += 1
                continue
                
            if is_dot_func[substring_index]:
                char_index_before = char_index

            if position_type == 'before':
                if char == '(':
                    has_been_nested = True
                    nested += 1
                    if amt_commas == 0 and add_args > 0:

                        if char_index_before is None:
                            char_index_before = char_index
                        elif nested == nested_level:
                            comma_amt = count_commas()
                            check_is_number = check_object_is_type(object_type="number")
                            char_index_before = None
                            if check_is_number and comma_amt <= num_comma - 1:
                                replace_with_pretty = f'{replace_with}, '
                                index_list.append((char_index + 1, replace_with_pretty))
                                add_args -= 1

                        elif nested_level == 2 and nested == 1:
                            comma_amt = count_commas()
                            check_is_number = check_object_is_type(object_type="number")
                            check_is_symbol = check_object_is_type(object_type="symbol")
                            if comma_amt > 0 and (check_is_number or check_is_symbol):
                                open_bracket_index = index_func[0] + char_index + 1
                                open_bracket_index_substring = get_index_in_substring() + 1
                                string.insert(open_bracket_index_substring, "(")
                                eq_string = eq_string[:open_bracket_index] + "(" + eq_string[open_bracket_index:]
                                add_close_bracket = True
                    
                elif char == ')':
                    nested -= 1
                    if nested == 0 and add_args > 0 and char_index_before is not None and check_is_number and comma_amt < num_comma - 1:
                        if nested_before == 0 and amt_commas == 0:
                            replace_with_pretty = f', {replace_with}'
                            if char_index_before not in index_list:
                                index_list.append((char_index_before, replace_with_pretty))
                            else:
                                index_list.append((char_index + 1, replace_with_pretty))

                            add_args -= 1

                    if nested == 0:
                        amt_commas = amt_commas_start
                        nested = nested_before
                        # nested_before = 0

                    elif add_close_bracket and nested == 1:
                        close_bracket_index = index_func[0] + char_index + 1
                        close_bracket_index_substring = get_index_in_substring() + 1
                        string.insert(close_bracket_index_substring, ")")
                        eq_string = eq_string[:close_bracket_index] + ")" + eq_string[close_bracket_index:]
                        add_close_bracket = False


                elif char == ',' and nested == 1:
                    amt_commas -= 1

                    if amt_commas == 0 and add_args > 0:
                        char_index_before = char_index
                        if nested_level == 1:
                            replace_with_pretty = f', {replace_with}'
                            comma_amt = count_commas()
                            check_is_number = check_object_is_type(object_type="number")
                            
                            if check_is_number and comma_amt < num_comma - 1: 
                                index_list.append((char_index_before, replace_with_pretty))
                                add_args -= 1
                                check_is_number = False

                        elif nested_level == 2:
                            comma_amt = count_commas()
                            check_is_number = check_object_is_type(object_type="number")
                            check_is_symbol = check_object_is_type(object_type="symbol")
                            if comma_amt > 0 and (check_is_number or check_is_symbol):
                                open_bracket_index = index_func[0] + char_index + 2 if eq_string[index_func[0] + char_index + 1] == ' ' else index_func[0] + char_index + 1
                                open_bracket_index_substring = get_index_in_substring() + (open_bracket_index - char_index)
                                string.insert(open_bracket_index_substring, "(")
                                eq_string = eq_string[:open_bracket_index] + "(" + eq_string[open_bracket_index:]
                                add_close_bracket = True

                if amt_commas + extra_arguments < 0 and len(index_list) != 0 and nested_before == 0:
                    index_list.pop()
                    amt_commas += 1


            elif position_type == 'after':
                if char == '(':
                    if nested == 0:
                        index_open_bracket = get_index_in_substring()
                    nested += 1
                elif char == ')':
                    nested -= 1

                elif char == ',' and nested == 1:
                    if amt_commas == 1:
                        add_args -= 1
                    else:
                        amt_commas -= 1

                if char == ')' and nested == 0:
                    index_close_bracket = get_index_in_substring()

                    if np.array([(char in "()") for char in string[index_open_bracket:index_close_bracket + 1]]).all():
                        replace_with_pretty = replace_with

                    if add_args > 0:
                        index_list.append((char_index, replace_with_pretty))
                    
                    add_args -= 1
                    amt_commas = amt_commas_start
                    nested = nested_before

            # print(char, char_index, nested, nested_before, amt_commas, index_list)

            char_index += 1

        index_list_secure.extend(index_list)

    additional_index = index_func[0]
    for char_index, replace_with_pretty in index_list_secure:
        char_index += additional_index 
        eq_string = eq_string[:char_index] + replace_with_pretty + eq_string[char_index:]
        additional_index += len(replace_with_pretty)
    
    return eq_string



def math_interpreter(eq_string: str) -> str:
    """
    Interprets and reformats a mathematical equation string to be compatible with SymPy.
    This function performs a series of regex-based transformations to ensure proper formatting
    for functions, constants, and mathematical operations.
    
    Args:
        eq_string (str): The input mathematical equation string.
    
    Returns:
        str: The reformatted equation string.
    """

    def insert_asterisks(match: re.Match) -> str:
        """
        Inserts asterisks between repeated characters unless they belong to a recognized function or constant.
        
        Args:
            match (re.Match): The regex match object containing the repeated characters.
        
        Returns:
            str: The original string if the characters are part of a function/constant name, 
                otherwise the string with asterisks inserted between the characters.
        """
        char = match.group(1)
        count = len(match.group(0))
        pos = match.start()

        # Check if repeated letters are part of any relevant function name
        for func in relevant_functions:
            if eq_string[pos:pos+len(func)] == func:
                return match.group(0)

        # Check if repeated letters are part of any constant name
        for const in relevant_constants:
            if eq_string[pos:pos+len(const)] == const:
                return match.group(0)
            
        for func in relevant_functions:
            index_range = len(func) - 1
            index_start = max(0, pos - index_range)
            index_end = min(len(eq_string), match.end() + index_range)
            if func in eq_string[index_start:index_end]:
                return match.group(0)


        return '*'.join(char for _ in range(count))

    def replace_constant_symbols(eq_string: str) -> str:
        """
        Replaces common mathematical constants and superscripts with their SymPy equivalents.
        
        Args:
            eq_string (str): The input mathematical equation string.
        
        Returns:
            str: The equation string with constants and superscripts replaced.
        """

        def replace_superscript(match: re.Match) -> str:
            """
            Converts superscript characters to their corresponding digits or letters.
            
            Args:
                match (Match): The regex match object containing superscript characters.
            
            Returns:
                str: The equivalent string with superscripts replaced.
            """            
            matched_super = match.group(1)
            letter_list = [superscript_to_letter[superscript] for superscript in matched_super]
            letters_string = ''.join(letter_list)

            replace = "^" + f"({letters_string})"
            return replace


        eq_string = re.sub(r'\b' + r'inf' + r'\b', r'oo', eq_string)
        eq_string = re.sub(r'\b' + r'infty' + r'\b', r'oo', eq_string)
        eq_string = re.sub(r'\b' + r'infinity' + r'\b', r'oo', eq_string)
        eq_string = re.sub(r'∞', r'oo', eq_string)
        eq_string = re.sub(r'π', r'pi', eq_string)

        string_superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᑫʳˢᵗᵘᵛʷˣʸᶻ"
        string_corresp_letters = "0123456789abcdefghijklmnopqrstuvwxyz"
        superscript_to_letter = dict(zip(string_superscripts, string_corresp_letters))
        
        eq_string = re.sub(f'([{string_superscripts}]+)', replace_superscript, eq_string)
        return eq_string
    
    def is_part_of_funcs_or_consts(match: re.Match, check_obj_list: list, obj_match_pos: int, extra_index: int=0) -> bool:
        """
        Determines whether the match object is part of a recognized function or constant.

        Args:
            match (re.Match): The regex match object to check.
            check_obj_list (list): The list of functions or constants to check against.
            obj_match_pos (int): The position of the matched object within the regex groups.
            extra_index (int, optional): Offset index to account for changes in the string length during replacements. 
                                        Defaults to 0.

        Returns:
            bool: True if the match is part of a recognized function or constant, False otherwise.
        """

        str_first_part = match.group(1)
        str_second_part = match.group(2)

        matched_obj = match.group(obj_match_pos)

        # quick check
        if str_first_part + str_second_part in check_obj_list:
            return True
        
        # thourough check
        for obj in check_obj_list:
            if obj == matched_obj:
                continue

            length_obj = len(obj)
            length_matched_obj = len(matched_obj)
            index_range = length_obj - length_matched_obj

            if index_range <= 0:
                continue

            index_start_match = match.start(1) + extra_index
            index_end_match = match.end(1) + extra_index
            index_start = max(0, index_start_match - index_range)
            index_end = min(len(eq_string), index_end_match + index_range)

            if obj in eq_string[index_start:index_end]:
                if matched_obj in obj and matched_obj != obj:
                    return True
                
        return False
    

    def add_parenthesis(match: re.Match, extra_index: int=0) -> str:
        """
        Adds parentheses around function arguments in the equation string if missing.
        
        Args:
            match (re.Match): The regex match object for a function name and its subsequent symbol.
            extra_index (int, optional): Offset index to account for changes in the string length during replacements.
                                         Defaults to 0.
        
        Returns:
            str: The original string if parentheses are correctly placed, otherwise with added parentheses.
        """

        is_part_of_funcs = is_part_of_funcs_or_consts(match, relevant_functions, obj_match_pos=1, extra_index=extra_index)
        if is_part_of_funcs:
            return match.group(0)
        
        return f'{match.group(1)}({match.group(2)})'


    def mult_constants(match: re.Match) -> str:
        """
        Adds multiplication between constants and variables if missing in the equation string.
        
        Args:
            match (re.Match): The regex match object for a constant and the subsequent symbol.
        
        Returns:
            str: The original string if correctly formatted, otherwise with added multiplication signs.
        """

        is_part_of_funcs = is_part_of_funcs_or_consts(match, relevant_functions, obj_match_pos=1)
        if is_part_of_funcs:
            return match.group(0)

        is_part_of_consts = is_part_of_funcs_or_consts(match, relevant_constants, obj_match_pos=2)
        if is_part_of_consts:
            return match.group(0)

        return f'{match.group(1)}*{match.group(2)}'

    
    eq_string = latex_to_plain_text(eq_string).casefold()
    eq_string = fix_mismatched_parenthesis(eq_string)


    # Replace common functions and symbols
    replacements = [
        (r"\|([^|]+)\|", r"Abs(\1)"), # ||x|| -> Abs(x)
        (r'abs', r'Abs'), # abs(x) -> Abs(x)
        (r'mod', r'Mod'), # mod(x, y) -> Mod(x, y)
        (r'sum', r'Sum'), # sum(x, (x, 1, 4)) -> Sum(x, (x, 1, 4))
        (r'∑', r'Sum'), # ∑(x, (x, 1, 4)) -> Sum(x, (x, 1, 4))
        (r'product', r'Product'), # product(x, (x, 1, 4)) -> Product(x, (x, 1, 4))
        (r'∏', r'Product'), # ∏(x, (x, 1, 4)) -> Product(x, (x, 1, 4))
        (r'lambertw', r'LambertW'), # lambertw(x) -> LambertW(x)
        (r'√', r'sqrt'), # √(x) -> sqrt(x)
        (r'∛', r'cbrt'), # ∛(x) -> cbrt(x)
        (r'\bi\b', r'I'), # i -> I
        (r'\be\b', r'E'), # e -> E
        (r"%(?!\d)", r'*0.01'), # 10% -> 10*0.01
        (r'(\d+/\d+)\s+(\d+/\d+)', r'\1*\2'), # 1/2 3/4 -> 1/2*3/4
        (r'(\d+)\s+(\d+/\d+)(?!(?:\.))', r'(\1+\2)'), # 1 2/3 -> (1+2/3)
        (r"\s+\.", "."), #  . -> .
        (r"\b(\d+)\.(\p{L})", r"(\1).\2"), # 2.diff() -> (2).diff()
    ]

    for pattern, repl in replacements:
        eq_string = re.sub(pattern, repl, eq_string)

    function_names = [name for name in dir(sp.functions) if not name.startswith('_')]
    function_names.extend(("diff", "integrate", "limit", "Mod", "subs", "Sum", "Product"))
    function_names.remove("ff")
    relevant_functions = [func for func in function_names if func in eq_string]

    eq_string = replace_constant_symbols(eq_string)

    constant_names_og = [name for name, obj in sp.__dict__.items() if isinstance(obj, (sp.Basic, sp.core.singleton.Singleton)) and not name.startswith('_') and sp.sympify(name).is_number]
    constant_names = [name.casefold() for name in constant_names_og]
    relevant_constants = [constant for constant in constant_names if constant in eq_string]

    arc_functions = ["arcsin", "arccos", "arctan", "arccot", "arcsec", "arccsc"]
    relevant_arc_functions = [arc_func for arc_func in arc_functions if arc_func in eq_string]
    if relevant_arc_functions:
        for arc_func in relevant_arc_functions:
            a_func = arc_func[0] + arc_func[3:]
            eq_string = re.sub(arc_func, a_func, eq_string)
            relevant_functions.insert(0, a_func)

    added_x = False
    if relevant_functions:
        rel_func_pattern = '|'.join(map(re.escape, relevant_functions))
        eq_string = re.sub(rf'({rel_func_pattern})' + r'(?:\s)+([\w\p{Greek}]+)', r'\1(\2)', eq_string) # sin x -> sin(x)

        add_x_pattern = rf'({rel_func_pattern})' + r'(?![\w\p{Greek}]+|\()' # sin -> sin(x)
        if re.findall(add_x_pattern, eq_string): 
            added_x = True
            eq_string = re.sub(add_x_pattern, r'\1(x)', eq_string)


    eq_string = re.sub(r'(?<=[\w\p{Greek})])\s+(?=[\w\p{Greek}(])', '*', eq_string)

    sub_patterns = [
        (r'(?<!\.)\b0(\d)', r'\1'), # remove leading 0
        (r'(\d)(\p{L})', r'\1*\2'), # 2x -> 2*x
        (r'\b(\p{L})(\d)', r'\1^\2'), # x2 -> x^2
        (r'\)([\w\p{Greek}])', r')*\1'), # )x -> )*x or )2 -> )*2
        (r'([\w\p{Greek}])\(', r'\1*('), # x( -> x*( or 2( -> 2*(
        (r'\)\(', r')*('), # )( -> )*(
        (r'(\p{L})\1+', insert_asterisks), # xx -> x*x
        (r'\b([e])\b', r'E'), # e -> E
        (r'\b([i])\b', r'I'), # i -> I
    ]
    
    def nest_functions(eq_string: str) -> str:
        """
        Adjusts nested functions in the equation string by ensuring proper parentheses around the arguments of nested functions.

        This function specifically handles cases where two functions might appear adjacently in the equation string
        without proper nesting (e.g., `func1func2(...)`). It ensures that the inner function is correctly nested
        as an argument to the outer function.

        Args:
            eq_string (str): The equation string to be processed.

        Returns:
            str: The modified equation string with properly nested functions.
        """
        for func2 in relevant_functions:
            eq_string = re.sub(rf"{func1}{func2}\((.*?)\)", rf"{func1}({func2}(\1))", eq_string)
            eq_string = re.sub(rf"{func2}{func1}\((.*?)\)", rf"{func2}({func1}(\1))", eq_string)

        return eq_string

    for _ in range(100):
        eq_string_before = eq_string
        for pattern, repl in sub_patterns:
            eq_string = re.sub(pattern, repl, eq_string)
        
        for func1 in relevant_functions:
            eq_string = nest_functions(eq_string)

            # Handle cases where function names overlap like sin and sinh
            matches = re.finditer(rf'({func1})' + rf'(?!(?:{rel_func_pattern}))' +  r'([\w\p{Greek}(]+)', eq_string, overlapped=True)
            old_eq_string = eq_string
            for match in matches:
                extra_index = len(eq_string) - len(old_eq_string)
                eq_string = re.sub(re.escape(match.group()), add_parenthesis(match, extra_index), eq_string, count=1)
            
            # Insert multiplication between a function and preceding variable
            eq_string = re.sub(r'\b' + rf'(?!(?:{rel_func_pattern}))' + r'([\w\p{Greek}]+)' + rf'({func1})', r'\1*\2', eq_string)

            # Ensure no multiplication sign between function and its arguments
            eq_string = re.sub(rf'({func1})\*\(', r'\1(', eq_string)

            eq_string = nest_functions(eq_string)

        if eq_string == eq_string_before:
            break
    
    for constant in relevant_constants:
        constant_patterns = [r'([\w\p{Greek}]+)' + f"({constant})", f"({constant})" + r'([\w\p{Greek}]+)']
        for pattern in constant_patterns:
            if relevant_functions:
                pattern = rf'(?!(?:{rel_func_pattern}))' + pattern
                
            eq_string = re.sub(pattern, mult_constants, eq_string)
    
    eq_string_start = eq_string

    # arguments: function_name, replace_with, amt_commas, nested_level, position_type, extra_arguments
    function_adjustments = [
        ("diff", 'x', 1, 1, "before"),
        ("subs", 'x', 1, 1, "before"),
        ("limit", 'x', 1, 1, "before", 1),
        ("integrate", 'x', 1, 2, "before"),
        ("Sum", 'x', 1, 2, "before"),
        ("Product", 'x', 1, 2, "before"),
        ('log', '10', 1, 1, "after"),
        ('root', '3', 1, 1, "after"),
    ]

    for args in function_adjustments:
        eq_string = add_args_to_func(eq_string, *args)

    eq_string = re.sub(r'(?<!\.)subs', r'Subs', eq_string)

    for i, constant in enumerate(relevant_constants):
        if re.search(r'\b' + constant + r'\b', eq_string) and constant not in constant_names_og:
            eq_string = re.sub(r'\b' + constant + r'\b', constant_names_og[i], eq_string)
    
    # change the added symbol from x if there is another symbol in the equation
    try:
        symbol_list = list(sp.sympify(eq_string.replace("=", "+").replace("diff", "Derivative").replace("integrate", "Integral"), evaluate=False).free_symbols)
        if symbol_list and (not re.findall(r"\bx\b", eq_string_start) or added_x):
            symbol = symbol_list.pop()
            if str(symbol) == 'x' and symbol_list:
                symbol = symbol_list.pop()

            if str(symbol) != 'x' and str(symbol) != 'y':
                eq_string = re.sub(r"\bx\b", str(symbol), eq_string)

    except Exception:
        pass

    return eq_string



def get_uneval_sp_objs(string: str, func_dict: Dict[str, str] = {"subs": "Subs", "diff": "Derivative", "integrate": "Integral", "limit": "Limit"}) -> Union[str, sp.Basic]:
    """
    Replaces dot notation functions (e.g., `.subs`, `.diff`) in a string with their corresponding unevaluated SymPy function equivalents.

    This function processes a given string to replace instances of functions in dot notation with their corresponding
    SymPy equivalents (x.subs() -> Subs(x), x.diff() -> Derivative(x), etc). It handles cases with varying arguments and ensures proper formatting.

    Args:
        string (str): The input string containing functions in dot notation.
        func_dict (Dict[str, str]): A dictionary mapping dot notation function names to their corresponding SymPy functions.

    Returns:
        Union[str, sp.Basic]: The SymPy expression object if successful, otherwise the original string.
    """


    def replace_function(match: re.Match) -> str:
        """
        Replaces a matched dot notation function call with its corresponding SymPy function.

        Args:
            match (re.Match): The regex match object containing the matched function.

        Returns:
            str: The formatted SymPy function string.
        """
        nonlocal extra_index_next
        expr = match.group(1)
        args_str = match.group(2)
        args = args_str.split(',')

        # Handle different cases for arguments
        if len(args) == 1 and not args[0]:
            func_expr = f"{replace_func}({expr})"
            extra_index_next -= 3

        elif len(args) != 2:
            func_expr = f"{replace_func}({expr}, {args_str})"
            extra_index_next -= 1

        else:
            args_var, args_val = args
            func_expr = f"{replace_func}({expr}, {args_var}, {args_val})"

        extra_index_next += len(replace_func) - len(func)
        return func_expr
    
    def remove_whitespace(match: re.Match) -> str:
        """
        Removes all whitespace from the matched function call.

        Args:
            match (re.Match): The regex match object containing the matched function call.

        Returns:
            str: The function call with whitespace removed.
        """
        return re.sub(r'\s+', '', match.group(0))

    alphabet_plus = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.^"
    string_og_list = [string]

    # we want the change to start at the location of the previous letter (counting backwards), but if index == 0 there is no next letter 
    get_index_range = lambda condition=True: (index + 1, index_func) if not condition or index != 0 else (0, index_func)

    for func, replace_func in func_dict.items():
        # Remove whitespace within dot notation functions
        string = re.sub(rf"\.{func}\(([^()]+)\)", remove_whitespace, string) 

        # immediately replace the functions if they aren't dot functions
        string = re.sub(rf'(?<!\.){func}', replace_func, string)

        # Find positions of dot functions
        index_dot_funcs = [m.start() for m in re.finditer(r'\.' + func, string)]
        string_og_list.append(string)

        if not index_dot_funcs:
            string = string.replace(func, replace_func)
            continue

        extra_index_next = 0
        for index_func in index_dot_funcs:
            index_func += extra_index_next
            relevant_string = string[:index_func]
            nested = 0

            for index in range(index_func - 1, -1, -1):
                char = relevant_string[index]
                if char == ')':
                    nested += 1

                elif char == '(':
                    nested -=1
                    if nested == 0:
                        if index == 0:
                            index_range = get_index_range(condition=True)
                            break

                    elif nested < 0:
                        index_range = get_index_range(condition=False)
                        break
                
                elif nested == 0:
                    if (char not in alphabet_plus) ^ (index == 0):
                        index_range = get_index_range(condition=True)
                        break
                    elif char not in alphabet_plus or index == 0:
                        index_range = get_index_range(condition=False)
                        break

            extra_index_next += 2
            changed_string = re.escape(string[index_range[0]:index_range[1]])

            # Replace dot function with corresponding SymPy function
            result_string = string
            pattern = f"({changed_string})" + rf"\.{func}\(([^()]*)\)"
            result_string = re.sub(pattern, replace_function, result_string)

            # Handle nested parentheses
            if result_string == string:
                nested_pattern = f"({changed_string})" + rf"\.{func}\((\([^()]*\))\)"
                result_string = re.sub(nested_pattern, replace_function, result_string)

            string = result_string

    string_og_list.append(string)

    # Attempt to sympify the resulting string for all changes made, if none work
    for result_string in reversed(string_og_list):
        try:
            sympy_expr = sp.sympify(result_string)
            return sympy_expr
        
        except sp.SympifyError:
            continue

    # return initial string if sympify fails for all attempts
    return string_og_list[0]