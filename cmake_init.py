from src.argument_parser import ArgumentParser
from src.create_project import create_project

__version__ = "0.40.8"


def main():
    argument_parser = ArgumentParser()
    argument_parser.add_arguments(__version__)
    arguments = argument_parser.parse()
    create_project(arguments)


if __name__ == "__main__":
    main()
