#!/usr/bin/env python3
import argparse

from . import keyplay


def make_args_parser():
    args_parser = argparse.ArgumentParser(
            description="Render a full set of riskeycap keycaps.")
    args_parser.add_argument("-o", "--out",
                             metavar="<filepath>", type=str, default=".",
                             help="Where the generated files will go.")
    args_parser.add_argument("-f", "--force",
                             required=False, action="store_true",
                             help="Forcibly re-render keycaps even if they already exist.")
    args_parser.add_argument("-l", "--legends",
                             required=False, action="store_true",
                             help="If True, generate a separate set of files for legends.")
    args_parser.add_argument("-t", "--file-type",
                             required=False, type=str, default="stl",
                             choices=["stl", "3mf"],
                             help="Output file type (default: stl, options: stl, 3mf)")
    args_parser.add_argument("-k", "--keycaps",
                             required=False, action="store_true",
                             help="If True, prints out the names of all keycaps we can render.")
    args_parser.add_argument("-j", "--max-processes",
                             required=False, type=int, default=2,
                             help="Maximum number of parallel OpenSCAD processes to run"
                             "(default: 2)")
    args_parser.add_argument("names",
                             nargs="*", metavar="name",
                             help="Optional name of specific keycap you wish to render")
    return args_parser


def main():
    args_parser = make_args_parser()
    args = args_parser.parse_args()

    if args.keycaps:
        keyplay.print_keycaps()
    else:
        keyplay.run(args)


if __name__ == "__main__":
    main()
