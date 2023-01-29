import argparse
import logging
import os
import sys

from automation_scripts.configuration import configuration_manager
from automation_scripts.configuration.project_configuration import ProjectConfiguration
from automation_scripts.toolkit.automation.automation_command import AutomationCommand
from automation_scripts.toolkit.python.python_package_builder import PythonPackageBuilder


logger = logging.getLogger("Main")


class DistributionCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        local_parser = subparsers.add_parser("distribution", help = "execute commands related to distribution")

        local_subparsers = local_parser.add_subparsers(title = "commands", metavar = "<command>")
        local_subparsers.required = True

        command_collection = [
            _SetupCommand,
            _PackageCommand,
        ]

        for command in command_collection:
            command_instance = command()
            command_parser = command_instance.configure_argument_parser(local_subparsers)
            command_parser.set_defaults(command_instance = command_instance)

        return local_parser


    def check_requirements(self) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        raise NotImplementedError("Run is not supported for a command group")


class _SetupCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        return subparsers.add_parser("setup", help = "setup the local packages for distribution")


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


class _PackageCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        return subparsers.add_parser("package", help = "create the distribution packages")


    def check_requirements(self) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        python_executable = sys.executable
        project_configuration: ProjectConfiguration = kwargs["configuration"]

        version = project_configuration.project_version.full_identifier
        output_directory = os.path.join("Artifacts", "Distributions")
        all_python_packages = configuration_manager.list_python_packages()

        python_package_builder = PythonPackageBuilder(python_executable)

        logger.info("Building python distribution packages")
        for python_package in all_python_packages:
            python_package_builder.build_distribution_package(python_package, version, output_directory, simulate = simulate)
