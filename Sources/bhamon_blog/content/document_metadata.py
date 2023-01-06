import dataclasses
from typing import List


@dataclasses.dataclass(frozen = True)
class DocumentMetadata:
    identifier: str
    title: str
    tags: List[str]
    warnings: List[str]
    excerpt: str
