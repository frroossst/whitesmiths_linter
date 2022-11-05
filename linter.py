import json
import os



open_brace = "{"
close_brace = "}"


def get_all_files() -> list:
    return os.listdir(os.getcwd())


def main() -> None:
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


def get_files_to_skip() -> list:
    with open("whitesmiths_linter_settings.json", "r") as fobj:
        settings = json.load(fobj)
        return settings["skip"]


def lint(fileName: str) -> None:
    with open(fileName, "r") as fobj:
        content = fobj.read()

    tokens = tokeniser(content)
    bracket_aligned = manage_brackets(tokens)
    print("*"*10,"After Brackets Aligned")
    print(bracket_aligned)
    indent_aligned = manage_indents(bracket_aligned)
    print("*"*10,"After Indent Management")
    print(indent_aligned)

    with open(fileName + "_output", "w") as fobj: # temp output as I do not trust this enough to manipulate source code
        content = fobj.write(indent_aligned)

    return None


def tokeniser(content: str) -> list:
    lines = content.split("\n")
    return lines


def manage_brackets(tokens: str) -> str:
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


def manage_indents(content: str) -> str:
    # minimum indent level allowed is 1 i.e. 4 spaces or 1 tab
    # content = re.sub("{", "    {", content)
    # content = re.sub("}", "    }", content)

    lines = content.split("\n")
    indented_lines = []

    prev_line = None
    
    for x, i in enumerate(lines):
        if x == 0:
            indented_lines.append(i)
        else:
            curr_line = i
            prev_line = indented_lines[-1]
            prev_indent = get_indent_level(prev_line)

            print(x,i)
            print(f"prev line: {prev_line}")
            print(f"prev indent: {prev_indent}")
            print(f"curr line: {curr_line}")
            print(f"curr indent: {get_indent_level(curr_line)}")
            print()

            # prev = code; curr = code -> same as prev
            if (is_a_code_line(prev_line)) and (is_a_code_line(curr_line)):
                indented_lines.append(get_indent_whitespace(prev_indent) + curr_line.lstrip())

            # prev = {; and curr = code -> same as prev
            elif (is_an_opening_line(prev_line)) and (is_a_code_line(curr_line)):
                indented_lines.append(get_indent_whitespace(prev_indent) + curr_line.lstrip())

            # prev = code; curr = } -> same as prev
            elif (is_a_code_line(prev_line)) and (is_a_closing_line(curr_line)):
                indented_lines.append(get_indent_whitespace(prev_indent) + curr_line.lstrip())

            # prev = code; curr = { -> +1 level
            elif (is_a_code_line(prev_line)) and (is_an_opening_line(curr_line)):
                indented_lines.append(get_indent_whitespace(prev_indent + 4) + curr_line.lstrip())

            # prev = }; curr = code -> -1 level
            elif (is_a_closing_line(prev_line) and is_a_code_line(curr_line)):
                indented_lines.append(get_indent_whitespace(prev_indent - 4) + curr_line.lstrip())

            else:
                indented_lines.append(curr_line)

    return "\n".join(indented_lines)


def get_indent_level(line: str) -> int:
    
    ascii_chars = [
        "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", "-", "`", "/", ":", 
        ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "|", "~"]

    count = 1 # because natural number counting

    if line is None:
        return 0

    for i in line:
        if i.isalpha() or (i == "\n") or (i in ascii_chars):
            break
        if i.isspace():
            if i == " ":
                count += 1
            elif i == "\t":
                count += 3

    if count == 1: # due to how the loop works with special characters
        return 0
    if count % 4 == 0:
        return count
    else:
        return get_nearest_multiple_of(count, 4)


def get_nearest_multiple_of(x: int, of: int) -> int:
    return ((x + (of - 1)) & (-of))

def get_indent_whitespace(indent_level: int, useTabs=False) -> str:
    if indent_level % 2 != 0:
        raise  Exception("InvalidIndentError")
    if indent_level < 0:
        return ""
    return " " * indent_level

def is_a_code_line(line):
    return (line.strip() != open_brace) and (line.strip() != close_brace)

def is_an_opening_line(line):
    return line.strip() == open_brace

def is_a_closing_line(line):
    return line.strip() == close_brace



if __name__ == "__main__":
    main()
