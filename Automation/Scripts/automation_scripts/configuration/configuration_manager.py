from typing import List

from automation_scripts.configuration.project_configuration import ProjectConfiguration
from automation_scripts.configuration.project_environment import ProjectEnvironment
from automation_scripts.toolkit.automation.project_version import ProjectVersion
from automation_scripts.toolkit.python.python_package import PythonPackage
from automation_scripts.toolkit.revision_control.git_client import GitClient


def load_environment() -> ProjectEnvironment:
    return ProjectEnvironment()


def load_configuration() -> ProjectConfiguration:
    return ProjectConfiguration(
        project_identifier = "MyBlog",
        project_display_name = "MyBlog",
        project_version = load_project_version(),
    )


def load_project_version() -> ProjectVersion:
    git_client = GitClient("git")

    revision = git_client.get_current_revision()
    revision_date = git_client.get_revision_date(revision)
    branch = git_client.get_current_branch()

    return ProjectVersion(
        identifier = "1.0.1",
        revision = revision,
        revision_date = revision_date,
        branch = branch,
    )


def list_python_packages() -> List[PythonPackage]:
    return [
        PythonPackage(name = "bhamon_blog", path_to_sources = "Sources"),
    ]
