import numpy as np
import sympy as sp
import regex as re


def add_args_to_func(eq_string, func_name: str='log', replace_with: str='10', amt_commas=1, func_amt_commas={'diff': 2, 'subs': 2, 'integrate': 3}, nested_level=1, position_type='after'):
    
    def check_object_number():
        index_comma = index - sum([len(string_) for string_ in string_split[:string_index]])
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
        # print(relevant_string)

        try:
            return sp.sympify(relevant_string).is_number
        except Exception:
            return False
        
    def count_commas():
        index_bracket = index - sum([len(string_) for string_ in string_split[:string_index]])
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

    
    index_func = [m.start() for m in re.finditer(func_name, eq_string)]
    index_dot_func = [m.start() for m in re.finditer(r'\.' + func_name, eq_string)]
    is_dot_func = []
    func_amt_commas_start = func_amt_commas.copy()

    for func_index in index_func:
        is_dot_func.append(func_index - 1 in index_dot_func)

    if len(index_func) == 0:
        return eq_string
    
    string_split = [list(eq_string)[index_func[i-1]:index_func[i]] if i != len(index_func) else list(eq_string)[index_func[i - 1]:] for i in range(1, len(index_func) + 1) ]
    index_list_secure = []
    nested = 0
    index = 0
    replace = 0

    if amt_commas < 0:
        amt_commas += eq_string.count(',') + 1

    amt_commas_start = amt_commas
    num_comma = amt_commas
    string_index = -1


    for string in string_split:
        string_index += 1

        replace += 1
        if replace < 1:
            replace = 1

        index_list = []
        amt_commas = amt_commas_start
        func_amt_commas = func_amt_commas_start.copy()
        nested_before = nested
        nested = 0
        replace_with_pretty = f', {replace_with}'
        index_before = None
        check_is_number = False
        comma_amt = 0
        is_nested = False
        no_replace = lambda: (nested == 0 and nested_before == 0 and is_nested)

        index_open_bracket = 0

        if is_dot_func[string_index]:
            amt_commas -= 1
            if func_amt_commas.get(func_name, None) is not None:
                func_amt_commas[func_name] -= 1

        if func_name in func_amt_commas.keys():
            num_comma = func_amt_commas[func_name]

        # print(func_amt_commas_start)
        # print("num comma = ", num_comma)

        for char in string:
            if no_replace():
                index += 1
                continue
                
            if is_dot_func[string_index]:
                index_before = index

            if position_type == 'before':
                if char == '(':
                    is_nested = True
                    nested += 1
                    if amt_commas == 0 and replace > 0:
                        if index_before is None:
                            index_before = index
                        elif nested == nested_level:
                            index_before = None
                            check_is_number = check_object_number()
                            comma_amt = count_commas()
                            if check_is_number and comma_amt <= num_comma - 1:
                                replace_with_pretty = f'{replace_with}, '
                                index_list.append((index + 1, replace_with_pretty))
                                replace -= 1

                    
                elif char == ')':
                    nested -= 1
                    if nested == 0 and replace > 0 and index_before is not None and check_is_number and comma_amt < num_comma - 1:
                        if nested_before == 0 and amt_commas == 0:
                            replace_with_pretty = f', {replace_with}'
                            if index_before not in index_list:
                                index_list.append((index_before, replace_with_pretty))
                            else:
                                index_list.append((index + 1, replace_with_pretty))

                            replace -= 1

                    if nested == 0:
                        amt_commas = amt_commas_start
                        nested = nested_before


                elif char == ',' and nested == 1:
                    amt_commas -= 1

                    if amt_commas == 0 and replace > 0:
                        index_before = index

                        if nested_level == 1:
                            replace_with_pretty = f', {replace_with}'
                            check_is_number = check_object_number()
                            comma_amt = count_commas()
                            # print(check_is_number)
                            if check_is_number and comma_amt < num_comma - 1: 
                                index_list.append((index_before, replace_with_pretty))
                                replace -= 1
                                check_is_number = False

                if amt_commas < 0 and len(index_list) != 0 and nested_before == 0:
                    index_list.pop()
                    amt_commas += 1


            elif position_type == 'after':
                if char == '(':
                    index_open_bracket = index - sum([len(string_) for string_ in string_split[:string_index]])
                    nested += 1
                elif char == ')':
                    nested -= 1

                elif char == ',' and nested == 1:
                    if amt_commas == 1:
                        replace -= 1
                    else:
                        amt_commas -= 1

                if char == ')' and nested == 0:
                    index_close_bracket = index - sum([len(string_) for string_ in string_split[:string_index]])

                    if np.array([(char in "()") for char in string[index_open_bracket:index_close_bracket + 1]]).all():
                        replace_with_pretty = replace_with

                    if replace > 0:
                        index_list.append((index, replace_with_pretty))
                    
                    replace -= 1
                    amt_commas = amt_commas_start
                    nested = nested_before

            # print(char, nested, nested_before, amt_commas, replace, index, index_list, no_replace())

            index += 1

        index_list_secure.extend(index_list)

    additional_index = index_func[0]
    for index, replace_with_pretty in index_list_secure:
        eq_string = eq_string[:index + additional_index] + replace_with_pretty + eq_string[index + additional_index:]
        additional_index += len(replace_with_pretty)
    
    return eq_string



