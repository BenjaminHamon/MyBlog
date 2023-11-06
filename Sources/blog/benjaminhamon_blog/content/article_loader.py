import abc
from typing import List

from benjaminhamon_blog.content.document import Document
from benjaminhamon_blog.content.document_metadata import DocumentMetadata


class ArticleLoader(abc.ABC):


    @abc.abstractmethod
    def load_all_metadata(self) -> List[DocumentMetadata]:
        pass


    @abc.abstractmethod
    def load_article(self, identifier_or_alias: str) -> Document:
        pass
