import dataclasses

from automation_scripts.helpers.document_metadata import DocumentMetadata
from automation_scripts.helpers.index_item import IndexItem


@dataclasses.dataclass()
class ContentItem:
    index: IndexItem
    metadata: DocumentMetadata
    text: str
