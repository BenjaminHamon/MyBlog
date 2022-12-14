import contextlib
import os
import platform
import shutil
from typing import Generator, Optional


@contextlib.contextmanager
def execute_in_workspace(script_path: str) -> Generator[None,None,None]:
    current_directory = os.getcwd()
    workspace_directory = resolve_workspace_root(script_path)

    os.chdir(workspace_directory)

    try:
        yield
    finally:
        os.chdir(current_directory)


def resolve_workspace_root(script_path: str) -> str:
    directory = os.path.dirname(os.path.realpath(script_path))

    while True:
        if os.path.isdir(os.path.join(directory, ".git")):
            return directory
        if os.path.dirname(directory) == directory:
            raise RuntimeError("Failed to resolve the workspace root")
        directory = os.path.dirname(directory)


def find_and_check_system_python_executable() -> str:
    python_executable = find_system_python_executable()
    if python_executable is None or not shutil.which(python_executable):
        raise RuntimeError("Python3 is required (Path: %r)" % python_executable)

    return python_executable


def find_system_python_executable() -> Optional[str]:
    all_supported_versions = [ "3.7", "3.8", "3.9" ]

    if platform.system() == "Linux":
        return "/usr/bin/python3"

    if platform.system() == "Windows":
        possible_paths = []

        for version in all_supported_versions:
            possible_paths += [
                os.path.join(os.environ["SystemDrive"] + "\\", "Python%s" % version.replace(".", ""), "python.exe"),
                os.path.join(os.environ["ProgramFiles"], "Python%s" % version.replace(".", ""), "python.exe"),
            ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        return None

    raise ValueError("Unsupported platform: '%s'" % platform.system())
