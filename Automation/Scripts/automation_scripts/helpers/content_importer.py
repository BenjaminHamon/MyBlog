import datetime
import filecmp
import glob
import logging
import os
import re
from typing import List, Tuple

import markdown
import yaml

from automation_scripts.helpers.content_item import ContentItem
from automation_scripts.helpers.document_metadata import DocumentMetadata
from automation_scripts.helpers.index_item import IndexItem
from automation_scripts.helpers.yaml_dumper import YamlDumper


logger = logging.getLogger("ContentImporter")


class ContentImporter:


    def import_articles(self, source_directory: str, destination_directory: str, now: datetime.datetime, simulate: bool = False) -> None:
        all_content_items = self.load_content_items(source_directory, now)

        self.write_index(destination_directory, [ content_item.index for content_item in all_content_items ], simulate = simulate)
        self.write_metadata(destination_directory, [ content_item.metadata for content_item in all_content_items ], simulate = simulate)
        self.write_text(destination_directory, all_content_items, simulate = simulate)


    def merge_metadata(self, old_directory: str, new_directory: str, simulate: bool = False) -> None:
        old_index = self.read_index(old_directory)
        new_index = self.read_index(new_directory)

        for new_item in new_index:
            old_item = next((x for x in old_index if x.identifier == new_item.identifier), None)
            if old_item is None:
                continue

            new_item.aliases = list(set(old_item.aliases + new_item.aliases))

        self.write_index(new_directory, new_index, simulate = simulate)

        old_metadata = self.read_metadata(old_directory)
        new_metadata = self.read_metadata(new_directory)

        for new_item in new_metadata:
            old_item = next((x for x in old_metadata if x.identifier == new_item.identifier), None)
            if old_item is None:
                continue

            new_item.creation_date = old_item.creation_date

            if old_item.reference is None or new_item.reference is None:
                raise ValueError("Content item reference is none")

            old_text_file_path = os.path.join(old_directory, old_item.reference + ".html")
            new_text_file_path = os.path.join(new_directory, new_item.reference + ".html")
            document_changed = not filecmp.cmp(old_text_file_path, new_text_file_path)

            if not document_changed:
                new_item.update_date = old_item.update_date

        self.write_metadata(new_directory, new_metadata, simulate = simulate)


    def load_content_items(self, source_directory: str, now: datetime.datetime) -> List[ContentItem]:
        if not os.path.exists(source_directory):
            raise FileNotFoundError("Source directory does not exist: '%s'" % source_directory)

        all_content_items: List[ContentItem] = []

        for file_entry in glob.glob(os.path.join(source_directory, "*")):
            with open(file_entry, mode = "r", encoding = "utf-8") as article_file:
                article_raw_text = article_file.read()

            article_metadata, article_text = self.parse_document(article_raw_text)
            article_metadata.reference = self._sanitize_for_file_name(article_metadata.title)
            article_metadata.creation_date = now
            article_metadata.update_date = now

            index_item = IndexItem(
                identifier = article_metadata.identifier,
                reference = article_metadata.reference,
                aliases = [ article_metadata.reference ],
            )

            all_content_items.append(ContentItem(index_item, article_metadata, article_text))

        return all_content_items


    def parse_document(self, document_raw_text: str) -> Tuple[DocumentMetadata, str]:
        document_raw_lines = document_raw_text.lstrip().splitlines()

        if document_raw_lines[0] != "---":
            raise ValueError("Document has no YAML header")

        try:
            yaml_end_index = document_raw_lines.index("---", 1)
        except ValueError as exception:
            raise ValueError("Document has an invalid YAML header") from exception

        yaml_header = "\n".join(document_raw_lines[1 : yaml_end_index]).strip()
        document_metadata_from_yaml: dict = yaml.safe_load(yaml_header)

        try:
            document_metadata = DocumentMetadata(
                identifier = document_metadata_from_yaml["Identifier"],
                reference = None,
                title = document_metadata_from_yaml["Title"],
                tags = document_metadata_from_yaml.get("Tags", []),
                warnings = document_metadata_from_yaml.get("Warnings", []),
                excerpt = document_metadata_from_yaml.get("Excerpt", []),
            )
        except KeyError as exception:
            raise KeyError("Missing metadata field: '%s'" % exception.args[0]) from exception

        document_text = "\n".join(document_raw_lines[yaml_end_index + 1 :]).strip()

        return (document_metadata, document_text)


    def read_index(self, content_directory: str) -> List[IndexItem]:
        index_file_path = os.path.join(content_directory, "Index.yaml")

        with open(index_file_path, mode = "r", encoding = "utf-8") as index_file:
            index_from_serialization: List[dict] = yaml.safe_load(index_file)

        index: List[IndexItem] = []
        for index_item_as_dict in index_from_serialization:
            index.append(IndexItem(**index_item_as_dict))

        return index


    def read_metadata(self, content_directory: str) -> List[DocumentMetadata]:
        metadata_file_path = os.path.join(content_directory, "Metadata.yaml")

        with open(metadata_file_path, mode = "r", encoding = "utf-8") as metadata_file:
            metadata_from_serialization: List[dict] = yaml.safe_load(metadata_file)

        all_metadata: List[DocumentMetadata] = []
        for metadata_as_dict in metadata_from_serialization:
            all_metadata.append(DocumentMetadata(**metadata_as_dict))

        return all_metadata


    def write_index(self, destination_directory: str, all_index_items: List[IndexItem], simulate: bool = False) -> None:
        index_for_serialization = [ index_item.__dict__ for index_item in all_index_items ]
        index_file_path = os.path.join(destination_directory, "Index.yaml")

        logger.debug("Writing '%s'", index_file_path)

        if not simulate:
            with open(index_file_path, mode = "w", encoding = "utf-8") as index_file:
                yaml.dump(index_for_serialization, index_file, Dumper = YamlDumper, sort_keys = False)


    def write_metadata(self, destination_directory: str, all_metadata: List[DocumentMetadata], simulate: bool = False) -> None:
        metadata_for_serialization = [ metadata.__dict__ for metadata in all_metadata ]
        metadata_file_path = os.path.join(destination_directory, "Metadata.yaml")

        logger.debug("Writing '%s'", metadata_file_path)

        if not simulate:
            with open(metadata_file_path, mode = "w", encoding = "utf-8") as metadata_file:
                yaml.dump(metadata_for_serialization, metadata_file, Dumper = YamlDumper, sort_keys = False)


    def write_text(self, destination_directory: str, all_content_items: List[ContentItem], simulate: bool = False) -> None:
        for content_item in all_content_items:
            html_file_path = os.path.join(destination_directory, content_item.index.reference + ".html")
            article_as_html = markdown.markdown(content_item.text)

            logger.debug("Writing '%s'", html_file_path)

            if not simulate:
                with open(html_file_path, mode = "w", encoding = "utf-8") as html_file:
                    html_file.write(article_as_html)


    def _sanitize_for_file_name(self, title: str) -> str:
        return re.sub(r"[^a-zA-Z0-9\.\-_']", "_", title)
