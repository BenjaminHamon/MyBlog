import argparse
import datetime
import logging
import os
import shutil

from automation_scripts.helpers.content_importer import ContentImporter
from automation_scripts.toolkit.automation.automation_command import AutomationCommand


logger = logging.getLogger("Main")


class UpdateContentCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = subparsers.add_parser("update-content", help = "generate content indexes")
        parser.add_argument("--source", required = True, help = "set the source directory for the content")
        return parser


    def check_requirements(self) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        source_directory: str = arguments.source

        if not os.path.exists(source_directory):
            raise FileNotFoundError("Source directory does not exist: '%s'" % source_directory)

        destination_directory = "Content"
        now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond = 0)
        content_importer = ContentImporter()

        if not simulate:
            if os.path.exists(destination_directory + ".tmp"):
                shutil.rmtree(destination_directory + ".tmp")
            os.makedirs(destination_directory + ".tmp")

        if not simulate:
            os.makedirs(os.path.join(destination_directory + ".tmp", "Articles"))

        content_importer.import_articles(
            source_directory = os.path.join(source_directory, "Articles"),
            destination_directory = os.path.join(destination_directory + ".tmp", "Articles"),
            now = now,
            simulate = simulate)

        if os.path.exists(destination_directory):
            content_importer.merge_metadata(
                old_directory = os.path.join(destination_directory, "Articles"),
                new_directory = os.path.join(destination_directory + ".tmp", "Articles"),
                simulate = simulate)

        if not simulate:
            if os.path.exists(destination_directory):
                shutil.rmtree(destination_directory)
            os.rename(destination_directory + ".tmp", destination_directory)
