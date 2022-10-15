from linter import *


assert get_indent_level("") == 0
assert get_indent_level("test") == 0
assert get_indent_level("\n\t") == 0

assert get_indent_level(" test") == 2
assert get_indent_level(" ") == 2
assert get_indent_level(" \n\t") == 2

assert get_indent_level("   ") == 4
assert get_indent_level("\t") == 4

assert get_indent_level(" \t") == 6
assert get_indent_level("  \t") == 6

assert get_indent_level("\t  \t") == 10
