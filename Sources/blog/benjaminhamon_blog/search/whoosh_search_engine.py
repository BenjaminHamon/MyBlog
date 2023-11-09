# cspell:words filedb filestore qparser

from typing import List, Optional

import whoosh.filedb.filestore
import whoosh.index
import whoosh.qparser

from benjaminhamon_blog.search.search_engine import SearchEngine


class WhooshSearchEngine(SearchEngine):


    def __init__(self, index: whoosh.index.FileIndex) -> None:
        self._index = index


    def assert_query(self, query_string: str) -> None:
        query_string = query_string.strip()

        if query_string == "":
            return

        query_parser = whoosh.qparser.QueryParser("any", self._index.schema)

        try:
            query_parser.parse(query_string)
        except whoosh.qparser.QueryParserError as exception:
            raise ValueError("The query is invalid") from exception


    def search(self, dataset: list, query_string: str, limit: Optional[int] = None) -> list:
        query_string = query_string.strip()

        if query_string == "":
            return list(dataset)

        query_parser = whoosh.qparser.QueryParser("any", self._index.schema)

        try:
            query = query_parser.parse(query_string)
        except whoosh.qparser.QueryParserError as exception:
            raise ValueError("The query is invalid") from exception

        result_identifiers: List[str] = []
        with self._index.searcher() as searcher:
            for result in searcher.search(query, limit = limit):
                result_identifiers.append(result["identifier"])

        dataset_as_dictionary = {}
        for item in dataset:
            dataset_as_dictionary[item.identifier] = item

        all_results = []
        for identifier in result_identifiers:
            all_results.append(dataset_as_dictionary[identifier])

        return all_results
