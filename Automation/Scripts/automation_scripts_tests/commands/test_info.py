import argparse

from automation_scripts.commands.info import InfoCommand
from automation_scripts.toolkit.automation import automation_helpers


def test_run(tmpdir):
    with automation_helpers.execute_in_workspace(tmpdir):
        command = InfoCommand()
        command.run(argparse.Namespace(), simulate = False)


def test_run_with_simulate(tmpdir):
    with automation_helpers.execute_in_workspace(tmpdir):
        command = InfoCommand()
        command.run(argparse.Namespace(), simulate = True)
