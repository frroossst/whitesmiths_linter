import json
import os



open_brace = "{"
close_brace = "}"


def get_all_files() -> list:
    return os.listdir(os.getcwd())

def get_files_to_skip() -> list:
    try:
        with open("whitesmiths_linter_settings.json", "r") as fobj:
            settings = json.load(fobj)
            return settings["skip"]
    except FileNotFoundError:
        generate_default_linter_settings()

def get_source_overwrite_permission() -> bool:
    with open("whitesmiths_linter_settings.json", "r") as fobj:
        settings = json.load(fobj)
        return settings["modify_source"]

def get_indent_spaces_length() -> int:
    with open("whitesmiths_linter_settings.json", "r") as fobj:
        settings = json.load(fobj)
        return int(settings["indent_space_length"])

def generate_default_linter_settings() -> None:
    default_settings = {"skip" : [
            "linter.py",
            "README.md",
            ".gitignore",
            "TODO",
            "LICENSE",
            "tests.py",
            "whitesmiths_linter_settings.json"],
    "indent_space_length": 4, "modify_source" : False}

    with open("whitesmiths_linter_settings.json", "w") as fobj:
        json.dump(default_settings,fobj, indent=6)



def main() -> None:
    files = get_all_files()
    except_src = get_files_to_skip()
    for i in files:
        if i not in except_src:
            try:
                lint(i)
                print(f"[LINTED] {i}")
            except IsADirectoryError:
                print(f"[SKIPPED] {i} is a directory")
        else:
            print(f"[SKIPPED] {i} found in exception list")

def lint(fileName: str) -> None:
    with open(fileName, "r") as fobj:
        content = fobj.read()

    tokens = tokeniser(content)
    bracket_aligned = manage_brackets(tokens)
    indent_aligned = manage_indents(bracket_aligned)

    if get_source_overwrite_permission():
        with open(fileName, "w") as fobj:
            fobj.write(indent_aligned)
    else:
        with open(fileName + "_output", "w") as fobj:
            fobj.write(indent_aligned)

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
    indent_spaces_length = get_indent_spaces_length()

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
                indented_lines.append(get_indent_whitespace(prev_indent + indent_spaces_length) + curr_line.lstrip())

            # prev = }; curr = code -> -1 level
            elif (is_a_closing_line(prev_line) and is_a_code_line(curr_line)):
                indented_lines.append(get_indent_whitespace(prev_indent - indent_spaces_length) + curr_line.lstrip())

            # prev = }; curr = } -> -1 level
            elif (is_a_closing_line(prev_line) and is_a_closing_line(curr_line)):
                indented_lines.append(get_indent_whitespace(prev_indent - indent_spaces_length) + curr_line.lstrip())

            # prev = {; curr = { -> +1 level
            elif (is_an_opening_line(prev_line) and is_an_opening_line(curr_line)):
                indented_lines.append(get_indent_whitespace(prev_indent + indent_spaces_length) + curr_line.lstrip())

            else:
                indented_lines.append(curr_line)

    return "\n".join(indented_lines)



def get_indent_level(line: str) -> int:
    
    ascii_chars = [
        "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", "-", "`", "/", ":", 
        ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "|", "~"]

    count = 0 # because natural number counting

    if line is None:
        return 0

    for i in line:
        if i.isalpha() or (i == "\n") or (i in ascii_chars):
            break
        if i.isspace():
            if i == " ":
                count += 1
            elif i == "\t":
                count += 4

    if count == 1:
        return 0
    if count % 4 == 0:
        return count
    else:
        return get_nearest_multiple_of(count, get_indent_spaces_length())

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