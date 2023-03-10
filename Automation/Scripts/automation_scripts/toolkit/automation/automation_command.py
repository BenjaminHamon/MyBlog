import abc
import argparse


class AutomationCommand(abc.ABC):


    @abc.abstractmethod
    def configure_argument_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser: # pylint: disable = protected-access
        pass


    @abc.abstractmethod
    def check_requirements(self) -> None:
        pass


    @abc.abstractmethod
    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        pass
