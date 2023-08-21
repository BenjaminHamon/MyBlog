import os
from typing import List, Optional

import yaml

from benjaminhamon_blog.content.document import Document
from benjaminhamon_blog.content.document_metadata import DocumentMetadata
from benjaminhamon_blog.content.exceptions.content_not_found_exception import ContentNotFoundException
from benjaminhamon_blog.content.exceptions.invalid_content_exception import InvalidContentException
from benjaminhamon_blog.content.index_item import IndexItem


class ArticleProvider:


    def __init__(self, content_directory: str) -> None:
        self._content_directory = content_directory


    def list_articles(self, skip: int = 0, limit: Optional[int] = None) -> List[DocumentMetadata]:
        all_articles = self.load_all_metadata()
        all_articles.sort(key = lambda x: x.creation_date, reverse = True)
        return all_articles[skip : skip + limit if limit is not None else None]


    def load_index(self) -> List[IndexItem]:
        index_file_path = os.path.join(self._content_directory, "Index.yaml")

        try:
            with open(index_file_path, mode = "r", encoding = "utf-8") as index_file:
                index_data = yaml.safe_load(index_file)
        except FileNotFoundError as exception:
            raise ContentNotFoundException("Index file not found: '%s'" % index_file_path) from exception

        index: List[IndexItem] = []

        for document_metadata_from_yaml in index_data:
            try:
                index.append(IndexItem(
                    identifier = document_metadata_from_yaml["identifier"],
                    reference = document_metadata_from_yaml["reference"],
                    aliases = document_metadata_from_yaml["aliases"],
                ))
            except KeyError as exception:
                raise InvalidContentException("Missing metadata field: '%s'" % exception.args[0]) from exception

        return index


    def load_all_metadata(self) -> List[DocumentMetadata]:
        index_file_path = os.path.join(self._content_directory, "Metadata.yaml")

        try:
            with open(index_file_path, mode = "r", encoding = "utf-8") as index_file:
                index_data = yaml.safe_load(index_file)
        except FileNotFoundError as exception:
            raise ContentNotFoundException("Index file not found: '%s'" % index_file_path) from exception

        all_articles: List[DocumentMetadata] = []

        for document_metadata_from_yaml in index_data:
            try:
                all_articles.append(DocumentMetadata(
                    identifier = document_metadata_from_yaml["identifier"],
                    reference = document_metadata_from_yaml["reference"],
                    title = document_metadata_from_yaml["title"],
                    author = document_metadata_from_yaml["author"],
                    tags = document_metadata_from_yaml.get("tags", []),
                    warnings = document_metadata_from_yaml.get("warnings", []),
                    excerpt = document_metadata_from_yaml.get("excerpt", []),
                    creation_date = document_metadata_from_yaml.get("creation_date"),
                    update_date = document_metadata_from_yaml.get("update_date"),
                ))
            except KeyError as exception:
                raise InvalidContentException("Missing metadata field: '%s'" % exception.args[0]) from exception

        return all_articles


    def load_article(self, identifier_or_alias: str) -> Document:
        index = self.load_index()
        all_metadata = self.load_all_metadata()

        index_item = self._find_in_index(index, identifier_or_alias)
        document_metadata = self._get_metadata(all_metadata, index_item.identifier)
        document_text = self._load_article_html(index_item.reference)

        return Document(
            metadata = document_metadata,
            content = document_text,
        )


    def _find_in_index(self, content_index: List[IndexItem], identifier_or_alias: str) -> IndexItem:
        for index_item in content_index:
            if identifier_or_alias == index_item.identifier:
                return index_item

        for index_item in content_index:
            if identifier_or_alias in index_item.aliases:
                return index_item

        raise ContentNotFoundException("Item not found: '%s'" % identifier_or_alias)


    def _get_metadata(self, all_metadata: List[DocumentMetadata], identifier: str) -> DocumentMetadata:
        document_metadata = next((x for x in all_metadata if x.identifier == identifier), None)
        if document_metadata is None:
            raise ContentNotFoundException("Missing metadata for identifier: '%s'" % identifier)

        return document_metadata


    def _load_article_html(self, reference: str) -> str:
        article_file_path = os.path.join(self._content_directory, reference + ".html")
        with open(article_file_path, mode = "r", encoding = "utf-8") as article_file:
            return article_file.read()
