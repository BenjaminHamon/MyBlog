import logging
import subprocess
from typing import List, Optional


logger = logging.getLogger("Python")


def run_command(command: List[str], simulate: bool = False) -> None:
    logger.info("+ %s", " ".join(("'" + x + "'") if " " in x else x for x in command))

    if not simulate:
        process_result = subprocess.run(command, check = False, capture_output = True, text = True, encoding = "utf-8")
        for line in process_result.stdout.splitlines():
            logging.getLogger("Python").debug(line)
        for line in process_result.stderr.splitlines():
            logging.getLogger("Python").error(line)

        if process_result.returncode != 0:
            raise RuntimeError("Python command failed (ExitCode: %r)" % process_result.returncode)


def install_packages(python_executable: str, name_or_path_collection: List[str], python_package_repository: Optional[str] = None, simulate = False) -> None:

    def is_local_package(name_or_path: str) -> bool:
        return name_or_path.startswith(".")

    install_command = [ python_executable, "-m", "pip", "install", "--upgrade" ]
    install_command += [ "--extra-index", python_package_repository ] if python_package_repository is not None else []

    for name_or_path in name_or_path_collection:
        install_command += [ "--editable", name_or_path ] if is_local_package(name_or_path) else [ name_or_path ]

    run_command(install_command, simulate = simulate)
