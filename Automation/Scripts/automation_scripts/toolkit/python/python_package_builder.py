import logging
import os
import re
import shutil

from automation_scripts.toolkit.automation.project_version import ProjectVersion
from automation_scripts.toolkit.processes.executable_command import ExecutableCommand
from automation_scripts.toolkit.python import python_helpers
from automation_scripts.toolkit.python.python_package import PythonPackage


logger = logging.getLogger("Python")


class PythonPackageBuilder:


    def __init__(self, python_executable: str) -> None:
        self._python_executable = python_executable


    def generate_package_metadata(self,
            project_version: ProjectVersion, copyright_text: str, python_package: PythonPackage, simulate: bool = False) -> None:

        metadata_file_path = os.path.join(python_package.path_to_sources, python_package.name_for_file_system, "__metadata__.py")

        metadata_content = ""
        metadata_content += "__version__ = \"%s\"\n" % project_version.full_identifier
        metadata_content += "__date__ = \"%s\"\n" % (project_version.revision_date.replace(tzinfo = None).isoformat() + "Z")
        metadata_content += "__copyright__ = \"%s\"\n" % copyright_text

        logger.debug("Writing '%s'", metadata_file_path)
        if not simulate:
            with open(metadata_file_path, mode = "w", encoding = "utf-8") as metadata_file:
                metadata_file.writelines(metadata_content)


    def build_distribution_package(self,
            python_package: PythonPackage, version: str, output_directory: str, simulate: bool = False):

        setup_command = ExecutableCommand(self._python_executable)
        setup_command.add_arguments([ "setup.py", "bdist_wheel" ])

        python_helpers.run_command(setup_command, working_directory = python_package.path_to_sources, simulate = simulate)

        archive_name = python_package.name_for_file_system + "-" + version
        source_path = os.path.join(python_package.path_to_sources, "dist", archive_name + "-py3-none-any.whl")
        destination_path = os.path.join(output_directory, archive_name + "-py3-none-any.whl")

        if not simulate:
            os.makedirs(os.path.dirname(destination_path), exist_ok = True)
            shutil.copyfile(source_path, destination_path + ".tmp")
            os.replace(destination_path + ".tmp", destination_path)

        logger.debug("Distribution package path: '%s'", destination_path)


    def copy_distribution_package_for_release(self, # pylint: disable = too-many-arguments
            python_package: PythonPackage, version: str, version_for_release: str, distribution_directory: str, simulate: bool = False):

        archive_name = python_package.name_for_file_system + "-" + version
        archive_name_for_release = python_package.name_for_file_system + "-" + version_for_release
        source_path = os.path.join(distribution_directory, archive_name + "-py3-none-any.whl")
        destination_path = os.path.join(distribution_directory, archive_name_for_release + "-py3-none-any.whl")

        if not simulate:
            archive_staging_directory = os.path.join(destination_path + ".staging")
            if os.path.exists(archive_staging_directory):
                shutil.rmtree(archive_staging_directory)

            shutil.unpack_archive(source_path, archive_staging_directory, "zip")
            os.rename(os.path.join(archive_staging_directory, archive_name + ".dist-info"),
                os.path.join(archive_staging_directory, archive_name_for_release + ".dist-info"))

            metadata_file_path = os.path.join(archive_staging_directory, archive_name_for_release + ".dist-info", "METADATA")
            self.update_metadata(metadata_file_path, "Version", version_for_release)

            if os.path.exists(destination_path):
                os.remove(destination_path)

            logger.debug("Writing '%s'", destination_path)
            shutil.make_archive(destination_path + ".tmp", "zip", archive_staging_directory)
            os.replace(destination_path + ".tmp.zip", destination_path)
            shutil.rmtree(archive_staging_directory)

        logger.debug("Distribution package path: '%s'", destination_path)


    def update_metadata(self, metadata_file_path: str, key: str, value: str) -> None:
        with open(metadata_file_path, mode = "r", encoding = "utf-8") as metadata_file:
            metadata = metadata_file.read()

        metadata = re.sub(r"^" + re.escape(key) + r": .*$", key + ": " + value, metadata, flags = re.MULTILINE)

        with open(metadata_file_path, mode = "w", encoding = "utf-8") as metadata_file:
            metadata_file.write(metadata)
