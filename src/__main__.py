#!/usr/bin/env python3
import argparse
import logging
import sys

from . import keyplay


def setup_logging(log_level: str, log_file: str | None) -> None:
    """Configure logging based on command line arguments."""
    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def make_args_parser():
    args_parser = argparse.ArgumentParser(description="Render a full set of riskeycap keycaps.")
    args_parser.add_argument(
        "-o",
        "--out",
        metavar="<filepath>",
        type=str,
        default=".",
        help="Where the generated files will go.",
    )
    args_parser.add_argument(
        "-f",
        "--force",
        required=False,
        action="store_true",
        help="Forcibly re-render keycaps even if they already exist.",
    )
    args_parser.add_argument(
        "-l",
        "--legends",
        required=False,
        action="store_true",
        help="If True, generate a separate set of files for legends.",
    )
    args_parser.add_argument(
        "-t",
        "--file-type",
        required=False,
        type=str,
        default="stl",
        choices=["stl", "3mf"],
        help="Output file type (default: stl, options: stl, 3mf)",
    )
    args_parser.add_argument(
        "-k",
        "--keycaps",
        required=False,
        action="store_true",
        help="If True, prints out the names of all keycaps we can render.",
    )
    args_parser.add_argument(
        "-j",
        "--max-processes",
        required=False,
        type=int,
        default=2,
        help="Maximum number of parallel OpenSCAD processes to run(default: 2)",
    )
    args_parser.add_argument(
        "--log-level",
        required=False,
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set the logging level (default: INFO)",
    )
    args_parser.add_argument(
        "--log-file",
        required=False,
        type=str,
        help="Path to log file (logs to console if not specified)",
    )
    args_parser.add_argument(
        "names",
        nargs="*",
        metavar="name",
        help="Optional name of specific keycap you wish to render",
    )
    return args_parser


def main():
    args_parser = make_args_parser()
    args = args_parser.parse_args()

    # Set up logging before any other operations
    try:
        setup_logging(args.log_level, args.log_file)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.keycaps:
        keyplay.print_keycaps()
    else:
        keyplay.run(args)


if __name__ == "__main__":
    main()
