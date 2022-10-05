import re
import os



def main():
    files = get_all_files()
    except_src = ["linter.py"]
    for i in files:
        if i not in except_src:
            try:
                code_formatter(i)
            except IsADirectoryError:
                print(f"[SKIPPED] {i} is a directory")

def get_all_files():
     return os.listdir(os.getcwd())

def code_formatter(fileName):
    with open(fileName, "r") as fobj:
        content = fobj.read()
        content = re.sub("[{]","\n\t{",content)
        content = re.sub("[}]","\t}\n",content)

        content = [x for x in content.splitlines() if x.strip() != ""]
        content = "\n".join(content)

    content = fix_indent_levels(content)

    with open(fileName, "w") as fobj:
        fobj.write(content)

def fix_indent_levels(content): 
    '''
    { => aligns to next line of code

    } => aligns to previous line of code 
    '''
    opening_brace = "{"
    closing_brace = "}"
    linesplit_li = content.splitlines()
    processed_li = []

    for x, i in enumerate(linesplit_li):
        if opening_brace in i:
            next_indent_level = get_indent_level(linesplit_li[x + 1])
            curr_indent_level = get_indent_level(i)
            fixed = match_indent_levels(next_indent_level, curr_indent_level, i)
            processed_li.append(fixed)

        elif closing_brace in i:
            prev_indent_level = get_indent_level(linesplit_li[x - 1])
            curr_indent_level = get_indent_level(i)
            fixed = match_indent_levels(prev_indent_level, curr_indent_level, i)
            processed_li.append(fixed)

        else:
            processed_li.append(i)

    matched_indents = "\n".join(processed_li)

    return matched_indents


def get_indent_level(line):
    count = 0
    for i in line:
        if not i.isalnum():
            if i == " ":
                count += 1
            elif i == "\t":
                count += 4
        else:
            break

    return count


def match_indent_levels(tomatch, current, str):
    if tomatch > current:
        return " " * (tomatch - current) + str
    elif tomatch < current:
        str = str.lstrip()
        return " " * tomatch + str
    else: 
        return str

def check_function_complexity(fileName):
     pass

def check_McGabe_complexity(fileName):
     pass



if __name__ == "__main__":
    main()