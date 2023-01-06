import os
from typing import List

import yaml

from bhamon_blog.content.document import Document
from bhamon_blog.content.document_metadata import DocumentMetadata
from bhamon_blog.content.exceptions.content_not_found_exception import ContentNotFoundException
from bhamon_blog.content.exceptions.invalid_content_exception import InvalidContentException
from bhamon_blog.content.index_item import IndexItem


class ArticleProvider:


    def __init__(self, content_directory: str, content_index: List[IndexItem]) -> None:
        self._content_directory = content_directory
        self._content_index = content_index


    def list_articles(self) -> List[Document]:
        all_articles = []

        for item in self._content_index:
            all_articles.append(self.load_article_by_reference(item.reference))

        return all_articles


    def load_article(self, identifier_or_alias: str) -> Document:
        reference = self.resolve_reference(identifier_or_alias)
        return self.load_article_by_reference(reference)


    def load_article_by_reference(self, reference: str) -> Document:
        article_file_path = os.path.join(self._content_directory, reference + ".md")

        with open(article_file_path, mode = "r", encoding = "utf-8") as article_file:
            document_raw_text = article_file.read()

        return self.parse_document(document_raw_text)


    def parse_document(self, document_raw_text: str) -> Document:
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
            document_metadata = DocumentMetadata(
                identifier = document_metadata_from_yaml["Identifier"],
                title = document_metadata_from_yaml["Title"],
                tags = document_metadata_from_yaml.get("Tags", []),
                warnings = document_metadata_from_yaml.get("Warnings", []),
                excerpt = document_metadata_from_yaml.get("Excerpt", []),
            )
        except KeyError as exception:
            raise InvalidContentException("Missing metadata field: '%s'" % exception.args[0]) from exception

        document_text = "\n".join(document_raw_lines[yaml_end_index + 1 :]).strip()

        return Document(
            metadata = document_metadata,
            content = document_text,
        )


    def resolve_reference(self, identifier_or_alias: str) -> str:
        for index_item in self._content_index:
            if identifier_or_alias == index_item.identifier:
                return index_item.reference

        for index_item in self._content_index:
            if identifier_or_alias in index_item.aliases:
                return index_item.reference

        raise ContentNotFoundException("Item not found: '%s'" % identifier_or_alias)
