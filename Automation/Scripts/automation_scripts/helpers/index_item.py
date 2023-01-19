import dataclasses
from typing import List


@dataclasses.dataclass()
class IndexItem:
    identifier: str
    reference: str
    aliases: List[str]
