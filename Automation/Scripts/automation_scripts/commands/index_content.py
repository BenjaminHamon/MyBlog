import argparse
import glob
import logging
import os
import re
from typing import List

import yaml

from bhamon_blog.content.document_metadata import DocumentMetadata
from bhamon_blog.content.exceptions.invalid_content_exception import InvalidContentException

from automation_scripts.toolkit.automation.automation_command import AutomationCommand


logger = logging.getLogger("Main")


class IndexContentCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = subparsers.add_parser("index-content", help = "generate content indexes")
        parser.add_argument("--content-directory", required = True, help = "set the source directory for the content")
        return parser


    def check_requirements(self) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        content_directory: str = arguments.content_directory

        if not os.path.exists(content_directory):
            raise FileNotFoundError("Content directory does not exist: '%s'" % content_directory)

        if os.path.exists(os.path.join(content_directory, "Articles")):
            index_file_path = os.path.join(content_directory, "Articles", "Index.yaml")
            content_index = _generate_index(os.path.join(content_directory, "Articles"))

            if not simulate:
                with open(index_file_path, mode = "w", encoding = "utf-8") as index_file:
                    yaml.safe_dump(content_index, index_file, sort_keys = False)


def _generate_index(content_directory: str) -> List[dict]:
    content_index = []
    identifier_set = set()

    for document_file_path in glob.glob(os.path.join(content_directory, "*.md")):
        with open(document_file_path, mode = "r", encoding = "utf-8") as document_file:
            document_raw_text = document_file.read()

        metadata = _get_document_metadata(document_raw_text)

        if metadata.identifier in identifier_set:
            raise ValueError("Identifier '%s' is used by several documents" % metadata.identifier)

        reference = re.sub(r"\.md$", "", os.path.basename(document_file_path))

        index_item = {
            "Identifier": metadata.identifier,
            "Reference": reference,
            "Aliases": [ reference ],
        }

        identifier_set.add(metadata.identifier)
        content_index.append(index_item)

    return content_index


def _get_document_metadata(document_raw_text: str) -> DocumentMetadata:
    document_raw_lines = document_raw_text.lstrip().splitlines()

    if document_raw_lines[0] != "---":
        raise InvalidContentException("Document has no YAML header")

    try:
        yaml_end_index = document_raw_lines.index("---", 1)
    except ValueError as exception:
        raise InvalidContentException("Document has an invalid YAML header") from exception

    yaml_header = "\n".join(document_raw_lines[1 : yaml_end_index]).strip()
    document_metadata_from_yaml: dict = yaml.safe_load(yaml_header)

    try:
        return DocumentMetadata(
            identifier = document_metadata_from_yaml["Identifier"],
            title = document_metadata_from_yaml["Title"],
            tags = document_metadata_from_yaml.get("Tags", []),
            warnings = document_metadata_from_yaml.get("Warnings", []),
            excerpt = document_metadata_from_yaml.get("Excerpt", []),
        )
    except KeyError as exception:
        raise InvalidContentException("Missing metadata field: '%s'" % exception.args[0]) from exception
