import logging
import subprocess
from typing import List, Optional

from automation_scripts.toolkit.processes import process_helpers
from automation_scripts.toolkit.processes.executable_command import ExecutableCommand


logger = logging.getLogger("Python")


def install_packages(python_executable: str,
        name_or_path_collection: List[str], python_package_repository: Optional[str] = None, simulate: bool = False) -> None:

    def is_local_package(name_or_path: str) -> bool:
        return name_or_path.startswith(".")

    install_command = ExecutableCommand(python_executable)
    install_command.add_arguments([ "-m", "pip", "install", "--upgrade" ])

    if python_package_repository is not None:
        install_command.add_arguments([ "--extra-index", python_package_repository ])

    for name_or_path in name_or_path_collection:
        install_command.add_arguments([ "--editable", name_or_path ] if is_local_package(name_or_path) else [ name_or_path ])

    run_command(install_command, simulate = simulate)


def run_command(command: ExecutableCommand, working_directory: Optional[str] = None, simulate: bool = False) -> None:
    logger.info("+ %s", process_helpers.format_executable_command(command.get_command_for_logging()))

    subprocess_options = {
        "cwd": working_directory,
        "capture_output": True,
        "text": True,
        "encoding": "utf-8",
        "stdin": subprocess.DEVNULL,
    }

    if not simulate:
        process_result = subprocess.run(command.get_command(), check = False, **subprocess_options)
        for line in process_result.stdout.splitlines():
            logger.debug(line)
        for line in process_result.stderr.splitlines():
            logger.error(line)

        if process_result.returncode != 0:
            raise RuntimeError("Python command failed (ExitCode: %r)" % process_result.returncode)
