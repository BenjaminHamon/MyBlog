import os
import shutil

from bhamon_development_toolkit.revision_control import git_helpers


def copy_workspace_file_to_test_directory(file_path_in_workspace: str, test_directory: str) -> None:
    workspace_root = git_helpers.resolve_repository_path(__file__)

    source = os.path.join(workspace_root, file_path_in_workspace)
    destination = os.path.join(test_directory, file_path_in_workspace)

    os.makedirs(os.path.dirname(destination), exist_ok = True)
    shutil.copy(source, destination)
