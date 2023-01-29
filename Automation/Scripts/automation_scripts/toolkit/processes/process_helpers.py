import shlex
from typing import List


def format_executable_command(command: List[str]):
    return " ".join(format_executable_command_element(element) for element in command)


def format_executable_command_element(element: str) -> str:
    return shlex.quote(element)
