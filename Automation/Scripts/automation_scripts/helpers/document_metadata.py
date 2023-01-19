import dataclasses
import datetime
from typing import List, Optional


@dataclasses.dataclass()
class DocumentMetadata:
    identifier: str
    reference: Optional[str]
    title: str
    tags: List[str]
    warnings: List[str]
    excerpt: str
    creation_date: Optional[datetime.datetime] = None
    update_date: Optional[datetime.datetime] = None
