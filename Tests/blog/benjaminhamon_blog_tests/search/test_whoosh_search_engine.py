""" Unit tests for WhooshSearchEngine """

# cspell:words filedb filestore

import datetime
from typing import List

import whoosh.fields
import whoosh.filedb.filestore
import whoosh.index

from benjaminhamon_blog.content.document_metadata import DocumentMetadata
from benjaminhamon_blog.search import whoosh_helpers
from benjaminhamon_blog.search.whoosh_search_engine import WhooshSearchEngine


def create_search_engine(document_collection: List[DocumentMetadata]) -> WhooshSearchEngine:
    schema = whoosh_helpers.create_schema_for_documents()

    index_storage = whoosh.filedb.filestore.RamStorage()
    index = whoosh.index.FileIndex.create(index_storage, schema)

    whoosh_helpers.update_index_for_documents(index, document_collection)

    return WhooshSearchEngine(index)


def test_search_with_identifier():
    """ Test search with an identifier field """

    all_documents = [
        DocumentMetadata(
            identifier = "identifier",
            reference = "reference",
            title = "The Title",
            author = "The Author",
            tags = [],
            warnings = [],
            excerpt = "",
            creation_date = datetime.datetime.min,
            update_date = datetime.datetime.min,
        )
    ]

    search_engine = create_search_engine(all_documents)

    results = search_engine.search(all_documents, "identifier:identifier")
    assert len(results) == 1
    assert results[0] == all_documents[0]

    results = search_engine.search(all_documents, "identifier:another-identifier")
    assert len(results) == 0


def test_search_with_text():
    """ Test search with a text field """

    all_documents = [
        DocumentMetadata(
            identifier = "identifier",
            reference = "reference",
            title = "The Title",
            author = "The Author",
            tags = [],
            warnings = [],
            excerpt = "",
            creation_date = datetime.datetime.min,
            update_date = datetime.datetime.min,
        )
    ]

    search_engine = create_search_engine(all_documents)

    results = search_engine.search(all_documents, "The Title")
    assert len(results) == 1
    assert results[0] == all_documents[0]

    results = search_engine.search(all_documents, "Another Title")
    assert len(results) == 0

    results = search_engine.search(all_documents, "title: 'The Title'")
    assert len(results) == 1
    assert results[0] == all_documents[0]

    results = search_engine.search(all_documents, "title: 'Another Title'")
    assert len(results) == 0


def test_search_with_keyword():
    """ Test search with a keyword field """

    all_documents = [
        DocumentMetadata(
            identifier = "identifier",
            reference = "reference",
            title = "The Title",
            author = "The Author",
            tags = [ "MyTag" ],
            warnings = [],
            excerpt = "",
            creation_date = datetime.datetime.min,
            update_date = datetime.datetime.min,
        )
    ]

    search_engine = create_search_engine(all_documents)

    results = search_engine.search(all_documents, "MyTag")
    assert len(results) == 1
    assert results[0] == all_documents[0]

    results = search_engine.search(all_documents, "AnotherTag")
    assert len(results) == 0

    results = search_engine.search(all_documents, "tag:MyTag")
    assert len(results) == 1
    assert results[0] == all_documents[0]

    results = search_engine.search(all_documents, "tag:AnotherTag")
    assert len(results) == 0


def test_search_with_namespaced_keyword():
    """ Test search with a namespaced keyword field """

    all_documents = [
        DocumentMetadata(
            identifier = "identifier",
            reference = "reference",
            title = "The Title",
            author = "The Author",
            tags = [ "MyCategory::MySubcategory::MyTag" ],
            warnings = [],
            excerpt = "",
            creation_date = datetime.datetime.min,
            update_date = datetime.datetime.min,
        )
    ]

    search_engine = create_search_engine(all_documents)

    results = search_engine.search(all_documents, "MyCategory::MySubcategory::MyTag")
    assert len(results) == 1
    assert results[0] == all_documents[0]

    results = search_engine.search(all_documents, "MyCategory::MySubcategory::AnotherTag")
    assert len(results) == 0

    results = search_engine.search(all_documents, "MyTag")
    assert len(results) == 1
    assert results[0] == all_documents[0]

    results = search_engine.search(all_documents, "AnotherTag")
    assert len(results) == 0

    results = search_engine.search(all_documents, "tag:'MyCategory::MySubcategory::MyTag'")
    assert len(results) == 1
    assert results[0] == all_documents[0]

    results = search_engine.search(all_documents, "tag:'MyCategory::MySubcategory::AnotherTag'")
    assert len(results) == 0

    results = search_engine.search(all_documents, "tag:MyTag")
    assert len(results) == 1
    assert results[0] == all_documents[0]

    results = search_engine.search(all_documents, "tag:AnotherTag")
    assert len(results) == 0


def test_search_with_many_items():
    """ Test search with many items """

    all_documents = []

    for i in range(20):
        all_documents.append(DocumentMetadata(
            identifier = "identifier-%s" % i,
            reference = "reference-%s" % i,
            title = "The Title of Article %s" % i,
            author = "The Author",
            tags = [ "MyTag" ],
            warnings = [],
            excerpt = "",
            creation_date = datetime.datetime.min,
            update_date = datetime.datetime.min,
        ))


    search_engine = create_search_engine(all_documents)

    results = search_engine.search(all_documents, "MyTag")
    assert len(results) == 20
