from automation_scripts.configuration.project_version import ProjectVersion


class ProjectConfiguration:


    def __init__(self, project_identifier: str, project_display_name: str, project_version: ProjectVersion) -> None:
        self.project_identifier = project_identifier
        self.project_display_name = project_display_name
        self.project_version = project_version

        self.copyright = "Copyright (c) 2023 Benjamin Hamon"


    def get_artifact_default_parameters(self) -> dict:
        return {
            "project": self.project_identifier,
            "version": self.project_version.identifier,
            "revision": self.project_version.revision_short,
        }