def math_interpreter(eq_string):

    def insert_asterisks(match):
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
            index_start = pos - index_range if pos - index_range >= 0 else 0
            index_end = match.end() + index_range if match.end() + index_range <= len(eq_string) else len(eq_string)
            if func in eq_string[index_start:index_end]:
                return match.group(0)


        return '*'.join(char for _ in range(count))

    def replace_constant_symbols(eq_string):
        def replace_superscript(match):
            matched_super = match.group(1)
            matched_super_list = list(matched_super)
            index_list = [list_superscript.index(matched_super_list[i]) for i in range(len(matched_super_list))]
            letter_list = [list_corresp_letters[i] for i in index_list]
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
        list_superscript = list(string_superscripts)
        list_corresp_letters = list(string_corresp_letters)

        
        eq_string = re.sub(f'([{string_superscripts}]+)', replace_superscript, eq_string)

        return eq_string
    

    def add_parenthesis(match, extra_index=0):
        function_name = match.group(1)
        symbol = match.group(2)

        # quick check
        if function_name + symbol in relevant_functions:
            return match.group(0)
        
        # thourough check
        for func in relevant_functions:
            if func == function_name:
                continue

            length_func_name = len(func)
            length_match_func = len(function_name)
            index_range = length_func_name - length_match_func

            if index_range <= 0:
                continue

            index_start_match = match.start(1) + extra_index
            index_end_match = match.end(1) + extra_index
            index_start = index_start_match - index_range if index_start_match - index_range >= 0 else 0
            index_end = index_end_match + index_range if index_end_match + index_range <= len(eq_string) else len(eq_string)

            if func in eq_string[index_start:index_end]:
                if function_name in func and func != function_name:
                    return match.group(0)

        
        return f'{function_name}({symbol})'


    def mult_constants(match):
        function_name = match.group(1)
        symbol = match.group(2)
        extra_index = 0

        # quick check
        if function_name + symbol in relevant_functions:
            return match.group(0)
        
        # thourough check
        for func in relevant_functions:
            if func == function_name:
                continue

            length_func_name = len(func)
            length_match_func = len(function_name)
            index_range = length_func_name - length_match_func

            if index_range <= 0:
                continue

            index_start_match = match.start(1) + extra_index
            index_end_match = match.end(1) + extra_index
            index_start = index_start_match - index_range if index_start_match - index_range >= 0 else 0
            index_end = index_end_match + index_range if index_end_match + index_range <= len(eq_string) else len(eq_string)

            if func in eq_string[index_start:index_end]:
                if function_name in func and func != function_name:
                    return match.group(0)


        matched = match.group(1)
        constant_name = match.group(2)

        # quick check
        if matched + constant_name in constant_names:
            return match.group(0)
        
        # thourough check
        for const in constant_names:
            if const == constant_name:
                continue
            
            length_const_name = len(const)
            length_match_const = len(constant_name)
            index_range = length_const_name - length_match_const

            if index_range <= 0:
                continue

            index_start_match = match.start(1)
            index_end_match = match.end(2)
            index_start = index_start_match - index_range if index_start_match - index_range >= 0 else 0
            index_end = index_end_match + index_range if index_end_match + index_range <= len(eq_string) else len(eq_string)

            if const in eq_string[index_start:index_end]:
                if constant_name in const and const != constant_name:
                    return match.group(0)

        return f'{matched}*{constant_name}'
        

    eq_string = eq_string.casefold()
    function_names = [name for name in dir(sp.functions) if not name.startswith('_')]
    function_names.extend(("diff", "integrate", "limit", "Mod", "subs"))
    function_names.remove("ff")
    relevant_functions = [func for func in function_names if func in eq_string]


    constant_names_og = [name for name, obj in sp.__dict__.items() if isinstance(obj, (sp.Basic, sp.core.singleton.Singleton)) and not name.startswith('_') and sp.sympify(name).is_number]
    constant_names_og.extend(("inf", "infty", "infinity"))
    constant_names = [name.casefold() for name in constant_names_og]

    eq_string = replace_constant_symbols(eq_string)


    abs_pattern = re.compile(r"\|([^|]+)\|")
    eq_string = re.sub(abs_pattern, r"Abs(\1)", eq_string)
    eq_string = re.sub(r'abs', r'Abs', eq_string)
    eq_string = re.sub(r'mod', r'Mod', eq_string)
    eq_string = re.sub(r'lambertw', r'LambertW', eq_string)

    arc_gonio_functions = ["arcsin", "arccos", "arctan", "arccot", "arcsec", "arccsc"]
    relevant_arc_functions = [arc_gonio_func for arc_gonio_func in arc_gonio_functions if arc_gonio_func in eq_string]

    if len(relevant_arc_functions) != 0:
        for arc_gonio_func in relevant_arc_functions:
            a_gonio_func = arc_gonio_func[0] + arc_gonio_func[3:]
            eq_string = re.sub(re.escape(arc_gonio_func), re.escape(a_gonio_func), eq_string)
            relevant_functions.insert(0, a_gonio_func)

    relevant_functions.extend([func for func in ["Abs", "Mod", "LambertW"] if func in eq_string])

    eq_string = re.sub(r'\b' + r'i'  + r'\b', r'I', eq_string)
    eq_string = re.sub(r'\b' + r'e'  + r'\b', r'E', eq_string)

    eq_string = re.sub(r"%(?!\d)", r'*0.01', eq_string)

    eq_string = re.sub(r'(\d+/\d+)\s+(\d+/\d+)', r'\1*\2', eq_string)
    eq_string = re.sub(r'(\d+)\s+(\d+/\d+)', r'(\1+\2)', eq_string)

    eq_string = re.sub(r"\s+" + r"\.", ".", eq_string)
    eq_string = re.sub(r"\b" + r"(\d+)" +  r"\.", r"(\1).", eq_string)

    if len(relevant_functions) != 0:
        eq_string = re.sub(rf'({'|'.join(map(re.escape, relevant_functions))})' + r'(?:\s)+([\w]+)', r'\1(\2)', eq_string)
   
    eq_string = re.sub(r'(?<=[\w)])\s+(?=[\w(])', '*', eq_string)

    if len(relevant_functions) != 0:
        eq_string = re.sub(rf'({'|'.join(map(re.escape, relevant_functions))})' r'(?!\w+|\()', r'\1(x)', eq_string)
    
    for _ in range(10):
        eq_string = re.sub(r'(?<!\.)' + r'\b' + r'0(\d)', r'\1', eq_string) # remove leading 0

        eq_string = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_string)
        eq_string = re.sub(r'\b' + r'([a-zA-Z])(\d)', r'\1^\2', eq_string)
        eq_string = re.sub(r'\)(\d)', r')*\1', eq_string)
        eq_string = re.sub(r'(\d)\(', r'\1*(', eq_string)

        eq_string = re.sub(r'\)([a-zA-Z])', r')*\1', eq_string)
        eq_string = re.sub(r'([a-zA-Z])\(', r'\1*(', eq_string)
        eq_string = re.sub(r'\)\(', r')*(', eq_string)

        eq_string = re.sub(r'([a-zA-Z])\1+', insert_asterisks, eq_string)
        eq_string = re.sub(r'\b' + r'([e])' + r'\b', r'E', eq_string)
        eq_string = re.sub(r'\b' + r'([i])' + r'\b', r'I', eq_string)
        
        for function_name1 in relevant_functions:
            for function_name2 in relevant_functions:
                eq_string = re.sub(function_name1 + function_name2 + r'\((.*?)\)', rf"{function_name1}({function_name2}\1)", eq_string)
                eq_string = re.sub(function_name2 + function_name1 + r'\((.*?)\)', rf"{function_name2}({function_name1}\1)", eq_string)

            eq_string = re.sub(function_name1 + r'\*' + rf'(?!(?:{'|'.join(map(re.escape, relevant_functions))}))' + r'(\d+|[a-zA-Z])', function_name1 + r'(x)*\1', eq_string)


            matches = re.finditer(rf'({re.escape(function_name1)})' + rf'(?!(?:{'|'.join(map(re.escape, relevant_functions))}))' +  r'([\w(]+)', eq_string, overlapped=True)
            old_eq_string = eq_string
            for match in matches:
                extra_index = len(eq_string) - len(old_eq_string)
                eq_string = re.sub(re.escape(match.group()), add_parenthesis(match, extra_index), eq_string, count=1)
            
            if len(relevant_functions) != 0:
                eq_string = re.sub(r'\b' + rf'(?!(?:{'|'.join(map(re.escape, relevant_functions))}))' + r'([\w]+)' + function_name1, r'\1*' + function_name1, eq_string)
            
            eq_string = re.sub(function_name1 + r'\*\(', function_name1 + '(', eq_string)

            
            for function_name2 in relevant_functions:
                eq_string = re.sub(function_name1 + function_name2 + r'\((.*?)\)', rf"{function_name1}({function_name2}(\1))", eq_string)
                eq_string = re.sub(function_name2 + function_name1 + r'\((.*?)\)', rf"{function_name2}({function_name1}(\1))", eq_string)
    
    if len(relevant_functions) != 0:
        eq_string = re.sub(rf'({'|'.join(map(re.escape, relevant_functions))})' r'(?!\w+|\()', r'\1(x)', eq_string)
    
    for constant in constant_names:
        if len(relevant_functions) != 0:
            eq_string = re.sub(rf'(?!(?:{'|'.join(map(re.escape, relevant_functions))}))' + r'([\w]+)' + f"({constant})", mult_constants, eq_string)
            eq_string = re.sub(rf'(?!(?:{'|'.join(map(re.escape, relevant_functions))}))' + f"({constant})" + r'([\w]+)', mult_constants, eq_string)
        else:
            eq_string = re.sub(r'([\w]+)' + f"({constant})", mult_constants, eq_string)
            eq_string = re.sub(f"({constant})" + r'([\w]+)', mult_constants, eq_string)
    
    eq_string_start = eq_string

    # print(eq_string)

    eq_string = add_args_to_func(eq_string, func_name="diff", replace_with='x', amt_commas=1, nested_level=1, position_type="before")
    eq_string = add_args_to_func(eq_string, func_name="subs", replace_with='x', amt_commas=1, nested_level=1, position_type="before")
    eq_string = add_args_to_func(eq_string, func_name="integrate", replace_with='x', amt_commas=1, nested_level=2, position_type="before")    
    eq_string = add_args_to_func(eq_string, func_name='log', replace_with='10')

    eq_string = re.sub(r'(?<!\.)subs', r'Subs', eq_string)

    for i in range(len(constant_names)):
        constant = constant_names[i]

        if re.search(r'\b' + str(constant) + r'\b', eq_string) is not None:
            if constant in constant_names and constant not in constant_names_og:
                eq_string = re.sub(r'\b' + str(constant) + r'\b', str(constant_names_og[i]), eq_string)
    
    try:
        symbol_list = list(sp.sympify(eq_string.replace("=", "+").replace("diff", "Derivative").replace("integrate", "Integral"), evaluate=False).free_symbols)
        if len(symbol_list) != 0 and len(re.findall(r"\b" + "x" + r"\b", eq_string_start)) == 0: 
            symbol = symbol_list.pop()
            eq_string = re.sub(r"\b" + "x" + r"\b", str(symbol), eq_string)
    except Exception:
        pass

    return eq_string



