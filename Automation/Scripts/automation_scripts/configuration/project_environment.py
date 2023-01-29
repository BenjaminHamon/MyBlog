from typing import Optional


class ProjectEnvironment:


    def __init__(self, python_package_repository_url: Optional[str] = None) -> None:
        self._python_package_repository_url = python_package_repository_url


    def get_python_package_repository_url(self) -> str:
        if self._python_package_repository_url is None:
            raise ValueError("Python package repository is not set")
        return self._python_package_repository_url
