import os
import platform
import sys
from typing import Callable, Optional, TypeVar

from src.argument_parser import Arguments
from src.init_git import init_git
from src.write_directory import Variables, write_directory


def handle_directory_exists(path: str, overwrite: bool):
    if overwrite:
        return
    if os.path.exists(path) and os.path.isdir(path) and len(os.listdir(path)) != 0:
        print(
            f"Error - directory exists and is not empty:\n{path}\nUse --overwrite to overwrite the existing directory",
            file=sys.stderr
        )
        exit(1)


T = TypeVar('T')


def prompt(header: str, message: str, default: str, mapper: Callable[[str], Optional[T]]) -> T:
    print()
    print(header)
    while True:
        print(f"{message} | default {default}: ")
        input_value = input()
        if input_value == "":
            default_value = mapper(default)
            if default_value is None:
                continue
            return default_value
        value = mapper(input_value)
        if value is not None:
            return value
        print("Invalid value, try again")


def complete_optional_arguments(arguments: Arguments):
    if arguments.type is None:
        arguments.type = prompt(
            "What type of project do you want to create?",
            "Type ([e]xecutable / [h]eader-only / [s]hared)",
            "e",
            lambda v: v.lower() if v.lower() in ["e", "s", "h"] else None
        )
    if arguments.std is None:
        arguments.std = prompt(
            "What standard do you want to use?",
            "Standard (11 / 14 / 17 / 20)",
            "17",
            lambda v: v if v in ["11", "14", "17", "20"] else None
        )
    if arguments.package_manager is None:
        package_manager = prompt(
            "Do you want to use a package manager?",
            "Package manager ([c]onan / [v]cpkg / [n]one)",
            "n",
            lambda v: v.lower() if v.lower() in ["c", "v", "n"] else None
        )
        arguments.package_manager = package_manager if package_manager != "n" else None


def get_variables(arguments: Arguments) -> Variables():
    variables = Variables()
    variables.set_variable("name", os.path.basename(arguments.path))
    variables.set_variable("version", "0.1.0")
    variables.set_variable("std", arguments.std)
    variables.set_bool("conan", arguments.package_manager == "c")
    variables.set_bool("vcpkg", arguments.package_manager == "v")
    variables.set_bool("exe", arguments.type == "e")
    variables.set_bool("lib", arguments.type == "h" or arguments.type == "s")
    variables.set_bool("clang_tidy", arguments.clang_tidy)
    variables.set_bool("cppcheck", arguments.cppcheck)

    variables.set_variable("pm_name", "conan" if arguments.package_manager == "c" else "vcpkg")
    variables.set_variable("os", {"Windows": "win64", "Linux": "linux", "Darwin": "darwin"}.get(platform.system(), "unknown"))
    variables.set_variable("cpus", str(os.cpu_count()))
    variables.set_variable("cpp_std", arguments.std)
    variables.set_variable("msvc_cpp_std", "")
    variables.set_variable("uc_name", variables.value("name").upper().replace("-", "_"))
    variables.set_variable("description", "")
    variables.set_variable("homepage", "")
    variables.set_bool("pm", arguments.package_manager is not None)
    variables.set_bool("cpp", True)
    variables.set_bool("c", False)
    variables.set_bool("cmake_321", False)
    variables.set_bool("use_clang_tidy", arguments.clang_tidy)
    variables.set_bool("use_cppcheck", arguments.cppcheck)
    variables.set_bool("catch3", True)
    variables.set_bool("examples", False)
    variables.set_bool("cpp_std", True)
    variables.set_bool("msvc_cpp_std", True)
    variables.set_bool("header", arguments.type == "h")
    variables.set_bool("cpp_examples", False)
    variables.set_bool("c_examples", False)
    variables.set_bool("include_source", arguments.type == "e")
    variables.set_bool("c_header", arguments.type == "h")
    return variables


def create_project(arguments: Arguments):
    handle_directory_exists(arguments.path, arguments.overwrite)
    complete_optional_arguments(arguments)
    if not os.path.exists(arguments.path):
        os.mkdir(arguments.path)
    variables = get_variables(arguments)
    write_directory(arguments.path, variables, 'common')
    mapping = {"e": "executable", "h": "header", "s": "shared"}
    write_directory(arguments.path, variables, mapping[arguments.type])
    init_git(arguments.path)
