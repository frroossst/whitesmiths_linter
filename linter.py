from itertools import chain
import os



def get_all_files():
    return os.listdir(os.getcwd())

def main():
    files = get_all_files()
    except_src = ["linter.py","README.md",".gitignore","TODO"]
    for i in files:
        if i not in except_src:
            try:
                lint(i)
                print(f"[LINTED] {i}")
            except IsADirectoryError:
                print(f"[SKIPPED] {i} is a directory")
        else:
            print(f"[SKIPPED] {i} found in exception list")

'''
    content = re.sub("[{]","\n    {\n",content)
    content = re.sub("[}]","\n    }\n",content)
'''

def lint(fileName) -> None:
    with open(fileName, "r") as fobj:
        content = fobj.read()

    tokens = tokeniser(content)
    bracket_aligned = manage_brackets(tokens)
    indent_aligned = manage_indents(bracket_aligned)

    return None


def tokeniser(content) -> list:
    lines = content.split("\n")
    return lines


def manage_brackets(tokens):
    open_brace = "{"
    close_brace = "}"
    
    bracket_aligned = []

    for idx, i in enumerate(tokens):
        for sub_idx, j in enumerate(i):
            curr = {"line num": idx, "char num": sub_idx, "char": j} # numbers are offset by 1
            if curr["char"] == open_brace:
                look_back = -1
                while True:
                    if (bracket_aligned[look_back].isalnum() or bracket_aligned[look_back].isspace()) and not ("\n" in bracket_aligned[look_back]) :
                        bracket_aligned.append("\n")
                    elif "\n" in bracket_aligned[look_back]:
                        break
                    look_back -= 1
                bracket_aligned.append(curr["char"])
            elif curr["char"] == close_brace:
                look_ahead = -1
                while True:
                    if (bracket_aligned[look_ahead].isalnum()) and not ("\n" in bracket_aligned[look_ahead]) :
                        bracket_aligned.append("\n")
                    elif "\n" in bracket_aligned[look_back]:
                        break
                    look_back -= 1
                bracket_aligned.append(curr["char"])
            else:
                bracket_aligned.append(curr["char"])


            print(curr)

        bracket_aligned.append("\n")
        print(idx)


    return bracket_aligned


def manage_indents(content):
    return content



if __name__ == "__main__":
    main()
