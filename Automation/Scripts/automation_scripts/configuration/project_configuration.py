from automation_scripts.toolkit.automation.project_version import ProjectVersion


class ProjectConfiguration:


    def __init__(self, # pylint: disable = too-many-arguments
            project_identifier: str,
            project_display_name: str,
            project_version: ProjectVersion,
            copyright_text: str,
            author: str,
            author_email: str,
            project_url: str,
            content_identifier: str) -> None:

        self.project_identifier = project_identifier
        self.project_display_name = project_display_name
        self.project_version = project_version

        self.copyright = copyright_text

        self.author = author
        self.author_email = author_email
        self.project_url = project_url

        self.content_identifier = content_identifier


    def get_setuptools_parameters(self) -> dict:
        return {
            "version": self.project_version.full_identifier,
            "author": self.author,
            "author_email": self.author_email,
            "url": self.project_url,
        }


    def get_artifact_default_parameters(self) -> dict:
        return {
            "project": self.project_identifier,
            "version": self.project_version.identifier,
            "revision": self.project_version.revision_short,
        }
