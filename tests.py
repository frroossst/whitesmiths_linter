from linter import *


assert get_indent_level(None) == 0

assert get_indent_level("") == 0
assert get_indent_level("test") == 0
assert get_indent_level("\n\t") == 0
assert get_indent_level(" test") == 0
assert get_indent_level(" ") == 0
assert get_indent_level(" \n\t") == 0

assert get_indent_level("   ") == 4
assert get_indent_level("    ") == 4
assert get_indent_level("\t") == 4

assert get_indent_level(" \t") == 8
assert get_indent_level("\t ") == 8
assert get_indent_level("  \t") == 8
assert get_indent_level("\t\t") == 8

assert get_indent_level("\t  \t") == 12
