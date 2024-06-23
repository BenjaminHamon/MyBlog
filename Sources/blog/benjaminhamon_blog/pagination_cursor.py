import dataclasses


@dataclasses.dataclass(frozen = True)
class PaginationCursor:
    page_number: int
    page_total: int
    item_count: int
    item_total: int
    url_arguments: dict


    @property
    def skip(self) -> int:
        return (self.page_number - 1) * self.item_count


    @property
    def limit(self) -> int:
        return self.item_count
