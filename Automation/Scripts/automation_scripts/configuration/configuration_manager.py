from automation_scripts.configuration.project_configuration import ProjectConfiguration
from automation_scripts.configuration.project_version import ProjectVersion
from automation_scripts.toolkit.revision_control.git_client import GitClient


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
        identifier = "1.0.0",
        revision = revision,
        revision_date = revision_date,
        branch = branch,
    )
