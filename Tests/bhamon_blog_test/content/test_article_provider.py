""" Unit tests for ArticleProvider """

from bhamon_blog.content.article_provider import ArticleProvider
from bhamon_blog.content.exceptions.invalid_content_exception import InvalidContentException

import pytest


def test_parse_document(tmpdir):
    article_provider = ArticleProvider(str(tmpdir), [])

    document_raw_text = """

---
Identifier: my_identifier
Title: my_title
---

Some text.

"""

    document = article_provider.parse_document(document_raw_text)

    assert document.metadata.identifier == "my_identifier"
    assert document.metadata.title == "my_title"
    assert document.content == "Some text."


def test_parse_document_with_extra_separator(tmpdir):
    article_provider = ArticleProvider(str(tmpdir), [])

    document_raw_text = """

---
Identifier: my_identifier
Title: my_title
---

Some text.

---

Some text after the separator.

"""

    document = article_provider.parse_document(document_raw_text)

    assert document.metadata.identifier == "my_identifier"
    assert document.metadata.title == "my_title"
    assert document.content == "Some text.\n\n---\n\nSome text after the separator."


def test_parse_document_with_missing_header(tmpdir):
    article_provider = ArticleProvider(str(tmpdir), [])

    document_raw_text = """

Some text.

"""

    with pytest.raises(InvalidContentException):
        article_provider.parse_document(document_raw_text)


def test_parse_document_with_mismatch_separators(tmpdir):
    article_provider = ArticleProvider(str(tmpdir), [])

    document_raw_text = """

---
Identifier: my_identifier
Title: my_title

Some text.

"""

    with pytest.raises(InvalidContentException):
        article_provider.parse_document(document_raw_text)
