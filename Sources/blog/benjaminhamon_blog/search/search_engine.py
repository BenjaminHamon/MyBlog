import abc
from typing import Optional


class SearchEngine(abc.ABC):
    """ Interface for an engine performing queries on data sets. """


    @abc.abstractmethod
    def assert_query(self, query_string: str) -> None:
        pass


    @abc.abstractmethod
    def search(self, dataset: list, query_string: str, limit: Optional[int] = None) -> list:
        pass
