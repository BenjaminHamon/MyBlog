import argparse
import logging
import os
import platform
import shutil
import subprocess
import sys
from typing import List

import helpers # pylint: disable = import-error


logger = logging.getLogger("Main")


def main() -> None:

    # Prevent active pyvenv from overriding a python executable specified in a command
    if "__PYVENV_LAUNCHER__" in os.environ:
        del os.environ["__PYVENV_LAUNCHER__"]

    with helpers.execute_in_workspace(__file__):
        arguments = parse_arguments()
        configure_logging(arguments.verbosity)

        if arguments.simulate:
            logger.info("(( The script is running as a simulation ))")
        logger.info("Setting up local workspace (Path: %s)", os.getcwd())

        python_system_executable = helpers.find_and_check_system_python_executable()
        setup_virtual_environment(python_system_executable, simulate = arguments.simulate)


def parse_arguments() -> argparse.Namespace:
    all_log_levels = [ "debug", "info", "warning", "error", "critical" ]

    main_parser = argparse.ArgumentParser()
    main_parser.add_argument("--simulate", action = "store_true",
        help = "perform a test run, without writing changes")
    main_parser.add_argument("--verbosity", choices = all_log_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(all_log_levels))

    return main_parser.parse_args()


def configure_logging(verbosity: str) -> None:
    logging.basicConfig(
        level = logging.getLevelName(verbosity.upper()),
        format = "[{levelname}][{name}] {message}",
        datefmt = "%Y-%m-%dT%H:%M:%S",
        style = "{")


def setup_virtual_environment(python_system_executable: str, simulate: bool) -> None:
    logger.info("Setting up python virtual environment")

    venv_python_executable = os.path.realpath(".venv/scripts/python.exe" if platform.system() == "Windows" else ".venv/bin/python")
    if sys.executable.lower() == venv_python_executable.lower():
        raise RuntimeError("Active python is the target virtual environment")

    if os.path.isdir(".venv") and not simulate:
        shutil.rmtree(".venv")

    run_python_command([ python_system_executable, "-m", "venv", ".venv" ], simulate = simulate)

    if platform.system() in [ "Darwin", "Linux" ] and not os.path.exists(".venv/scripts") and not simulate:
        os.symlink("bin", ".venv/scripts")

    run_python_command([ ".venv/scripts/python", "-m", "pip", "install", "--upgrade", "pip", "wheel" ], simulate = simulate)
    run_python_command([ ".venv/scripts/python", "-m", "pip", "install", "--upgrade", "--editable", "Automation/Scripts[dev]" ], simulate = simulate)


def run_python_command(command: List[str], simulate: bool) -> None:
    logger.info("+ %s", " ".join(command))

    if not simulate:
        process_result = subprocess.run(command, check = False, capture_output = True, text = True, encoding = "utf-8")
        for line in process_result.stdout.splitlines():
            logging.getLogger("Python").debug(line)
        for line in process_result.stderr.splitlines():
            logging.getLogger("Python").error(line)

        if process_result.returncode != 0:
            raise RuntimeError("Python command failed (ExitCode: %r)" % process_result.returncode)


if __name__ == "__main__":
    try:
        main()
    except Exception: # pylint: disable = broad-except
        logger.error("Script failed", exc_info = True)
        sys.exit(1)
