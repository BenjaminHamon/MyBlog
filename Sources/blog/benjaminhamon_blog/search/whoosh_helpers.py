# cspell:words filedb filestore

from typing import List, Set

import whoosh.fields
import whoosh.filedb.filestore
import whoosh.index

from benjaminhamon_blog.content.document_metadata import DocumentMetadata


def create_schema_for_documents() -> whoosh.fields.Schema:
    return whoosh.fields.Schema(
        identifier = whoosh.fields.ID(stored = True),
        reference = whoosh.fields.ID(),
        title = whoosh.fields.ID(),
        author = whoosh.fields.TEXT(),
        tag = whoosh.fields.KEYWORD(),
        warning = whoosh.fields.KEYWORD(),
        date = whoosh.fields.DATETIME(),
        any = whoosh.fields.TEXT(),
    )


def update_index_for_documents(index: whoosh.index.Index, document_collection: List[DocumentMetadata]) -> None:
    index_writer = index.writer()
    for document in document_collection:
        index_writer.add_document(
            identifier = document.identifier,
            reference = document.reference,
            title = document.title,
            author = document.author,
            tag = convert_keywords_for_search(document.tags),
            warning = convert_keywords_for_search(document.warnings),
            date = document.creation_date,
            any = " ".join([ document.title, convert_keywords_for_search(document.tags) ])
        )

    index_writer.commit()


def convert_keywords_for_search(keyword_collection: List[str]) -> str:
    all_searchable_values: Set[str] = set()

    for keyword in keyword_collection:
        all_searchable_values.add(keyword)

        for keyword_element in keyword.split("::"):
            all_searchable_values.add(keyword_element)

    return " ".join(sorted(all_searchable_values))
