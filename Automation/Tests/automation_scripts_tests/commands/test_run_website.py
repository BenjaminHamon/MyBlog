import argparse
import os

import mockito

from bhamon_development_toolkit.automation import automation_helpers

from automation_scripts.commands.run_website import RunWebsiteCommand
from automation_scripts.configuration.project_configuration import ProjectConfiguration


def test_run_with_simulate(tmpdir):
    with automation_helpers.execute_in_workspace(tmpdir):
        os.makedirs("Content/Articles")
        with open("Content/Articles/Metadata.yaml", mode = "w", encoding = "utf-8") as metadata_file:
            metadata_file.write("[]")

        project_configuration = mockito.mock(spec = ProjectConfiguration)

        command = RunWebsiteCommand()
        arguments = argparse.Namespace(address = None, port = None)

        command.run(arguments, configuration = project_configuration, simulate = True)
