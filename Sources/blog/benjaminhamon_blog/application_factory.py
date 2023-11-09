# cspell:words filedb filestore

import logging
import os
from typing import Callable, List

import flask
import jinja2
import werkzeug.exceptions
import whoosh.fields
import whoosh.filedb.filestore
import whoosh.index

import benjaminhamon_blog
from benjaminhamon_blog import jinja_operations
from benjaminhamon_blog.application import Application
from benjaminhamon_blog.content.article_loader_implementation import ArticleLoaderImplementation
from benjaminhamon_blog.content.article_provider import ArticleProvider
from benjaminhamon_blog.main_controller import MainController
from benjaminhamon_blog.search import whoosh_helpers
from benjaminhamon_blog.search.whoosh_search_engine import WhooshSearchEngine


main_logger = logging.getLogger("Website")
request_logger = logging.getLogger("Request")


def create_application(title: str, content_directory: str) -> Application:
    sources_url = "https://github.com/BenjaminHamon/MyBlog"
    contact_email = "development@benjaminhamon.com"

    article_provider = create_article_provider(content_directory)
    main_controller = MainController(article_provider)

    flask_application = flask.Flask("benjaminhamon_blog")
    application = Application(flask_application)

    configure(flask_application, title, sources_url, contact_email)
    register_handlers(flask_application, application)
    register_routes(flask_application, main_controller)

    return application


def create_article_provider(content_directory: str) -> ArticleProvider:
    article_loader = ArticleLoaderImplementation(os.path.join(content_directory, "Articles"))

    schema = whoosh_helpers.create_schema_for_documents()
    index_storage = whoosh.filedb.filestore.RamStorage()
    index = whoosh.index.FileIndex.create(index_storage, schema)

    all_articles = article_loader.load_all_metadata()
    whoosh_helpers.update_index_for_documents(index, all_articles)

    search_engine = WhooshSearchEngine(index)
    article_provider = ArticleProvider(article_loader, search_engine)

    return article_provider


def configure(application: flask.Flask, title: str, sources_url: str, contact_email: str) -> None:
    application.config["WEBSITE_TITLE"] = title
    application.config["WEBSITE_COPYRIGHT"] = benjaminhamon_blog.__copyright__
    application.config["WEBSITE_VERSION"] = benjaminhamon_blog.__version__
    application.config["WEBSITE_DATE"] = benjaminhamon_blog.__date__
    application.config["WEBSITE_SOURCES_URL"] = sources_url
    application.config["WEBSITE_CONTACT_EMAIL"] = contact_email

    application.jinja_env.undefined = jinja2.StrictUndefined
    application.jinja_env.trim_blocks = True
    application.jinja_env.lstrip_blocks = True

    application.jinja_env.filters["format_document_date"] = jinja_operations.format_document_date
    application.jinja_env.filters["render_text"] = jinja_operations.render_text

    application.context_processor(lambda: { "url_for": versioned_url_for })


def register_handlers(flask_application: flask.Flask, application: Application) -> None:
    flask_application.log_exception = lambda exc_info: None
    flask_application.before_request(application.log_request)
    for exception in werkzeug.exceptions.default_exceptions.values():
        flask_application.register_error_handler(exception, application.handle_error)


def register_routes(application: flask.Flask, main_controller: MainController) -> None:
    add_url_rule(application, "/", [ "GET" ], main_controller.home)
    add_url_rule(application, "/about", [ "GET" ],  main_controller.about)
    add_url_rule(application, "/article_collection", [ "GET" ], main_controller.article_collection)
    add_url_rule(application, "/article/<identifier_or_alias>", [ "GET" ], main_controller.article)
    add_url_rule(application, "/contact", [ "GET" ],  main_controller.contact)


def add_url_rule(application: flask.Flask, path: str, methods: List[str], handler: Callable, **kwargs) -> None:
    endpoint = ".".join(handler.__module__.split(".")[1:]) + "." + handler.__name__
    application.add_url_rule(path, methods = methods, endpoint = endpoint, view_func = handler, **kwargs)


def versioned_url_for(endpoint: str, **values) -> str:
    if endpoint == "static":
        values["version"] = flask.current_app.config["WEBSITE_VERSION"]
    return flask.url_for(endpoint, **values)
