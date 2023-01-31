class ProjectEnvironment:


    def get_application_content_repository_url(self) -> str:
        return "https://nexus.benjaminhamon.com/repository/application-content"


    def get_python_package_repository_url(self, target_environment: str) -> str:
        if target_environment == "Development":
            return "https://nexus.benjaminhamon.com/repository/python-packages-development"
        if target_environment == "Production":
            return "https://nexus.benjaminhamon.com/repository/python-packages"

        raise ValueError("Unknown environment: '%s'" % target_environment)
