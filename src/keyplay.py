#!/usr/bin/env python3
"""
Generates a whole keyboard's worth of keycaps (and a few extras).

Fonts used by this script:
--------------------------

 * Gotham Rounded:style=Bold
 * Arial Black:style=Regular
 * Aharoni
 * FontAwesome
 * Font Awesome 6 Free:style=Solid
 * Hack
 * Material Design Icons:style=Regular
 * Code2000
 * Agave
 * DejaVu Sans:style=Bold
 * Noto
"""

import asyncio
import functools
import logging
import os
import subprocess
from collections.abc import Sequence
from copy import deepcopy
from typing import Any

from src.riskeycap import KEYCAPS

logger = logging.getLogger(__name__)


def run_command(cmd: str) -> str:
    """
    Run prepared behave command in shell and return its output.
    :param cmd: Well-formed behave command to run.
    :return: Command output as string.
    """
    logger.debug(f"Running {cmd}")
    try:
        output = subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=True,
            cwd=os.getcwd(),
        )
    except subprocess.CalledProcessError as e:
        logger.exception(f"Error running {cmd}\n{e}")
        output = e.output

    return output


async def run_command_on_loop(loop: asyncio.AbstractEventLoop, command: str, semaphore) -> str:
    """
    Run test for one particular feature, check its result and return report.
    :param loop: Loop to use.
    :param command: Command to run.
    :return: Result of the command.
    """
    logger.debug("Starting commands loop")
    async with semaphore:
        runner = functools.partial(run_command, command)
        output = await loop.run_in_executor(None, runner)
        await asyncio.sleep(1)  # Slowing a bit for demonstration purposes
        return output


async def process_result(result: Any):  # noqa:RUF029
    """
    Do something useful with result of the commands
    """
    logger.debug(f"Processing command result: {result}")


async def run_all_commands(semaphore, commands: Sequence[str]) -> None:
    """
    Run all commands in a list
    :param commands: List of commands to run.
    """
    logger.debug("Running all commands")
    loop = asyncio.get_event_loop()
    fs = [run_command_on_loop(loop, command, semaphore) for command in commands]
    results = []
    for f in asyncio.as_completed(fs):
        result = await f
        results.append(asyncio.ensure_future(process_result(result)))

    logger.info("All commands completed")
    logger.debug(f"{results=}")


def print_keycaps():
    """
    Prints the names of all keycaps in KEYCAPS.
    """
    keycap_names = ", ".join(a.name for a in KEYCAPS)
    logger.info(f"Here's all the keycaps we can render:\n{keycap_names}")


def should_skip_file(output_path, name, file_type, force):
    """Check if a file should be skipped based on existence and force flag."""
    file_path = f"{output_path}/{name}.{file_type}"
    if not force and os.path.exists(file_path):
        logger.info(f"{file_path} exists; skipping...")
        return True
    return False


def make_keycap_command(keycap, output_path, file_type, force):
    """Make a command for a keycap to the commands list."""
    keycap.output_path = output_path
    keycap.file_type = file_type

    if should_skip_file(output_path, keycap.name, file_type, force):
        return

    logger.info(f"Rendering {output_path}/{keycap.name}.{file_type}...")
    logger.debug(f"Keycap details: {keycap}")
    return str(keycap)


def make_legend_command(keycap, output_path, force):
    """Add a command for keycap legends to the commands list."""
    if keycap.legends == [""]:
        return

    legend_name = f"{keycap.name}_legends"
    legend_file_type = "stl"  # Always use STL for legends

    if should_skip_file(output_path, legend_name, legend_file_type, force):
        return

    legend = deepcopy(keycap)

    legend.name = legend_name
    legend.output_path = output_path
    legend.render = ["legends"]
    legend.file_type = legend_file_type

    logger.info(f"Rendering {output_path}/{legend.name}.{legend_file_type}...")
    logger.debug(f"Legend details: {legend}")
    return str(legend)


def process_specific_keycaps(args):
    """Process commands for specific keycap names."""
    commands = []

    for name in args.names:
        name_found = False
        for keycap in KEYCAPS:
            if keycap.name.lower() == name.lower():
                name_found = True
                new_command = make_keycap_command(keycap, args.out, args.file_type, args.force)
                if new_command:
                    commands.append(new_command)

                if args.legends:
                    new_command = make_legend_command(keycap, args.out, args.force)
                    if new_command:
                        commands.append(new_command)
                break

        if not name_found:
            logger.warning(f"Could not find a keycap named {name}")

    return commands


def process_all_keycaps(args):
    """Process commands for all keycaps."""
    commands = []
    for keycap in KEYCAPS:
        new_command = make_keycap_command(keycap, args.out, args.file_type, args.force)
        if new_command:
            commands.append(new_command)

        if args.legends:
            new_command = make_legend_command(keycap, args.out, args.force)
            if new_command:
                commands.append(new_command)

    return commands


def make_commands(args):
    """Returns a list of commands to generate the keycaps using OpenSCAD"""
    if args.names:
        commands = process_specific_keycaps(args)
    else:
        commands = process_all_keycaps(args)

    return commands


def run(args):
    logger.info(f"Outputting to: {args.out}")

    commands = make_commands(args)
    semaphore = asyncio.Semaphore(args.max_processes)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_all_commands(semaphore=semaphore, commands=commands))
