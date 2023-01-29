import argparse
import logging
import sys

from automation_scripts.configuration import configuration_manager
from automation_scripts.configuration.project_configuration import ProjectConfiguration
from automation_scripts.toolkit.automation.automation_command import AutomationCommand
from automation_scripts.toolkit.python import python_helpers
from automation_scripts.toolkit.python.python_package_builder import PythonPackageBuilder


logger = logging.getLogger("Main")


class InstallCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        return subparsers.add_parser("install", help = "install python packages to local environment")


    def check_requirements(self) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        python_executable = sys.executable
        project_configuration: ProjectConfiguration = kwargs["configuration"]
        all_python_packages = configuration_manager.list_python_packages()

        python_package_builder = PythonPackageBuilder(python_executable)

        logger.info("Generating python package metadata")
        for python_package in all_python_packages:
            python_package_builder.generate_package_metadata(
                project_configuration.project_version, project_configuration.copyright, python_package, simulate = simulate)

        logger.info("Installing project packages")
        python_helpers.install_packages(python_executable, [ "./Sources" ], simulate = simulate)
