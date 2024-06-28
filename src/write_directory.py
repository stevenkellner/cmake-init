import os.path
import re
import sys
from typing import Callable, Dict, List, Optional, Tuple


class Variables:
    def __init__(self):
        self.dict: Dict[str, str] = {}
        self.bool_values: Dict[str, bool] = {}

    def set_variable(self, variable: str, value: str):
        self.dict[variable] = value

    def set_bool(self, variable: str, value: bool):
        self.bool_values[variable] = value

    def value(self, variable: str) -> str:
        if variable not in self.dict:
            raise SyntaxError(f"Unknown value variable {variable}")
        return self.dict[variable]

    def is_true(self, variable: str) -> bool:
        if variable not in self.bool_values:
            raise SyntaxError(f"Unknown bool variable {variable}")
        return self.bool_values[variable]


def compile_template(template_content: str, variables: Variables) -> str:
    block_regex = re.compile(r"(.*?)({% .+? %}|{= .+? =})|(.+?)\Z", re.MULTILINE | re.DOTALL)

    depth = 0
    python_source = ["def f():\n _result = []"]

    def add_line(line):
        python_source.append(" " * (depth + 1) + line)

    def add_repr(o):
        add_line("_result.append(str(" + repr(o) + "))")

    for match in block_regex.finditer(template_content):
        before, block, tail = match.groups()
        if not block:
            add_repr(tail)
            continue
        if block == "end":
            depth -= 1
            continue
        if before:
            add_repr(before)
        inner = block[3:-3]
        if block[1:2] == "=":
            add_repr(variables.value(inner))
            continue
        if inner == "end":
            depth -= 1
            continue
        if inner == "else" or inner.startswith("elif "):
            depth -= 1
        add_line(inner + ":")
        depth += 1

    if depth != 0:
        raise SyntaxError("Block not properly terminated")

    add_line("return \"\".join(_result)")
    locals = {}
    exec("\n".join(python_source), variables.bool_values, locals)
    return locals["f"]()


def write_file(path: str, template_path: str, variables: Variables):
    with open(template_path, "r", encoding="UTF-8") as f:
        template_content = f.read()
    content = compile_template(template_content, variables)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, "w", encoding="UTF-8", newline="\n") as f:
        f.write(content)


def include_file(path: str, variables: Variables) -> bool:
    if path == "cmake\\project-is-top-level.cmake":
        return not variables.is_true("cmake_321")
    if path == "vcpkg.json":
        return variables.is_true("vcpkg")
    if path == "conanfile.py" or path == ".github\\scripts\\conan-ci-setup.sh":
        return variables.is_true("conan")
    if path == "cmake\\install-config.cmake":
        return not variables.is_true("exe")
    if path == "env.ps1" or path == "env.bat":
        return variables.is_true("lib") and not variables.is_true("pm")
    return True


def write_directory(path: str, variables: Variables, name: str):
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', name)
    if not os.path.exists(template_path) or not os.path.isdir(template_path):
        print(f"Template {name} not found", file=sys.stderr)
        exit(1)
    for directory_path, _, file_names in os.walk(template_path):
        for template_file_path in [os.path.join(directory_path, file_name) for file_name in file_names]:
            rel_file_path = os.path.relpath(template_file_path, template_path)
            if not include_file(rel_file_path, variables):
                continue
            file_path = os.path.join(path, rel_file_path.replace("__name__", variables.value("name")))
            write_file(file_path, template_file_path, variables)
