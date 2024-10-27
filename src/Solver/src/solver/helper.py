"""
This module contains a collection of helper functions used by the solver module. 
These functions provide utilities for mathematical operations, array manipulations, 
and symbolic computations.
Functions:
    unique_preserve_order(lst):
        Remove duplicates from a list while preserving the original order.
    apply_opperator(x, selected_operator, y):
        Apply a specified operator to two operands.
    segmented_linspace(start, end, breakpoints, num=10, breakpoint_offset=0.01):
    get_smooth_x_coords(x_range, dx, vert_asympt=None):
        Generate a smooth set of x-coordinates over a specified range, optionally considering vertical asymptotes.
    write_as_sin_and_cos(x):
        Simplify a SymPy expression by writing sec-csc and tan-cot in terms of cos-sin.
    pop_iterable(pop_list, index_list):
        Remove elements from a list at the specified indices.
    map_equation_type_to_sp(eq_type):
        Map a string representation of an equation type to its corresponding SymPy function or operator.
This module contains helper functions used by the solver module.
"""

import numpy as np
import sympy as sp
import operator
from sympy.simplify.fu import TR2, TR1, TR111
import typing


def unique_preserve_order(lst):
    """
    Return a list of unique elements from the input list while preserving the order of their first occurrence.

    Args:
        lst (list): The input list from which to remove duplicates.

    Returns:
        list: A list containing unique elements from the input list, in the order of their first occurrence.
    """
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

def apply_opperator(x, selected_operator, y):
    """
    Apply a comparison operator to two values.

    Parameters:
    x (any): The first value to compare.
    selected_operator (str): The operator to apply. Supported operators are:
                             "==", "=", "!=", ">", "<", ">=", "<=".
    y (any): The second value to compare.

    Returns:
    bool: The result of the comparison.

    Raises:
    ValueError: If an invalid operator is provided.
    """
    # Dictionary to map operator strings to functions
    operators = {
        "==": operator.eq,  # Equality
        "=": operator.eq,   # Equality
        "!=": operator.ne,  # Not equal
        ">": operator.gt,   # Greater than
        "<": operator.lt,   # Less than
        ">=": operator.ge,  # Greater than or equal to
        "<=": operator.le,  # Less than or equal to
    }
    try:
        return operators[selected_operator](x, y)
    except KeyError:
        raise ValueError("Invalid operator")

def segmented_linspace(start: float, end: float, breakpoints: typing.Iterable[float], num: int=10, breakpoint_offset: float=0.01) -> typing.List[np.ndarray]:
    """
    Generate a list of linearly spaced segments between `start` and `end`, divided by `breakpoints`.

    Args:
        start (float): The starting point of the range.
        end (float): The ending point of the range.
        breakpoints (Iterable[float]): Points at which the range is divided into segments.
        num (int): Number of points in each segment (default is 10).
        breakpoint_offset (float): Small offset added to the start and end of each segment (default is 0.01).

    Returns:
        List[np.ndarray]: A list of numpy arrays, each containing a segment of linearly spaced points.
    """

    all_points = sorted([start] + list(breakpoints) + [end])
    return [np.linspace(all_points[i] + breakpoint_offset, all_points[i+1] - breakpoint_offset, num) for i in range(len(all_points)-1)]


def get_smooth_x_coords(x_range, dx, vert_asympt=None):
    """
    Generate a smooth set of x-coordinates over a specified range.
    Parameters:
    x_range (tuple): A tuple containing the start and end of the x-coordinate range.
    dx (float): The step size for generating the x-coordinates.
    vert_asympt (list, optional): A list of vertical asymptotes to consider when generating the x-coordinates. Defaults to None.
    Returns:
    numpy.ndarray: An array of x-coordinates that are smoothly distributed over the specified range.
    """
    if vert_asympt is None:
        x_coords = np.linspace(x_range[0] - 1, x_range[1] + 1, int(1/dx))
        for i in range(1, 10):
            x_coords = np.sort(np.append(x_coords, np.linspace(x_range[0]/(10**i), x_range[1]/(10**i), max(10, int(10/(dx*10**i))))))

    else:
        x_coords = segmented_linspace(x_range[0] - 1, x_range[1] + 1, vert_asympt, num=int(1/dx), breakpoint_offset=0.00001)
        if len(x_coords) > 3:
            return x_coords

        for i in range(1, 5):
            new_x_coords = segmented_linspace(x_range[0]/(10**i), x_range[1]/(10**i), vert_asympt, num=max(10, int(10/(dx*10**i))), breakpoint_offset=0.00001)
            for i in range(len(x_coords)):
                array = x_coords[i]
                min_array = min(array)
                max_array = max(array)
                for array_new in new_x_coords:
                    if min_array <= np.mean(array_new) <= max_array:
                        x_coords[i] = np.sort(np.append(array, array_new))

    return x_coords


def write_as_sin_and_cos(x):
    """
    Write sec-csc and tan-cot in terms of cos-sin.

    Args:
        expr (sp.Basic): The SymPy expression to simplify.

    Returns:
        sp.Basic: The simplified SymPy expression.
    """

    return TR1(TR2(x))

def pop_iterable(pop_list: list, index_list: typing.Iterable[int]) -> list:
    """
    Remove elements from `pop_list` at the specified indices.

    Args:
        pop_list (list): The list from which elements will be removed.
        index_list (Iterable[int]): List of indices to remove from `pop_list`.

    Returns:
        list: The list after the specified elements have been removed.
    """

    for index in sorted(index_list, reverse=True):
        pop_list.pop(index)
    return pop_list

def map_equation_type_to_sp(eq_type: str):
    """
    Maps a string representation of an equation type to its corresponding sympy or operator function.

    Args:
        eq_type (str): The string representation of the equation type. 
                       Possible values include '!=', '>=', '<=', '==', '=', '>', '<'.

    Returns:
        function or str: The corresponding sympy or operator function if the input is a recognized equation type.
                         If the input is not recognized, it returns the input string itself.
    """
    equation_symbol_map = {"!=": sp.Ne, ">=": sp.Ge, "<=": sp.Le, "==": operator.eq, "=": sp.Eq, ">": sp.Gt, "<": sp.Lt}
    return equation_symbol_map.get(eq_type, eq_type)