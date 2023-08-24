""" Unit tests for application_factory """

from benjaminhamon_blog import application_factory


def test_create_application():
    application_factory.create_application("MyTitle", "MyContentDirectory")
