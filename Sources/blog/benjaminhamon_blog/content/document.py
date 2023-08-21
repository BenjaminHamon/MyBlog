import dataclasses

from benjaminhamon_blog.content.document_metadata import DocumentMetadata


@dataclasses.dataclass(frozen = True)
class Document:
    metadata: DocumentMetadata
    content: str
