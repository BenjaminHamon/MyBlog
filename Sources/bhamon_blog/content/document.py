import dataclasses

from bhamon_blog.content.document_metadata import DocumentMetadata


@dataclasses.dataclass(frozen = True)
class Document:
    metadata: DocumentMetadata
    content: str
