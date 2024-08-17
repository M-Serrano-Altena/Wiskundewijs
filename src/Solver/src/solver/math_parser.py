import numpy as np
import sympy as sp
import regex as re
from pylatexenc.latex2text import LatexNodes2Text


def latex_to_plain_text(latex_str):
    latex_str = re.sub(r"%", r"\%", latex_str)
    return LatexNodes2Text().latex_to_text(latex_str).replace("·", "*")

def add_args_to_func(eq_string: str, func_name: str='log', replace_with: str='10', amt_commas: int=1, nested_level: int=1, position_type: str='after') -> str:
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


    def check_object_number() -> bool:
        """
        Checks if the substring following the current position in the equation is a numeric object.

        Returns:
            bool: True if the substring is a number, False otherwise.
        """

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
            elif char == ',':
                break
        
            relevant_index += 1

        relevant_string = ''.join(string[index_comma+1:relevant_index])

        try:
            return sp.sympify(relevant_string).is_number
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
            elif char == ',':
                comma_counter += 1
        
        return comma_counter

    func_amt_commas = {'diff': 2, 'subs': 2, 'integrate': 3} # max amount of commas each function has for proper syntax
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
                            char_index_before = None
                            check_is_number = check_object_number()
                            comma_amt = count_commas()
                            if check_is_number and comma_amt <= num_comma - 1:
                                replace_with_pretty = f'{replace_with}, '
                                index_list.append((char_index + 1, replace_with_pretty))
                                add_args -= 1

                    
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


                elif char == ',' and nested == 1:
                    amt_commas -= 1

                    if amt_commas == 0 and add_args > 0:
                        char_index_before = char_index

                        if nested_level == 1:
                            replace_with_pretty = f', {replace_with}'
                            check_is_number = check_object_number()
                            comma_amt = count_commas()
                            if check_is_number and comma_amt < num_comma - 1: 
                                index_list.append((char_index_before, replace_with_pretty))
                                add_args -= 1
                                check_is_number = False

                if amt_commas < 0 and len(index_list) != 0 and nested_before == 0:
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

            char_index += 1

        index_list_secure.extend(index_list)

    additional_index = index_func[0]
    for char_index, replace_with_pretty in index_list_secure:
        eq_string = eq_string[:char_index + additional_index] + replace_with_pretty + eq_string[char_index + additional_index:]
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
        for const in constant_names:
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

        is_part_of_consts = is_part_of_funcs_or_consts(match, constant_names, obj_match_pos=2)
        if is_part_of_consts:
            return match.group(0)

        return f'{match.group(1)}*{match.group(2)}'

    
    eq_string = latex_to_plain_text(eq_string).casefold()
    function_names = [name for name in dir(sp.functions) if not name.startswith('_')]
    function_names.extend(("diff", "integrate", "limit", "Mod", "subs"))
    function_names.remove("ff")
    relevant_functions = [func for func in function_names if func in eq_string]


    constant_names_og = [name for name, obj in sp.__dict__.items() if isinstance(obj, (sp.Basic, sp.core.singleton.Singleton)) and not name.startswith('_') and sp.sympify(name).is_number]
    constant_names_og.extend(("inf", "infty", "infinity"))
    constant_names = [name.casefold() for name in constant_names_og]

    eq_string = replace_constant_symbols(eq_string)

    # Replace common functions and symbols
    replacements = [
        (r"\|([^|]+)\|", r"Abs(\1)"), # ||x|| -> Abs(x)
        (r'abs', r'Abs'), # abs(x) -> Abs(x)
        (r'mod', r'Mod'), # mod(x, y) -> Mod(x, y)
        (r'lambertw', r'LambertW'), # lambertw(x) -> LambertW(x)
        (r'\bi\b', r'I'), # i -> I
        (r'\be\b', r'E'), # e -> E
        (r"%(?!\d)", r'*0.01'), # 10% -> 10*0.01
        (r'(\d+/\d+)\s+(\d+/\d+)', r'\1*\2'), # 1/2 3/4 -> 1/2*3/4
        (r'(\d+)\s+(\d+/\d+)(?!(?:\.))', r'(\1+\2)'), # 1 2/3 -> (1+2/3)
        (r"\s+\.", "."), #  . -> .
        (r"\b(\d+)\.([a-zA-Z])", r"(\1).\2"), # 2.diff() -> (2).diff()
    ]

    for pattern, repl in replacements:
        eq_string = re.sub(pattern, repl, eq_string)

    arc_functions = ["arcsin", "arccos", "arctan", "arccot", "arcsec", "arccsc"]
    relevant_arc_functions = [arc_func for arc_func in arc_functions if arc_func in eq_string]
    if relevant_arc_functions:
        for arc_func in relevant_arc_functions:
            a_func = arc_func[0] + arc_func[3:]
            eq_string = re.sub(arc_func, a_func, eq_string)
            relevant_functions.insert(0, a_func)

    # check the capitalized version of the functions
    relevant_functions.extend([func for func in ["Abs", "Mod", "LambertW"] if func in eq_string])

    added_x = False
    if relevant_functions:
        rel_func_pattern = '|'.join(map(re.escape, relevant_functions))
        eq_string = re.sub(rf'({rel_func_pattern})' + r'(?:\s)+([\w]+)', r'\1(\2)', eq_string) # sin x -> sin(x)

        add_x_pattern = rf'({rel_func_pattern})' + r'(?!\w+|\()' # sin -> sin(x)
        if re.findall(add_x_pattern, eq_string): 
            added_x = True
            eq_string = re.sub(add_x_pattern, r'\1(x)', eq_string)


    eq_string = re.sub(r'(?<=[\w)])\s+(?=[\w(])', '*', eq_string)

    sub_patterns = [
        (r'(?<!\.)\b0(\d)', r'\1'), # remove leading 0
        (r'(\d)([a-zA-Z])', r'\1*\2'), # 2x -> 2*x
        (r'\b([a-zA-Z])(\d)', r'\1^\2'), # x2 -> x^2
        (r'\)(\w)', r')*\1'), # )x -> )*x or )2 -> )*2
        (r'(\w)\(', r'\1*('), # x( -> x*( or 2( -> 2*(
        (r'\)\(', r')*('), # )( -> )*(
        (r'([a-zA-Z])\1+', insert_asterisks), # xx -> x*x
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

    for _ in range(5):
        for pattern, repl in sub_patterns:
            eq_string = re.sub(pattern, repl, eq_string)
        
        for func1 in relevant_functions:
            eq_string = nest_functions(eq_string)

            # Handle cases where function names overlap like sin and sinh
            matches = re.finditer(rf'({func1})' + rf'(?!(?:{rel_func_pattern}))' +  r'([\w(]+)', eq_string, overlapped=True)
            old_eq_string = eq_string
            for match in matches:
                extra_index = len(eq_string) - len(old_eq_string)
                eq_string = re.sub(re.escape(match.group()), add_parenthesis(match, extra_index), eq_string, count=1)
            
            # Insert multiplication between a function and preceding variable
            eq_string = re.sub(r'\b' + rf'(?!(?:{rel_func_pattern}))' + rf'([\w]+)({func1})', r'\1*\2', eq_string)

            # Ensure no multiplication sign between function and its arguments
            eq_string = re.sub(rf'({func1})\*\(', r'\1(', eq_string)

            eq_string = nest_functions(eq_string)
    
    for constant in constant_names:
        constant_patterns = [r'([\w]+)' + f"({constant})", f"({constant})" + r'([\w]+)']
        for pattern in constant_patterns:
            if relevant_functions:
                pattern = rf'(?!(?:{rel_func_pattern}))' + pattern
                
            eq_string = re.sub(pattern, mult_constants, eq_string)
    
    eq_string_start = eq_string

    # arguments: function_name, replace_with, amt_commas, nested_level, position_type
    function_adjustments = [
        ("diff", 'x', 1, 1, "before"),
        ("subs", 'x', 1, 1, "before"),
        ("integrate", 'x', 1, 2, "before"),
        ('log', '10', 1, 1, "after"),
    ]

    for args in function_adjustments:
        eq_string = add_args_to_func(eq_string, *args)

    eq_string = re.sub(r'(?<!\.)subs', r'Subs', eq_string)

    for i, constant in enumerate(constant_names):
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



def replace_dot_funcs(string: str, func_dict: dict = {"subs": "Subs", "diff": "Derivative", "integrate": "Integral"}):

    def replace_function(match):
        nonlocal extra_index_next
        expr_str = match.group(1)
        args_str = match.group(2)
        expr = expr_str
        try:
            args_var, args_val = args_str.split(',')
            func_expr = f"{replace_func}({expr}, {args_var}, {args_val})"
        except ValueError:
            args_var = args_str
            if args_var == '':
                func_expr = f"{replace_func}({expr})"
                extra_index_next -= 3
            else:
                func_expr = f"{replace_func}({expr}, {args_var})"
                extra_index_next -= 1

        extra_index_next += len(replace_func) - len(func)
        return str(func_expr)
    
    def remove_whitespace(match):
        return re.sub(r'\s+', '', match.group(0))
    

    alphabet_plus = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.^"
    string_og_list = []
    result_string = None

    for func, replace_func in func_dict.items():
        string = re.sub(rf"\.{func}\(([^()]+)\)", remove_whitespace, string)

        index_funcs = [m.start() for m in re.finditer(func, string)]
        index_dot_funcs = [m.start() for m in re.finditer(r'\.' + func, string)]
        index_range = []
        string_og_list.append(string)

        if len(index_dot_funcs) == 0 and len(index_funcs) == 0:
            continue
            
        elif len(index_dot_funcs) == 0:
            string = string.replace(func, replace_func)
            continue


        extra_index_next = 0
        for index_func in index_dot_funcs:
            index_func += extra_index_next
            relevant_string = string[:index_func]
            relevant_string_l = [char for char in reversed(relevant_string)]
            nested = 0
            index = index_func
            break_activate = False

            for char in relevant_string_l:
                if char == ')':
                    nested += 1

                elif char == '(':
                    nested -=1
                    if nested == 0:
                        break_activate = True
                        index -= 1
                        if index > 0:
                            continue
                        else:
                            index_range.append((0, index_func))

                elif nested == 0 and (char not in alphabet_plus or index == 1):
                    if index == 1:
                        index_range.append((0, index_func))
                    else:
                        index_range.append((index, index_func))
                    extra_index_next += 2
                    break

                if break_activate:
                    if not (char in alphabet_plus or char in "()") or index == 1 or nested < 0:
                        if index == 1:
                            index_range.append((0, index_func))
                        else:
                            index_range.append((index, index_func))
                        extra_index_next += 2
                        break

                index -= 1
            
            changed_string_bit = []
            for index_start, index_end in index_range:
                changed_string_bit.append(string[index_start:index_end])


            result_string = string
            for changed_string in changed_string_bit:
                pattern = f"({re.escape(changed_string)})" + rf"\.{func}\(([^()]*)\)"
                result_string = re.sub(pattern, replace_function, result_string)

                if result_string == string:
                    pattern2 = f"({re.escape(changed_string)})" + rf"\.{func}\((\([^()]*\))\)"
                    result_string = re.sub(pattern2, replace_function, result_string)

            string = result_string

    if result_string is not None:
        for func, replace_func in func_dict.items():
            result_string = re.sub(rf'(?<!\.){func}', replace_func, result_string)

        string_og_list.append(result_string)

    else:
        string_og_list = [string]

    string_og_list = [string_og for string_og in reversed(string_og_list)]
    for result_string in string_og_list:
        try:
            string = sp.sympify(result_string)
            break
        except Exception:
            continue
    
    if isinstance(string, str):
        string = string_og_list[-1]

    return string
