from typing import List, Optional

from benjaminhamon_blog.content.article_loader import ArticleLoader
from benjaminhamon_blog.content.document import Document
from benjaminhamon_blog.content.document_metadata import DocumentMetadata


class ArticleProvider:


    def __init__(self, article_loader: ArticleLoader) -> None:
        self._article_loader = article_loader


    def get_article_count(self) -> int:
        return len(self._article_loader.load_all_metadata())


    def list_articles(self, skip: int = 0, limit: Optional[int] = None) -> List[DocumentMetadata]:
        all_articles = self._article_loader.load_all_metadata()
        all_articles.sort(key = lambda x: x.creation_date, reverse = True)
        return all_articles[skip : skip + limit if limit is not None else None]


    def get_article(self, identifier_or_alias: str) -> Document:
        return self._article_loader.load_article(identifier_or_alias)
