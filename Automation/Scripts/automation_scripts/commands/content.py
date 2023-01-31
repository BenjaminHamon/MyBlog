import argparse
import datetime
import logging
import os
import shutil

from automation_scripts.configuration.project_configuration import ProjectConfiguration
from automation_scripts.configuration.project_environment import ProjectEnvironment
from automation_scripts.helpers.content_importer import ContentImporter
from automation_scripts.toolkit.automation.automation_command import AutomationCommand
from automation_scripts.toolkit.automation.automation_command_group import AutomationCommandGroup
from automation_scripts.toolkit.security.interactive_credentials_provider import InteractiveCredentialsProvider
from automation_scripts.toolkit.web.web_client import WebClient


logger = logging.getLogger("Main")


class ContentCommand(AutomationCommandGroup):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        local_parser: argparse.ArgumentParser = subparsers.add_parser("content", help = "execute commands related to content")

        command_collection = [
            _ClearCommand,
            _PackageCommand,
            _UpdateCommand,
            _UploadCommand,
        ]

        self.add_commands(local_parser, command_collection)

        return local_parser


    def check_requirements(self) -> None:
        pass


class _ClearCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        return subparsers.add_parser("clean", help = "clear local content")


    def check_requirements(self) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        local_content_directory = "Content"

        if not simulate:
            if os.path.exists(local_content_directory):
                shutil.rmtree(local_content_directory)
            os.makedirs(local_content_directory)


class _PackageCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        return subparsers.add_parser("package", help = "create a content package from local content")


    def check_requirements(self) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        project_configuration: ProjectConfiguration = kwargs["configuration"]

        local_content_directory = "Content"
        artifact_path = get_artifact_path(project_configuration)

        logger.info("Creating content package for '%s'", project_configuration.content_identifier)
        logger.debug("Writing '%s'", artifact_path)
        shutil.make_archive(artifact_path + ".tmp", "zip", local_content_directory, dry_run = simulate)
        if not simulate:
            os.replace(artifact_path + ".tmp.zip", artifact_path + ".zip")


class _UpdateCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = subparsers.add_parser("update", help = "update local content by importing from a content source")
        parser.add_argument("--source", required = True, help = "set the source directory for the content")
        return parser


    def check_requirements(self) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        source_directory: str = arguments.source

        if not os.path.exists(source_directory):
            raise FileNotFoundError("Source directory does not exist: '%s'" % source_directory)

        local_content_directory = "Content"
        now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond = 0)
        content_importer = ContentImporter()

        if not simulate:
            if os.path.exists(local_content_directory + ".tmp"):
                shutil.rmtree(local_content_directory + ".tmp")
            os.makedirs(local_content_directory + ".tmp")

        if not simulate:
            os.makedirs(os.path.join(local_content_directory + ".tmp", "Articles"))

        content_importer.import_articles(
            source_directory = os.path.join(source_directory, "Articles"),
            destination_directory = os.path.join(local_content_directory + ".tmp", "Articles"),
            now = now,
            simulate = simulate)

        if os.path.exists(local_content_directory):
            content_importer.merge_metadata(
                old_directory = os.path.join(local_content_directory, "Articles"),
                new_directory = os.path.join(local_content_directory + ".tmp", "Articles"),
                simulate = simulate)

        if not simulate:
            if os.path.exists(local_content_directory):
                shutil.rmtree(local_content_directory)
            os.rename(local_content_directory + ".tmp", local_content_directory)


class _UploadCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        return subparsers.add_parser("upload", help = "upload a content package to the content repository")


    def check_requirements(self) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        project_environment: ProjectEnvironment = kwargs["environment"]
        project_configuration: ProjectConfiguration = kwargs["configuration"]

        archive_path = get_artifact_path(project_configuration) + ".zip"
        repository_url = project_environment.get_application_content_repository_url() + "/" + project_configuration.project_identifier
        archive_remote_url = repository_url + "/" + os.path.basename(archive_path)

        credentials_provider = InteractiveCredentialsProvider()
        credentials = credentials_provider.get_credentials(repository_url)
        web_client = WebClient(authentication = (credentials.username, credentials.secret))

        logger.info("Uploading content package for '%s'", project_configuration.content_identifier)
        if not simulate:
            web_client.upload_file(archive_remote_url, archive_path)


def get_artifact_path(project_configuration: ProjectConfiguration) -> str:
    artifact_parameters = project_configuration.get_artifact_default_parameters()
    artifact_parameters["content"] = project_configuration.content_identifier
    artifact_name = "{project}_{version}+{revision}_Content_{content}".format(**artifact_parameters)
    return os.path.join("Artifacts", "Content", artifact_name)