def replace_dot_funcs(string: str, func_dict: dict = {"subs": "Subs", "diff": "Derivative", "integrate": "Integral"}):

    def replace_function(match):
        nonlocal extra_index_next
        # print("ENTERED THE MAIN FRAME")
        expr_str = match.group(1)
        args_str = match.group(2)
        # print(expr_str, args_str)
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
        # print(func_expr)
        return str(func_expr)
    
    def escape_characters(string):
        string_list = list(string)
        escape_list = ".^$*+?{}[]()|\\"
        escape_index = 0
        index_list = []
        for char in string_list:
            if char in escape_list:
                index_list.append(escape_index)
                escape_index += 1

            escape_index += 1

        for escape_index in index_list:
            string_list.insert(escape_index, "\\")

        string = ''.join(string_list)
        return string
    
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
            # print()
            # print()
            # print(extra_index_next)
            index_func += extra_index_next
            relevant_string = string[:index_func]
            # print("relevant string = ", relevant_string)
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
                    # print(char, char not in alphabet_plus)
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

                # print(char, nested, index)
                
                index -= 1
            
            changed_string_bit = []
            for index_start, index_end in index_range:
                changed_string_bit.append(string[index_start:index_end])


            # print(changed_string_bit)

            result_string = string
            for changed_string in changed_string_bit:
                pattern = f"({escape_characters(changed_string)})" + rf"\.{func}\(([^()]*)\)"
                # print("pattern = ", pattern)
                result_string = re.sub(pattern, replace_function, result_string)
                # print("result string = ", result_string)

                if result_string == string:
                    pattern2 = f"({escape_characters(changed_string)})" + rf"\.{func}\((\([^()]*\))\)"
                    # print("pattern = ", pattern2)
                    result_string = re.sub(pattern2, replace_function, result_string)
                    # print("result string = ", result_string)

            string = result_string

    if result_string is not None:
        for func, replace_func in func_dict.items():
            # print("before = ", result_string)
            result_string = re.sub(rf'(?<!\.){func}', replace_func, result_string)
            # print("after = ", result_string)

        string_og_list.append(result_string)

    else:
        string_og_list = [string]

    string_og_list = [string_og for string_og in reversed(string_og_list)]
    for result_string in string_og_list:
        try:
            string = sp.sympify(result_string)
            # print("updated string = ", string)
            break
        except Exception:
            continue
    
    if isinstance(string, str):
        string = string_og_list[-1]

    return string
