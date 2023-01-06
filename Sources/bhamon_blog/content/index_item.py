import dataclasses
from typing import List


@dataclasses.dataclass(frozen = True)
class IndexItem:
    identifier: str
    reference: str
    aliases: List[str]
