""" Unit tests for ContentImporter """

from automation_scripts.helpers.content_importer import ContentImporter

import pytest


def test_parse_document():
    content_importer = ContentImporter()

    document_raw_text = """

---
Identifier: my_identifier
Title: my_title
Author: my_author
---

Some text.

"""

    metadata, text = content_importer.parse_document(document_raw_text)

    assert metadata.identifier == "my_identifier"
    assert metadata.title == "my_title"
    assert text == "Some text."


def test_parse_document_with_extra_separator():
    content_importer = ContentImporter()

    document_raw_text = """

---
Identifier: my_identifier
Title: my_title
Author: my_author
---

Some text.

---

Some text after the separator.

"""

    metadata, text = content_importer.parse_document(document_raw_text)

    assert metadata.identifier == "my_identifier"
    assert metadata.title == "my_title"
    assert text == "Some text.\n\n---\n\nSome text after the separator."


def test_parse_document_with_missing_header():
    content_importer = ContentImporter()

    document_raw_text = """

Some text.

"""

    with pytest.raises(ValueError):
        content_importer.parse_document(document_raw_text)


def test_parse_document_with_mismatch_separators():
    content_importer = ContentImporter()

    document_raw_text = """

---
Identifier: my_identifier
Title: my_title
Author: my_author

Some text.

"""

    with pytest.raises(ValueError):
        content_importer.parse_document(document_raw_text)
