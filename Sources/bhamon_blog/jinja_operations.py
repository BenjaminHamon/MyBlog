import datetime
from typing import Optional

from bhamon_blog.content.document_metadata import DocumentMetadata


def format_document_date(metadata: DocumentMetadata, now: Optional[datetime.datetime] = None) -> str:

    def format_date(value: datetime.datetime) -> str:
        return value.strftime("%d %B %Y").lstrip("0")

    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)

    if metadata.update_date.date() > metadata.creation_date.date():
        return format_date(metadata.creation_date) + " (Updated on %s)" % format_date(metadata.update_date)

    if now.date() == metadata.creation_date.date():
        return format_date(metadata.creation_date) + " (Today)"
    if now.date() == metadata.creation_date.date() + datetime.timedelta(days = 1):
        return format_date(metadata.creation_date) + " (Yesterday)"

    return format_date(metadata.creation_date)


def render_text(value: Optional[str]) -> str:
    return value if value is not None else ""
