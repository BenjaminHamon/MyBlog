""" Unit tests for application_factory """

import os

import yaml

from benjaminhamon_blog import application_factory


def test_create_application(tmpdir):
    content_directory = os.path.join(tmpdir, "MyContentDirectory")
    metadata_file_path = os.path.join(content_directory, "Articles", "Metadata.yaml")

    os.makedirs(os.path.dirname(metadata_file_path))
    with open(metadata_file_path, mode = "w", encoding = "utf-8") as metadata_file:
        yaml.dump([], metadata_file)

    application_factory.create_application("MyTitle", content_directory)
