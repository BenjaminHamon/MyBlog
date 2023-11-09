from typing import List, Optional

from benjaminhamon_blog.content.article_loader import ArticleLoader
from benjaminhamon_blog.content.document import Document
from benjaminhamon_blog.content.document_metadata import DocumentMetadata
from benjaminhamon_blog.search.search_engine import SearchEngine


class ArticleProvider:


    def __init__(self, article_loader: ArticleLoader, search_engine: SearchEngine) -> None:
        self._article_loader = article_loader
        self._search_engine = search_engine


    def get_article_count(self, query: Optional[str] = None) -> int:
        all_articles = self._article_loader.load_all_metadata()

        if query is None:
            search_results = all_articles
        else:
            search_results = self._search_engine.search(all_articles, query)

        return len(search_results)


    def list_articles(self, query: Optional[str] = None, skip: int = 0, limit: Optional[int] = None) -> List[DocumentMetadata]:
        all_articles = self._article_loader.load_all_metadata()
        all_articles.sort(key = lambda x: x.creation_date, reverse = True)

        if query is None:
            search_results = all_articles
        else:
            search_results = self._search_engine.search(all_articles, query)

        return search_results[skip : skip + limit if limit is not None else None]


    def get_article(self, identifier_or_alias: str) -> Document:
        return self._article_loader.load_article(identifier_or_alias)
