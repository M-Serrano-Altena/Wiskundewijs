import numpy as np
import sympy as sp
import re

def fix_internal_links(html_content):
    """Convert .md links to the MkDocs format (/folder/)"""
    return re.sub(r'href="([^"]+)\.md([^"]*)"', r'href="\1/\2"', html_content)

string = 'href="../../afgeleide.md#regels"'
print(fix_internal_links(string)) # href="/test/"