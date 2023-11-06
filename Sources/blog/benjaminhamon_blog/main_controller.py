import flask
from werkzeug.exceptions import NotFound

from benjaminhamon_blog.content.article_provider import ArticleProvider
from benjaminhamon_blog.content.exceptions.content_not_found_exception import ContentNotFoundException


class MainController:


    def __init__(self, article_provider: ArticleProvider) -> None:
        self._article_provider = article_provider


    def home(self) -> str:
        article_collection = self._article_provider.list_articles(limit = 3)
        return flask.render_template("home.html", title = "Home", article_collection = article_collection)


    def article_collection(self) -> str:
        article_collection = self._article_provider.list_articles()
        return flask.render_template("article_collection.html", title = "Article Collection", article_collection = article_collection)


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
