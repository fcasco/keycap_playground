#!/usr/bin/env python3
import argparse
import logging
import sys
import tomllib
from pathlib import Path
from typing import Any

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


def load_config_file(config_path: Path | None) -> dict[str, Any]:
    """Load configuration from TOML file."""
    if not config_path:
        return {}

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    return config


def merge_config_with_args(
    config: dict[str, Any], args: argparse.Namespace
) -> argparse.Namespace:
    """Merge TOML configuration with command line arguments."""
    # Create a copy of args to modify
    merged_args = argparse.Namespace()

    # Copy all existing attributes from args
    for attr_name in dir(args):
        if not attr_name.startswith("_"):
            setattr(merged_args, attr_name, getattr(args, attr_name))

    # Override with config values (excluding the config parameter itself)
    config_copy = {k: v for k, v in config.items() if k != "config"}

    for key, value in config_copy.items():
        if hasattr(merged_args, key):
            setattr(merged_args, key, value)

    return merged_args


def make_args_parser():
    args_parser = argparse.ArgumentParser(description="Render a full set of riskeycap keycaps.")
    args_parser.add_argument(
        "-c",
        "--config",
        required=False,
        type=Path,
        help="Path to TOML configuration file",
    )
    args_parser.add_argument(
        "-f",
        "--force",
        required=False,
        action="store_true",
        help="Forcibly re-render keycaps even if they already exist.",
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
        "-k",
        "--keycaps",
        required=False,
        action="store_true",
        help="If True, prints out the names of all keycaps we can render.",
    )
    args_parser.add_argument(
        "-l",
        "--legends",
        required=False,
        action="store_true",
        help="If True, generate a separate set of files for legends.",
    )
    args_parser.add_argument(
        "--log-file",
        required=False,
        type=str,
        help="Path to log file (logs to console if not specified)",
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
        "-o",
        "--out",
        metavar="<filepath>",
        type=str,
        default=".",
        help="Where the generated files will go.",
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
        "names",
        nargs="*",
        metavar="name",
        help="Optional name of specific keycap you wish to render",
    )
    return args_parser


def main():
    args_parser = make_args_parser()
    args = args_parser.parse_args()

    # Load and merge TOML configuration if provided
    if args.config:
        try:
            config = load_config_file(args.config)
            args = merge_config_with_args(config, args)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error loading configuration: {e}", file=sys.stderr)
            sys.exit(1)

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
