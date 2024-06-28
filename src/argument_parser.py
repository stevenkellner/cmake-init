import argparse
import os
from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class Arguments:
    path: str
    type: Optional[Literal["e", "h", "s"]]
    std: Optional[Literal["11", "14", "17", "20"]]
    clang_tidy: bool
    cppcheck: bool
    package_manager: Optional[Literal["c", "v"]]
    overwrite: bool


class ArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super().__init__(
            prog="cmake-init",
            description=__doc__,
            add_help=False,
        )

    def add_arguments(self, version: str):
        self.add_argument(
            "--help",
            action="help",
            help="show this help message and exit"
        )
        self.add_argument(
            "--version",
            action="version",
            version=version
        )
        self.add_argument(
            "path",
            type=os.path.realpath,
            help="path to generate to, the name is also derived from this"
        )
        self.add_argument(
            "-t", "--type",
            choices=["e", "h", "s"],
            help="Type of the project to generate, e for executable, h for header-only library, "
                 "s for static / shared library"
        )
        self.add_argument(
            "--std",
            choices=["11", "14", "17", "20"],
            help="The language standard to use"
        )
        self.add_argument(
            "--clang-tidy",
            action="store_true",
            help="Add clang-tidy to the project, defaults to true"
        )
        self.add_argument(
            "--cppcheck",
            action="store_true",
            help="Add cppcheck to the project, defaults to true"
        )
        self.add_argument(
            "-p", "--package-manager",
            choices=["c", "v"],
            help="Package manager to use, c for conan, v for vcpkg"
        )
        self.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing files, defaults to false",
            default=False
        )

    def parse(self) -> Arguments:
        args = self.parse_args()
        return Arguments(
            path=args.path,
            type=args.type,
            std=args.std,
            clang_tidy=args.clang_tidy,
            cppcheck=args.cppcheck,
            package_manager=args.package_manager,
            overwrite=args.overwrite
        )
