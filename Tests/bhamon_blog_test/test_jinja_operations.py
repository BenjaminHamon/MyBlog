""" Unit tests for jinja_operations """

import datetime

from benjaminhamon_blog import jinja_operations
from benjaminhamon_blog.content.document_metadata import DocumentMetadata


def test_format_date():
    base_date = datetime.datetime(year = 2000, month = 1, day = 1)
    metadata_as_dict = {
        "identifier": "MyIdentifier",
        "reference": "MyReference",
        "title": "MyTitle",
        "tags": [],
        "warnings": [],
        "excerpt": "",
    }

    metadata = DocumentMetadata(**metadata_as_dict, creation_date = base_date, update_date = base_date)
    assert jinja_operations.format_document_date(metadata, base_date) == "1 January 2000 (Today)"
    assert jinja_operations.format_document_date(metadata, base_date + datetime.timedelta(days = 1)) == "1 January 2000 (Yesterday)"
    assert jinja_operations.format_document_date(metadata, base_date + datetime.timedelta(days = 2)) == "1 January 2000"

    metadata = DocumentMetadata(**metadata_as_dict, creation_date = base_date, update_date = base_date + datetime.timedelta(days = 1))
    assert jinja_operations.format_document_date(metadata, base_date + datetime.timedelta(days = 1)) == "1 January 2000 (Updated on 2 January 2000)"
