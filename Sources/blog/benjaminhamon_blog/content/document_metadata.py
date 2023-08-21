import dataclasses
import datetime
from typing import List


@dataclasses.dataclass(frozen = True)
class DocumentMetadata:
    identifier: str
    reference: str
    title: str
    tags: List[str]
    warnings: List[str]
    excerpt: str
    creation_date: datetime.datetime
    update_date: datetime.datetime
