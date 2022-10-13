def get_indent_level(line):
    count = 0

    for i in line:
        if i.isalpha() or i == "\n":
            return count
        if i.isspace():
            if i == " ":
                count += 1
            elif i == "\t":
                count += 4

    return count



assert get_indent_level("") == 0
assert get_indent_level("test") == 0
assert get_indent_level("\n\t") == 0

assert get_indent_level(" test") == 1
assert get_indent_level(" ") == 1
assert get_indent_level(" \n\t") == 1

assert get_indent_level("   ") == 3

assert get_indent_level("\t") == 4

assert get_indent_level(" \t") == 5

assert get_indent_level("  \t") == 6

assert get_indent_level("\t  \t") == 10
