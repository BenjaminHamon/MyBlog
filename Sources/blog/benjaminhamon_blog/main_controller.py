import math

import flask
from werkzeug.exceptions import NotFound

from benjaminhamon_blog.content.article_provider import ArticleProvider
from benjaminhamon_blog.content.exceptions.content_not_found_exception import ContentNotFoundException
from benjaminhamon_blog.pagination_cursor import PaginationCursor


class MainController:


    def __init__(self, article_provider: ArticleProvider) -> None:
        self._article_provider = article_provider


    def home(self) -> str:
        article_collection = self._article_provider.list_articles(limit = 3)
        return flask.render_template("home.html", title = "Home", article_collection = article_collection)


    def article_collection(self) -> str:

        def get_pagination(item_total: int, url_arguments: dict) -> PaginationCursor:
            item_count = max(min(flask.request.args.get("item_count", default = 10, type = int), 50), 5)
            page_total = max(int(math.ceil(item_total / item_count)), 1)
            page_number = max(min(flask.request.args.get("page", default = 1, type = int), page_total), 1)

            return PaginationCursor(
                page_number = page_number,
                page_total = page_total,
                item_count = item_count,
                item_total = item_total,
                url_arguments = url_arguments,
            )

        item_total = self._article_provider.get_article_count()
        pagination = get_pagination(item_total, {})

        article_collection = self._article_provider.list_articles(skip = pagination.skip, limit = pagination.limit)
        return flask.render_template("article_collection.html", title = "Article Collection", article_collection = article_collection, pagination = pagination)


    def article(self, identifier_or_alias: str) -> str:
        try:
            article = self._article_provider.get_article(identifier_or_alias)
        except ContentNotFoundException as exception:
            raise NotFound() from exception

        return flask.render_template("article.html", title = article.metadata.title, article = article)


    def about(self) -> str:
        return flask.render_template("about.html", title = "About")


    def contact(self) -> str:
        return flask.render_template("contact.html", title = "Contact")
