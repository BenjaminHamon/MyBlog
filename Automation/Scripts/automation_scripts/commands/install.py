import argparse
import logging
import os
import sys

from automation_scripts.configuration import configuration_manager
from automation_scripts.configuration.project_configuration import ProjectConfiguration
from automation_scripts.configuration.python_package import PythonPackage
from automation_scripts.toolkit.automation.automation_command import AutomationCommand
from automation_scripts.toolkit.python import python_helpers


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

        logger.info("Generating python package metadata")
        for python_package in all_python_packages:
            _generate_package_metadata(project_configuration, python_package, simulate = simulate)

        logger.info("Installing project packages")
        python_helpers.install_packages(python_executable, [ "./Sources" ], simulate = simulate)


def _generate_package_metadata(project_configuration: ProjectConfiguration, python_package: PythonPackage, simulate: bool) -> None:
    metadata_file_path = os.path.join(python_package.path_to_sources, python_package.name_for_file_system, "__metadata__.py")

    metadata_content = ""
    metadata_content += "__copyright__ = \"%s\"\n" % project_configuration.copyright
    metadata_content += "__version__ = \"%s\"\n" % project_configuration.project_version.full_identifier
    metadata_content += "__date__ = \"%s\"\n" % (project_configuration.project_version.revision_date.replace(tzinfo = None).isoformat() + "Z")

    logger.debug("Writing '%s'", metadata_file_path)
    if not simulate:
        with open(metadata_file_path, mode = "w", encoding = "utf-8") as metadata_file:
            metadata_file.writelines(metadata_content)
