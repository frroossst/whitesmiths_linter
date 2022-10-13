import json
import os
import re



open_brace = "{"
close_brace = "}"

def get_all_files():
    return os.listdir(os.getcwd())

def main():
    files = get_all_files()
    except_src = get_files_to_skip()
    for i in files:
        if i not in except_src:
            try:
                lint(i)
                print(f"[LINTED] {i}")
                break # ! only for testing
            except IsADirectoryError:
                print(f"[SKIPPED] {i} is a directory")
        else:
            print(f"[SKIPPED] {i} found in exception list")

'''
    content = re.sub("[{]","\n    {\n",content)
    content = re.sub("[}]","\n    }\n",content)
'''

def get_files_to_skip():
    with open("whitesmiths_linter_settings.json", "r") as fobj:
        settings = json.load(fobj)
        return settings["skip"]

def lint(fileName) -> None:
    with open(fileName, "r") as fobj:
        content = fobj.read()

    tokens = tokeniser(content)
    bracket_aligned = manage_brackets(tokens)
    indent_aligned = manage_indents(bracket_aligned)

    with open(fileName + "_output", "w") as fobj: # temp output as I do not trust this enough to manipulate source code
        content = fobj.write(indent_aligned)

    return None


def tokeniser(content) -> list:
    lines = content.split("\n")
    return lines


def manage_brackets(tokens):
    bracket_aligned = []

    for idx, i in enumerate(tokens):
        for sub_idx, j in enumerate(i):
            curr = {"line num": idx, "char num": sub_idx, "char": j} # numbers are offset by 1
            if curr["char"] == open_brace:
                look_back = -1
                while True:
                    a = bracket_aligned[look_back]
                    if (bracket_aligned[look_back].isalnum()) and not ("\n" in bracket_aligned[look_back]) :
                        if bracket_aligned[look_back].isspace():
                            pass
                        else:
                            bracket_aligned.append("\n")
                            break
                    elif "\n" in bracket_aligned[look_back]:
                        break
                    look_back -= 1
                bracket_aligned.append(curr["char"])

            elif curr["char"] == close_brace:
                look_ahead = -1
                while True:
                    if (bracket_aligned[look_ahead].isalnum()) and not ("\n" in bracket_aligned[look_ahead]) :
                        bracket_aligned.append("\n")
                        break
                    elif "\n" in bracket_aligned[look_ahead]:
                        break
                    look_ahead -= 1
                bracket_aligned.append(curr["char"])
            else:
                bracket_aligned.append(curr["char"])

        bracket_aligned.append("\n")

    return "".join(bracket_aligned)


def manage_indents(content):
    # minimum indent level allowed is 1 i.e. 4 spaces or 1 tab
    # content = re.sub("{", "    {", content)
    # content = re.sub("}", "    }", content)

    lines = content.split("\n")
    indented_lines = []

    upper_bound = len(lines) - 1
    prev_line = None
    
    for x, i in enumerate(lines):
        if x == 0:
            indented_lines.append(i)
        else:
            prev_line = lines[x - 1]
            prev_indent = get_indent_level(prev_line)
            indented_lines.append(get_indent_whitespace(prev_indent) + i)

    return "\n".join(indented_lines)


def get_indent_level(line):
    count = 0

    if line is None:
        return count

    for i in line:
        if i.isalpha() or i == "\n":
            break
        if i.isspace():
            if i == " ":
                count += 1
            elif i == "\t":
                count += 4

    if count % 2 == 0:
        return count
    else:
        return count + 1 


def get_indent_whitespace(indent_level):
    if indent_level % 2 != 0:
        raise  Exception("InvalidIndentError")
    return " " * indent_level



if __name__ == "__main__":
    main()
