import logging
import os
from typing import Callable, List

import flask
import jinja2
import werkzeug.exceptions

import bhamon_blog
from bhamon_blog import jinja_operations
from bhamon_blog.application import Application
from bhamon_blog.content.article_provider import ArticleProvider
from bhamon_blog.main_controller import MainController


main_logger = logging.getLogger("Website")
request_logger = logging.getLogger("Request")


def create_application(content_directory: str) -> Application:
    article_provider = ArticleProvider(os.path.join(content_directory, "Articles"))
    main_controller = MainController(article_provider)

    flask_application = flask.Flask("bhamon_blog")
    application = Application(flask_application)

    configure(flask_application, "Benjamin Hamon's blog")
    register_handlers(flask_application, application)
    register_routes(flask_application, main_controller)

    return application


def configure(application: flask.Flask, title: str) -> None:
    application.config["WEBSITE_TITLE"] = title
    application.config["WEBSITE_COPYRIGHT"] = bhamon_blog.__copyright__
    application.config["WEBSITE_VERSION"] = bhamon_blog.__version__
    application.config["WEBSITE_DATE"] = bhamon_blog.__date__

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


def add_url_rule(application: flask.Flask, path: str, methods: List[str], handler: Callable, **kwargs) -> None:
    endpoint = ".".join(handler.__module__.split(".")[1:]) + "." + handler.__name__
    application.add_url_rule(path, methods = methods, endpoint = endpoint, view_func = handler, **kwargs)


def versioned_url_for(endpoint: str, **values) -> str:
    if endpoint == "static":
        values["version"] = flask.current_app.config["WEBSITE_VERSION"]
    return flask.url_for(endpoint, **values)
