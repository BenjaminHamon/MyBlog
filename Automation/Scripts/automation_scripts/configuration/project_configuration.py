from automation_scripts.toolkit.automation.project_version import ProjectVersion


class ProjectConfiguration:


    def __init__(self, project_identifier: str, project_display_name: str, project_version: ProjectVersion) -> None:
        self.project_identifier = project_identifier
        self.project_display_name = project_display_name
        self.project_version = project_version

        self.copyright = "Copyright (c) 2023 Benjamin Hamon"

        self.content_identifier = "Samples"


    def get_setuptools_parameters(self) -> dict:
        return {
            "version": self.project_version.full_identifier,
            "author": "Benjamin Hamon",
            "author_email": "development@benjaminhamon.com",
            "url": "https://github.com/BenjaminHamon/MyBlog",
        }


    def get_artifact_default_parameters(self) -> dict:
        return {
            "project": self.project_identifier,
            "version": self.project_version.identifier,
            "revision": self.project_version.revision_short,
        }
