import argparse

from automation_scripts.toolkit.automation.automation_command import AutomationCommand


class InfoCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        return subparsers.add_parser("info", help = "show project information")


    def check_requirements(self) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        pass
